import json


def load_data():
    with open("../data/constraints.json") as f:
        return json.load(f)
    
def is_valid(cls, slot, room, prof_busy, room_busy, group_busy):
    
    if slot in prof_busy.get(cls["professor_id"], []):
        return False
    
    if slot in room_busy.get(room["room_id"], []):
        return False
    
    if slot in group_busy.get(cls["group_id"], []):
        return False
    
    if room["capacity"] < cls["enrolled"]:
        return False
    
    return True


def backtrack(classes, index, schedule, prof_busy, room_busy, group_busy, rooms, time_slots):
    
    if index == len(classes):
        return True 
    
    cls = classes[index]
    
    for s in time_slots:
        for r in rooms:
            if is_valid(cls, s, r, prof_busy, room_busy, group_busy):
                
                # assign
                prof_busy.setdefault(cls["professor_id"], []).append(s)
                room_busy.setdefault(r["room_id"], []).append(s)
                group_busy.setdefault(cls["group_id"], []).append(s)
                schedule.append({
                        "class_id": cls["class_id"],
                        "group_id": cls["group_id"],
                        "professor_id": cls["professor_id"],
                        "enrolled": cls["enrolled"],
                        "time_slot": s,
                        "room_id": r["room_id"],
                        "capacity": r["capacity"],
                        "wasted": r["capacity"] - cls["enrolled"]
                    })  
                
                if backtrack(classes, index+1, schedule, prof_busy, room_busy, group_busy, rooms, time_slots):
                    return True
                
                # unassign (backtrack)
                prof_busy[cls["professor_id"]].remove(s)
                room_busy[r["room_id"]].remove(s)
                group_busy[cls["group_id"]].remove(s)
                schedule.pop()
    
    return False


def run_backtracker(data):
    
    classes = sorted(data["classes"], key=lambda x: x["enrolled"], reverse=True)
    rooms = sorted(data["rooms"], key=lambda r: r["capacity"])
    time_slots = [
        "MON-09:00", "MON-11:00", "MON-13:00", "MON-15:00",
        "TUE-09:00", "TUE-11:00", "TUE-13:00", "TUE-15:00",
        "WED-09:00", "WED-11:00", "WED-13:00", "WED-15:00",
        "THU-09:00", "THU-11:00", "THU-13:00", "THU-15:00",
        "FRI-09:00", "FRI-11:00", "FRI-13:00", "FRI-15:00",
    ]
    
    schedule = []
    prof_busy = {}
    room_busy = {}
    group_busy = {}
    
    backtrack(classes, 0, schedule, prof_busy, room_busy, group_busy, rooms, time_slots)
    
    scheduled_ids = {s["class_id"] for s in schedule}
    unscheduled = [c for c in classes if c["class_id"] not in scheduled_ids]
    
    return schedule, unscheduled


if __name__ == "__main__":
    data = load_data()
    schedule, unscheduled = run_backtracker(data)
    
    print(f"Scheduled: {len(schedule)}")
    print(f"Unscheduled: {len(unscheduled)}")
    
    total_waste = sum(s["wasted"] for s in schedule)
    print(f"Total wasted seats: {total_waste}")
    
    if unscheduled:
        print("Unscheduled classes (manual intervention needed):")
        for c in unscheduled:
            print(f"  ✗ {c['class_id']} - {c['group_id']}")
