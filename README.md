# Requirements Engineering - TU Clausthal

**Student:** Siddharth D. Patni (sp01)  
**Course:** Requirements Engineering  
**Department:** Institut für Software and Systems Engineering

## Contents

This repository contains assignments and exercises for the Requirements Engineering course, organized into the following folders:

---

### Exercise 04: E-Scooter Ride-Share System (Agent-Oriented Modeling)
- **Folder:** [Exercise_04/](Exercise_04/)
- **File:** [Solution_Exercise_04_Goal_Model.md](Exercise_04/Solution_Exercise_04_Goal_Model.md)
- **Description:** Agent-oriented modeling solution including agents/roles identification, functional and quality goals, pricing model, and behavioral interface model (BIM) for an E-Scooter ride-sharing system.

---

### Exercise 05: Petri Net - File Locking Mechanism
- **Folder:** [Exercise_05/](Exercise_05/)
- **File:** [exercise5.py](Exercise_05/exercise5.py)
- **Description:** Python implementation of a Petri Net modeling a file locking mechanism using inhibitor arcs. Simulates concurrent read/write access with proper locking semantics.
- **Simulation Results:** PNG images showing different states of the Petri Net simulation (Initial state, reading, writing, blocking scenarios, etc.)

---

### Exercise 06: E-Scooter CPN Model
- **Folder:** [Exercise_06/](Exercise_06/)
- **File:** [Solution_Exercise_06.py](Exercise_06/Solution_Exercise_06.py)
- **Description:** Coloured Petri Net (CPN) implementation for the E-Scooter ride-share system. Models the complete workflow including commuter/scooter pools, reservations, rides, payments, and billing history.
- **Simulation Results:** PNG images showing each step of the ride-share process.

---

## Technologies Used

- Python 3.x
- SNAKES library (Petri Net modeling)
- Graphviz (visualization)
- Mermaid (diagrams in markdown)

## Running the Simulations

### Exercise 05 - File Locking
```bash
cd Exercise_05
python3 exercise5.py
```

### Exercise 06 - E-Scooter CPN
```bash
cd Exercise_06
python3 Solution_Exercise_06.py
```

Both simulations generate PNG images showing the state transitions.

---

**Submitted:** December 2024
