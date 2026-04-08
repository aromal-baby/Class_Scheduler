import json, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from greedy_solver import greedy_solver, load_data
from graph_engine import conflict_graph, welsh_powell, print_graph
from optimizer import allct_rooms
from backtracker import run_backtracker

def conflict_report(schdld, unschdld):

    print(f"{'CONFLICT REPORT':^55}")

    for s in schdld:

        waste = s["wasted"]
        if waste == 0 :
            note = "Perfect Fit" 
        else:
            note = f"Wasted {waste} seats"

        print(f"Scheduled   {s['class_id']:<12} {s['time_slot']:<14} {s['room_id']:<8} {note}")
    
    for c in unschdld:

        print(f"Unscheduled {c['class_id']:<12} {'N/A':<14} {'N/A':<8}")


if __name__ == "__main__":

    data = load_data()
    time_slots = [
        "MON-09:00", "MON-11:00", "MON-13:00", "MON-15:00",
        "TUE-09:00", "TUE-11:00", "TUE-13:00", "TUE-15:00",
        "WED-09:00", "WED-11:00", "WED-13:00", "WED-15:00",
        "THU-09:00", "THU-11:00", "THU-13:00", "THU-15:00",
        "FRI-09:00", "FRI-11:00", "FRI-13:00", "FRI-15:00",
    ]


    print("Stage 1 - Greedy")
    grd_sched, grd_unsched = greedy_solver(data)
    grd_wst = 0
    for s in grd_sched:
        grd_wst += s["capacity"] - s["enrolled"]
    print(f"Scheduled: {len(grd_sched)} | Wasted: {grd_wst}")


    print("Stage 2 - Graph Colouring")
    grph = conflict_graph(data["classes"])
    assgnmt = welsh_powell(grph, time_slots)
    print(f"Classes assigned slots: {len(assgnmt)}")
    print_graph(grph)


    print("Stage 3 - Room Allocation")
    dp_schd = allct_rooms(data, assgnmt)
    dp_waste = 0
    for s in dp_schd:
        dp_waste += s["wasted"]
    print(f"Scheduled: {len(dp_schd)} | Wasted: {dp_waste}")


    print("Stage 4 - Backtracking")
    bt_schd,  bt_unschd = run_backtracker(data)
    bt_wst = 0
    for s in bt_schd:
        bt_wst += s["wasted"]
    print(f"Scheduled: {len(bt_schd)} | Wasted: {bt_wst}")



    print(" Final Conflict Report (Backtracking)")
    conflict_report(bt_schd, bt_unschd)


    
    print("WASTE COMPARISON")
    print(f"Greedy:       {grd_wst} wasted seats")
    print(f"DP Allocator: {dp_waste} wasted seats")
    print(f"Backtracking: {bt_wst} wasted seats")
        
