"""
# To Generate the data and save it json which is need for this project
"""
import random
import json

# To generate student data 
def std_gen():

    students = []

    for i in range(1, 5001):
        
        student_i = {
            "matriculation": f"MAT-{i:05d}",
            "name": f"Student_{i}",
            "group": None
        }
    
        students.append(student_i)
        # print(students)
    
    return students




# To generate Professors data
def gen_prfs():

    profs = []

    for i in range(1, 301):

        prof_i = {
            "prof_id": f"PROF-{i:04d}",
            "name": f"Professor_{i}"
        }

        profs.append(prof_i)
    
    # print(profs)
    return profs



# To generate different studfent groups
def grp_gen():

    groups = []
    years = [1, 2, 3]
    programmes = {
        "CS": ["A", "B", "C"], 
        "BBA": ["A", "B", "C"], 
        "LO": ["A", "B"],
        "LA": ["A", "B"], 
        "BC": ["A", "B", "C"]
        }
               
    sections = ["A", "B", "C"]

    for y in years:
        for p, sections in programmes.items():
            for s in sections :
                group_name = f"Y{y}-{p}-{s}"
                groups.append(group_name)      
    
    # print(groups)
    return groups


# To generate the 50 rooms with varied capacities
def gen_rooms():

    room_types = [
        ("small", 5, 25, 30),
        ("standard", 25, 65, 80),
        ("medium", 15, 120, 150),
        ("large", 5, 400, 500),
    ]

    rooms = []

    # for i in range(1, 51):
    #     rooms_i = {
    #         "room_id": f"R-{i:03d}"
    #     }
    #     rooms.append(rooms_i)

    room_id = 1

    for name, count, min_cap, max_cap in room_types:
        for i in range(count):
            rooms_i = {
                "room_id": f"R-{room_id:03d}",
                "capacity": random.randint(min_cap, max_cap),
                "type": name 
            }
            rooms.append(rooms_i)
            room_id += 1
    
    # print(rooms)
    return rooms


def grp_assgn():
    students = std_gen()      
    random.shuffle(students)    # TO simulate the logic of students not having the matriculation number in order in the group   
    groups = grp_gen()     
    
    result = []
    start = 0
    sizes = []
    for i in range(len(groups)-1):
        sizes.append(random.randint(120, 135))
    sizes.append(5000 - sum(sizes))

    for i, group in enumerate(groups):
        size = sizes[i]
        print(f"{group}: size={size}, start={start}")
        chunk = students[start : start + size] 
        
        result.append({
            "group_id": group,
            "size": len(chunk),
            "students": [s["matriculation"] for s in chunk]
        })
        
        start = start + size  # To move forward, like keeping a count were the last groups last student number

    # For smaller rooms we may need smaller groups(Orientations, tutorialas etc.,) 
    for g in result[:10]:
        tut = {
            "group_id": g["group_id"] + "-TUT",
            "size": 65,
            "students": g["students"][:65]
        }
        result.append(tut)

    # ELectives
    all_stds = [s["matriculation"] for s in students]
    for i in range(1, 6):
        elctv = {
            "group_id": f"ELEC-0{i}",
            "size": 22,
            "students": random.sample(all_stds, 22)
        }
        result.append(elctv)
    
    print(f"Total groups: {len(result)}")
    print(f"Total students: {sum(g['size'] for g in result)}")
    print(f"Last group size: {sizes[-1]}")
    print(f"Sum of all sizes: {sum(sizes)}")

    # print(result[1])
    return result


# To save these generated data to a json file called "constraints.json"
def save_json(stds, grps, profs, rooms):

    data = {
        "students": stds,
        "groups": grps,
        "professors": profs,
        "rooms": rooms
    }

    with open("data/constraints.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("constraints.json saved! in the folder data")


if __name__ == "__main__":
    
    stds = std_gen()
    grps = grp_assgn()
    profs = gen_prfs()
    rooms = gen_rooms()
    save_json(stds, grps, profs, rooms)




