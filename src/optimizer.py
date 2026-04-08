import json
from collections import defaultdict

def load_data():
    with open("../data/constraints.json") as f:
        return json.load(f)
    

def allct_rooms(data, ass):

    gpd = defaultdict(list)
    clss_lookup = {c["class_id"]: c for c in data["classes"]}
    rooms = sorted(data["rooms"], key=lambda r: r["capacity"])


    for c_id, s in ass.items():

        gpd[s].append(clss_lookup[c_id])

    schedule = []

    for s, sloted_clss in gpd.items():
        
        srtd_cls = sorted(sloted_clss, key=lambda x: x["enrolled"], reverse=True)
        usd_rm = set()

        for c in srtd_cls:
            for r in rooms:
                if r["room_id"] not in usd_rm and r["capacity"] >= c["enrolled"]:

                    schedule.append({
                        "class_id": c["class_id"],
                        "group_id": c["group_id"],
                        "professor_id": c["professor_id"],
                        "enrolled": c["enrolled"],
                        "time_slot": s,
                        "room_id": r["room_id"],
                        "capacity": r["capacity"],
                        "wasted": r["capacity"] - c["enrolled"]
                    })

                    usd_rm.add(r["room_id"])

                    break


    print(schedule)
    total_waste = sum(s["wasted"] for s in schedule)
    print(f"Total wasted seats: {total_waste}")
    return schedule


if __name__ == "__main__":

    from graph_engine import conflict_graph, welsh_powell
    
    data = load_data()
    time_slots = ["MON-09:00", "MON-11:00", "MON-13:00", "MON-15:00",
                  "TUE-09:00", "TUE-11:00", "TUE-13:00", "TUE-15:00",
                  "WED-09:00", "WED-11:00", "WED-13:00", "WED-15:00",
                  "THU-09:00", "THU-11:00", "THU-13:00", "THU-15:00",
                  "FRI-09:00", "FRI-11:00", "FRI-13:00", "FRI-15:00"]
    
    graph = conflict_graph(data["classes"])
    ass = welsh_powell(graph, time_slots)
    allct_rooms(data, ass)

