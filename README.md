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

## How to Run
```bash
python generate_data.py   # regenerate data
python main.py            # run all 4 stages
```

## Algorithm Justification

###
