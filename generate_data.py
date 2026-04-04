import random

def gen():

    students = []

    for i in range(1, 5001):
        
        student_i = {
            "matriculation": f"MAT-{i:05d}",
            "name": f"Student_{i}",
            "group": None
        }
    
        students.append(student_i)
        print(students)
    
    return students

def grp_assgn():

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
    
    print(groups)
    return groups



if __name__ == "__main__":
    grp_assgn()


