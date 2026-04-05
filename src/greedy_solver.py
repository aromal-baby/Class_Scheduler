import json

# To load the generated json data constraints
def load_data():

    with open("../data/constraints.json") as f:
        return json.load(f)
    


# ACtuall algorithm application
def greedy_solver(data):

    time_slots = time_slots = [
        "MON-09:00", "MON-11:00", "MON-13:00", "MON-15:00",
        "TUE-09:00", "TUE-11:00", "TUE-13:00", "TUE-15:00",
        "WED-09:00", "WED-11:00", "WED-13:00", "WED-15:00",
        "THU-09:00", "THU-11:00", "THU-13:00", "THU-15:00",
        "FRI-09:00", "FRI-11:00", "FRI-13:00", "FRI-15:00",
    ]

    # To sort classes to descending according to enrolled constraint
    classes = sorted(data["classes"], key=lambda x: x["enrolled"], reverse=True)

    # Tracking..
    prof_busy = {}
    room_busy = {}
    grp_busy = {}

    scheduled = []
    unscheduled = []

    rooms = data["rooms"]

    for c in classes:

        prof_id = c["professor_id"]
        grp_id = c["group_id"]
        
        placed = False

        for s in time_slots:
            for r in rooms:

                room_id = r["room_id"]
                if s not in prof_busy.get(prof_id, []):
                    if s not in room_busy.get(room_id,[]):
                        if s not in grp_busy.get(grp_id, []):
                            if r["capacity"] >= c["enrolled"]:
                            
                                scheduled.append({
                                    "professor_id": prof_id,
                                    "group_id": grp_id,
                                    "room_id": room_id,
                                    "time_slots": s,
                                    "enrolled": c["enrolled"],
                                    "capacity": r["capacity"]
                                })
                                prof_busy.setdefault(prof_id, []).append(s)
                                room_busy.setdefault(room_id, []).append(s)
                                grp_busy.setdefault(grp_id, []).append(s)
                                placed = True
            if placed:
                break

        if not placed:
            unscheduled.append(c)

    print(scheduled, unscheduled)
    return scheduled, unscheduled



if __name__ == "__main__":

    data = load_data()
    greedy_solver(data)



