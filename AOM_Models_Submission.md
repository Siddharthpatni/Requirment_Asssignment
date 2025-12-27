# AOM Models Submission

**Student:** Siddharth D. Patni (sp01)  
**Course:** Requirements Engineering  
**Department:** Institut für Software and Systems Engineering, TU Clausthal

---

## Overview

This repository contains Agent-Oriented Modeling (AOM) solutions for the Requirements Engineering course, covering Exercises 04, 05, and 06.

## Exercise Summaries

### Exercise 04: E-Scooter Ride-Share Goal Model
- **Location:** [Exercise_04/](Exercise_04/)
- **Contents:** Agent-oriented modeling solution with agents/roles identification, functional and quality goals, pricing model, and behavioral interface model (BIM).

### Exercise 05: Petri Net - File Locking Mechanism
- **Location:** [Exercise_05/](Exercise_05/)
- **Contents:** Petri Net implementation modeling concurrent file access with inhibitor arcs. Demonstrates read/write locking semantics with simulation outputs.

### Exercise 06: E-Scooter CPN Model
- **Location:** [Exercise_06/](Exercise_06/)
- **Contents:** Coloured Petri Net (CPN) implementation modeling the complete E-Scooter ride-share system workflow including:
  - Commuter and Scooter pools
  - Reservation, ride start/end transitions
  - Payment processing
  - Billing history

---

## Running the Simulations

### Exercise 05
```bash
cd Exercise_05
python3 exercise5.py
```

### Exercise 06
```bash
cd Exercise_06
python3 Solution_Exercise_06.py
```

Both simulations generate PNG images showing the state transitions.
