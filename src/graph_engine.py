import json
from collections import Counter

def conflict_graph(classes):

    graph = {}

    for c in classes:

        graph[c["class_id"]] = []
    
    # To check evry pair or calsses cpnflicting or not
    for i in range(len(classes)):
        for j in range(i+1, len(classes)):

            a = classes[i]
            b = classes[j]

            if a["professor_id"] == b["professor_id"] or a["group_id"] == b["group_id"]:
                graph[a["class_id"]].append(b["class_id"])
                graph[b["class_id"]].append(a["class_id"])

    # edges = sum(len(v) for v in graph.values()) // 2
    # print(f"Total edges: {edges}")
    # prof_counts = Counter(cls["professor_id"] for cls in classes)
    # duplicates = {p: c for p, c in prof_counts.items() if c > 1}
    # print(f"Professors teaching multiple classes: {len(duplicates)}")
    # print(duplicates)


    return graph

def welsh_powell(graph, time_slots):

    nodes = sorted(graph.keys(), key=lambda n: len(graph[n]), reverse=True)

    assgnmnt = {}

    for n in nodes:
        # Finding slots used by   already assigned neighbours
        ngbr_slots = []
        for nb in graph[n]:
            if nb in assgnmnt:
                ngbr_slots.append(assgnmnt[nb])

        # To pick the first slot that is not in the neighbour slots
        for s in time_slots:
            if s not in ngbr_slots:
                assgnmnt[n] = s
                break

    # print(assgnmnt)
    # print(f"Assigned: {len(assgnmnt)}")
    # print(f"Missing: {[c['class_id'] for c in classes if c['class_id'] not in assgnmnt]}")
    return assgnmnt


def load_data():
    with open("../data/constraints.json") as f:
        return json.load(f)
    

def print_graph(graph):
    print("\nConflict Graph:")
    for class_id, neighbours in graph.items():
        if neighbours:
            print(f"  {class_id} → {', '.join(neighbours)}")



if __name__ == "__main__":
    data = load_data()
    classes = data["classes"]
    time_slots = [
        "MON-09:00", "MON-11:00", "MON-13:00", "MON-15:00",
        "TUE-09:00", "TUE-11:00", "TUE-13:00", "TUE-15:00",
        "WED-09:00", "WED-11:00", "WED-13:00", "WED-15:00",
        "THU-09:00", "THU-11:00", "THU-13:00", "THU-15:00",
        "FRI-09:00", "FRI-11:00", "FRI-13:00", "FRI-15:00",
    ]
    
    graph = conflict_graph(classes)
    assignment = welsh_powell(graph, time_slots)
    
    print(assignment)