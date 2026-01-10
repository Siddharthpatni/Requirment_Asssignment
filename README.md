# Requirements Engineering - TU Clausthal

**Student:** Siddharth D. Patni (sp01)  
**Course:** Requirements Engineering  
**University:** TU Clausthal

---

## Repository Structure

```
.
├── Exercise_04/           # AOM: E-Scooter Ride-Share Goal Model
│   ├── Submission/        # ⬅️ Files to upload to Moodle
│   └── ...
├── Exercise_05/           # Petri Net: File Locking with Test Arcs
│   ├── Submission/        # ⬅️ Files to upload to Moodle
│   └── ...
├── Exercise_06/           # CPN: E-Scooter Coloured Petri Net
│   ├── Submission/        # ⬅️ Files to upload to Moodle
│   └── ...
└── Helped_Exercise_04/    # Assisted work
```

---

## Exercises

### Exercise 04: Agent-Oriented Modeling (AOM)
**Deadline:** 12.01.2026  
**Folder:** [Exercise_04/](Exercise_04/)

| Submission File | Description |
|-----------------|-------------|
| `Patni_553265_Exercise04_RolesGoalsBIM.pdf` | Roles, Goals, BIM (2 pages) |
| `Patni_553265_Exercise04_GoalModel.pdf` | Goal Model Diagram |

**Contents:**
- 3 Agents: Commuter, E-Scooter, Backend Server
- 5 Functional Goals + 3 Quality Goals
- Hybrid pricing: €1.00 + €0.10/min + €0.05/km
- Complete BIM with exception handling

---

### Exercise 05: Petri Net File Locking
**Deadline:** 26.01.2026  
**Folder:** [Exercise_05/](Exercise_05/)

| Submission File | Description |
|-----------------|-------------|
| `exercise5.py` | SNAKES implementation |
| `simulation_*.png` | 9 state images |

**Contents:**
- Token-based mutual exclusion lock
- Demonstrates test arc concept
- Two concurrent processes (P1, P2)

---

### Exercise 06: E-Scooter CPN Model
**Deadline:** 26.01.2026  
**Folder:** [Exercise_06/](Exercise_06/)

| Submission File | Description |
|-----------------|-------------|
| `Solution_Exercise_06.py` | SNAKES CPN implementation |
| `sim_scooter_*.png` | 12 state images |
| `AOM_Goal_Model.pdf` | Goal hierarchy |
| `AOM_BIM.pdf` | Behavioral Interface Model |

**Contents:**
- 2 Users (with wallet tracking)
- 3 Scooters (at different stations)
- Dynamic cost calculation: €1 + (duration × €0.20)
- Error handling with guards

---

## Technologies

- Python 3.x
- SNAKES (Petri Net library)
- Graphviz (visualization)
- Puppeteer (PDF generation)
- Mermaid (diagrams)

## Running Simulations

```bash
# Exercise 05
cd Exercise_05 && python3 exercise5.py

# Exercise 06
cd Exercise_06 && python3 Solution_Exercise_06.py
```

---

**Submitted:** January 2026
