# Exercise 05 Solution: Concurrent File Access via Petri Nets

**TU Clausthal**  
**Institute:** Software and Systems Engineering  
**Module:** Requirements Engineering  
**Assignment:** 05 – Petri Net Modeling  
**Author:** Siddharth D. Patni (sp01)  
**Submission Date:** 27.12.2024

---

## 1. Problem Context

When multiple programs attempt to modify the same file, data corruption becomes inevitable without coordination. This exercise models a **mutual exclusion mechanism** using Petri Nets—a classic concurrency control pattern found in database systems and operating system kernels.

The core challenge: permit simultaneous reads (non-destructive operations) while enforcing exclusive access during writes (destructive operations).

---

## 2. Net Architecture

I designed the Petri Net with five places representing distinct program states, connected by four transitions governing state changes.

### State Places

| Place Name | Starting Tokens | Meaning |
|------------|-----------------|---------|
| `Idle` | Two process IDs: [1, 2] | Programs waiting to begin work |
| `Reading` | Empty | Programs currently reading file contents |
| `ReadyToWrite` | Empty | Programs queued to enter write mode |
| `Writing` | Empty | Single program performing write operation |
| `Lock` | One token: ['available'] | Semaphore controlling write access |

### Transition Rules

| Transition | What It Does |
|------------|--------------|
| `StartRead` | Moves a process from Idle into Reading mode |
| `EndRead` | Moves a process from Reading into the write queue |
| `StartWrite` | Consumes the lock token, moves process into Writing |
| `EndWrite` | Returns the lock token, moves process back to Idle |

---

## 3. How the Lock Prevents Conflicts

The single token in the `Lock` place acts as a gatekeeper. Here's the logic:

1. A process in `ReadyToWrite` can only fire `StartWrite` if the Lock contains a token
2. Firing `StartWrite` removes the token—no other process can now enter `Writing`
3. When `EndWrite` fires, the token reappears, allowing another queued process to proceed

This pattern guarantees **at most one writer at any instant**, even with unlimited readers.

---

## 4. Simulation Walkthrough

Running the Python script produces nine snapshots demonstrating the mechanism:

| Snapshot | System State |
|----------|--------------|
| `simulation_00_Initial.png` | Both processes idle, lock token present |
| `simulation_01_P1_Reading.png` | Process 1 reading (non-exclusive) |
| `simulation_02_P1_ReadyToWrite.png` | Process 1 finished reading, waiting for lock |
| `simulation_03_P1_Writing.png` | Process 1 acquired lock, now writing |
| `simulation_04_P2_Reading.png` | Process 2 reading while P1 writes (allowed!) |
| `simulation_05_P2_ReadyToWrite_BLOCKED.png` | Process 2 wants to write but lock is held |
| `simulation_06_P1_Idle_LockReleased.png` | Process 1 released lock, returned to idle |
| `simulation_07_P2_Writing.png` | Process 2 acquired the now-free lock |
| `simulation_08_P2_Idle_Final.png` | Both processes back to idle state |

---

## 5. Execution Instructions

### Dependencies
```bash
pip install snakes
brew install graphviz  # On macOS
# apt install graphviz  # On Ubuntu/Debian
```

### Running the Model
```bash
cd Exercise_05
python exercise5.py
```

### Expected Console Output
```
[*] Net Created. Generating State Images...
    Saved state: simulation_00_Initial.png
[-] Process 1 starts reading...
...
    [SUCCESS] 'StartWrite' has no valid modes. Lock is working!
...
[*] Simulation Complete.
[*] Generated 9 PNG images showing the state transitions.
```

---

## 6. Deliverables Checklist

- ✅ `exercise5.py` – Complete Petri Net implementation
- ✅ `simulation_*.png` – Nine state transition visualizations
- ✅ `README.md` – This explanatory document
