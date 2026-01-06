# Exercise 05: File Locking with Inhibitor Arcs

**TU Clausthal**  
**Institute:** Software and Systems Engineering  
**Module:** Requirements Engineering  
**Assignment:** 05 – Petri Net with Locking Mechanism  
**Author:** Siddharth D. Patni (sp01)  
**Date:** 27.12.2024

---

## 1. Problem Statement

Two processes attempt to read from and write to the same file. Without coordination, simultaneous writes cause data corruption. This exercise implements a **locking mechanism using inhibitor arcs** to ensure mutual exclusion.

---

## 2. Solution: Inhibitor Arc Locking

### How Inhibitor Arcs Work

An **inhibitor arc** blocks a transition when the connected place contains tokens—the opposite of normal arcs that require tokens to fire.

```
Normal Arc:     Transition fires WHEN place has tokens
Inhibitor Arc:  Transition BLOCKED WHEN place has tokens
```

### Implementation

- `StartWrite` transition checks the `Writing` place
- If `Writing` contains ANY token → `StartWrite` is **BLOCKED**
- Only when `Writing` is empty can a process enter the critical section

---

## 3. Petri Net Structure

### Places

| Place | Initial Tokens | Purpose |
|-------|----------------|---------|
| `Idle` | [1, 2] | Processes waiting to work |
| `Reading` | [] | Process reading file (non-critical) |
| `ReadyToWrite` | [] | Process waiting to enter critical section |
| `Writing` | [] | **CRITICAL SECTION** (max 1 process) |

### Transitions

| Transition | From → To | Description |
|------------|-----------|-------------|
| `StartRead` | Idle → Reading | Begin reading |
| `EndRead` | Reading → ReadyToWrite | Finish reading |
| `StartWrite` | ReadyToWrite → Writing | **Guarded by inhibitor arc** |
| `EndWrite` | Writing → Idle | Exit critical section |

---

## 4. Simulation Results

The simulation demonstrates the inhibitor arc blocking Process 2 while Process 1 is writing:

| Step | Image | Description |
|------|-------|-------------|
| 0 | `simulation_00_Initial.png` | Both processes idle |
| 1 | `simulation_01_P1_Reading.png` | P1 reading |
| 2 | `simulation_02_P1_ReadyToWrite.png` | P1 ready to write |
| 3 | `simulation_03_P1_Writing.png` | P1 in critical section |
| 4 | `simulation_04_P2_Reading.png` | P2 reading (concurrent) |
| 5 | `simulation_05_P2_ReadyToWrite_BLOCKED.png` | **P2 BLOCKED** (inhibitor arc) |
| 6 | `simulation_06_P1_Idle_LockReleased.png` | P1 exits, Writing empty |
| 7 | `simulation_07_P2_Writing.png` | P2 now writes |
| 8 | `simulation_08_P2_Idle_Final.png` | Both idle (complete) |

---

## 5. Key Demonstration: Step 5

At Step 5, the inhibitor arc prevents Process 2 from entering:

```
Writing place contains: [1]
INHIBITOR CHECK: Writing is NOT EMPTY -> BLOCKED!
Process 2 cannot enter StartWrite transition.
```

This proves mutual exclusion is enforced.

---

## 6. Running the Code

### Requirements
```bash
pip install snakes
brew install graphviz  # macOS
# apt install graphviz  # Linux
```

### Execute
```bash
python3 exercise5.py
```

---

## 7. Submission Files

| File | Description |
|------|-------------|
| `exercise5.py` | SNAKES CPN implementation |
| `simulation_*.png` | 9 state transition images |
| `README.md` | This documentation |
