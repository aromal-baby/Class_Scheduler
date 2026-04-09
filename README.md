# Campus Scheduler

## Overview
A program carefully engineered to build a system where a university can easily schedule the lecture accordingly with no time slots, professors or lecture halls overlapping and minimizing the resource waste using a greesdy approach and comparing it with backtracking to make sure maintaining minimal wastage.

## Project Structure
```
campus_scheduler/
├── data/
│   └── constraints.json
├── src/
│   ├── greedy_solver.py
│   ├── graph_engine.py
│   ├── optimizer.py
│   └── backtracker.py
├── generate_data.py
├── main.py
└── README.md
```

No external dependencies required. Python >= 3.10 only.

## How to Run
```bash
python generate_data.py   # regenerate data
python main.py            # run all 4 stages
```

## Algorithm Justification

### Stage 1 — Greedy Solver
Sorts classes by enrolled students descending, places each into the first valid (time slot, room) pair. Time complexity O(C × T × R) where C=54, T=20, R=50.

### Stage 2 — Graph Colouring (Welsh-Powell)
Builds a conflict graph where nodes are classes and edges connect classes sharing a professor or student group. Welsh-Powell colours the graph so no two conflicting classes share a time slot. Time complexity O(C² + C × T).

### Stage 3 — Room Allocation
Groups classes by time slot, assigns each class the smallest available room that fits. Minimises wasted seats. Time complexity O(C × R) per slot.

### Stage 4 — Backtracking
Recursively assigns classes to (time slot, room) pairs. Backtracks when constraints are violated. Classes sorted by enrolment descending (fail-first). Worst case O((T × R)^C), pruning makes it tractable.

## Results

| Stage | Scheduled | Wasted Seats |
|---|---|---|
| Greedy | 54/54 | 1,343 |
| Graph + Room Allocation | 54/54 | 1,413 |
| Backtracking | 54/54 | 1,114 |

## Conflict Report Sample

```
  Scheduled   CLASS-002   MON-09:00   R-032   Perfect Fit
  Scheduled   CLASS-012   MON-09:00   R-038   Wasted 21 seats
  Scheduled   CLASS-016   MON-09:00   R-048   Wasted 280 seats
  Unscheduled CLASS-XXX   N/A         N/A
```

## Manual Fix Log

If classes remain unscheduled a university manager can:
1. Move a low-priority class to a different time slot
2. Split a large class into smaller sections
3. Reserve a large lecture theatre for specific modules

## Dataset

5,000 students, 300 professors, 54 classes, 50 rooms across 4 size tiers, 20 time slots (Mon-Fri, 2-hour blocks). Generated programmatically via `generate_data.py`.

## References

Welsh, D.J.A. and Powell, M.B. (1967) 'An upper bound for the chromatic number of a graph', The Computer Journal, 10(1), pp. 85-86.

Cormen, T.H. et al. (2022) Introduction to Algorithms. 4th ed. MIT Press.
