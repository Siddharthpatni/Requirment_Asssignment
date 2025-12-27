# Exercise 05: Petri Net - File Locking Mechanism

**TU Clausthal**  
**Department:** Institut für Software and Systems Engineering  
**Course:** Requirements Engineering  
**Exercise:** 05 (Petri Net with Locking)  
**Submitted By:** Siddharth D. Patni (sp01)  
**Date:** 27.12.2024

---

## 1. Overview

This exercise implements a **Petri Net** that models a **file locking mechanism** for concurrent read/write access. The model ensures mutual exclusion - only one process can write at a time while multiple processes can read concurrently.

---

## 2. Model Structure

### Places

| Place | Initial Tokens | Description |
|-------|----------------|-------------|
| `Idle` | [1, 2] | Processes waiting to work |
| `Reading` | [] | Processes currently reading |
| `ReadyToWrite` | [] | Processes waiting to acquire write lock |
| `Writing` | [] | Process in critical section (max 1) |
| `Lock` | ['available'] | Write lock token |

### Transitions

| Transition | Description |
|------------|-------------|
| `StartRead` | Process moves from Idle → Reading |
| `EndRead` | Process moves from Reading → ReadyToWrite |
| `StartWrite` | Process acquires lock, moves to Writing |
| `EndWrite` | Process releases lock, returns to Idle |

---

## 3. Locking Mechanism

The **Lock** place contains a single token (`'available'`). When a process wants to write:

1. It must consume the lock token from `Lock` place
2. Only one process can hold the lock at a time
3. When writing finishes, the lock token is returned

This ensures **mutual exclusion** in the writing phase.

---

## 4. Simulation Output

The simulation generates 9 PNG images showing state transitions:

| Image | State |
|-------|-------|
| `simulation_00_Initial.png` | Initial: Both processes idle, lock available |
| `simulation_01_P1_Reading.png` | Process 1 reading |
| `simulation_02_P1_ReadyToWrite.png` | Process 1 ready to write |
| `simulation_03_P1_Writing.png` | Process 1 writing (lock acquired) |
| `simulation_04_P2_Reading.png` | Process 2 reading concurrently |
| `simulation_05_P2_ReadyToWrite_BLOCKED.png` | Process 2 blocked - no lock available |
| `simulation_06_P1_Idle_LockReleased.png` | Process 1 done, lock released |
| `simulation_07_P2_Writing.png` | Process 2 now writing |
| `simulation_08_P2_Idle_Final.png` | Final state: both idle |

---

## 5. Running the Simulation

### Prerequisites
```bash
pip install snakes
brew install graphviz  # macOS
# or: apt install graphviz  # Linux
```

### Execute
```bash
python exercise5.py
```

### Expected Output
```
[*] Net Created. Generating State Images...
    Saved state: simulation_00_Initial.png
[-] Process 1 starts reading...
    Saved state: simulation_01_P1_Reading.png
...
    [SUCCESS] 'StartWrite' has no valid modes. Lock is working!
...
[*] Simulation Complete.
[*] Generated 9 PNG images showing the state transitions.
```

---

## 6. Files Included

- `exercise5.py` - Python Petri Net implementation
- `simulation_*.png` - Generated state diagrams (9 images)
- `README.md` - This documentation
