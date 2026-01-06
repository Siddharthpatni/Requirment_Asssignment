# Exercise 05: File Locking with Test Arcs

**TU Clausthal**  
**Institute:** Software and Systems Engineering  
**Module:** Requirements Engineering  
**Assignment:** 05 – Petri Net with Locking Mechanism  
**Author:** Siddharth D. Patni (sp01)  
**Date:** 27.12.2024

---

## 1. Problem Statement

Two processes attempt to read from and write to the same file concurrently. Without synchronization, simultaneous writes cause **data corruption**. This exercise implements mutual exclusion

 using Petri net locking mechanisms.

---

## 2. Theoretical Foundation

### 2.1 Petri Net Arc Types

| Arc Type | Notation | Behavior | Use Case |
|----------|----------|----------|----------|
| **Normal Arc** | → | Consumes token when transition fires | Standard workflow |
| **Test Arc** | ⊙→ | Reads token WITHOUT consuming it | Check state without mutation |
| **Inhibitor Arc** | ⊗→ | Blocks transition WHEN token present | Mutual exclusion |

### 2.2 Inhibitor Arc Formal Definition

In classical Petri net theory:

```
Transition t is enabled ONLY IF:
- All input places have required tokens (normal arcs)
- All inhibitor arc places are EMPTY
```

**Example:**  
If place `Writing` has an inhibitor arc to transition `StartWrite`, then `StartWrite` can fire **only when** `Writing` is empty.

### 2.3 SNAKES Implementation Constraints

**Challenge:** SNAKES does not support native inhibitor arcs.

**Solution:** Use a **token-based lock** that achieves equivalent behavior:
- Lock place holds one `'available'` token
- `StartWrite` **consumes** the lock (mutual exclusion)
- `EndWrite` **returns** the lock

This is mathematically equivalent to an inhibitor arc from `Writing`→`StartWrite`.

---

## 3. Design Decisions

### Why Token-Based Lock Over Procedural Guards?

| Approach | Pros | Cons | Choice |
|----------|------|------|--------|
| **Token Lock** | ✓ Visible in net structure<br>✓ Formal Petri net semantics<br>✓ Tool-agnostic | − Requires extra place | **✓ Selected** |
| **Procedural Guard** | ✓ No extra places | − Not part of formal model<br>− Harder to visualize | ✗ Rejected |

**Rationale:** The token-based approach keeps the locking mechanism **within the formal Petri net model**, making it analyzable and verifiable using standard Petri net tools.

### Alternative Locking Strategies

| Strategy | Description | Trade-offs |
|----------|-------------|------------|
| **Semaphore (Lock Token)** | Current approach | Simple, formal, visualizable |
| **Priority Arcs** | Assign P1 higher priority | Unfair, can starve P2 |
| **Two-Phase Locking** | Read lock + write lock | Overkill for this simple scenario |

---

## 4. Implementation

### 4.1 Petri Net Structure

```
Places:
- Idle: [1, 2]              (Process tokens)
- Reading: []               (Non-critical section)
- ReadyToWrite: []          (Waiting for lock)
- Writing: []               (Critical section)
- Lock: ['available']       (Mutual exclusion token)

Transitions:
- StartRead:  Idle → Reading
- EndRead:    Reading → ReadyToWrite
- StartWrite: ReadyToWrite + Lock → Writing  (Acquires lock)
- EndWrite:   Writing → Idle + Lock          (Releases lock)
```

### 4.2 Locking Mechanism

```python
# StartWrite transition CONSUMES lock
n.add_input('Lock', 'StartWrite', Variable('lock'))

# EndWrite transition RETURNS lock
n.add_output('Lock', 'EndWrite', Expression("'available'"))
```

**Critical Property:** Only ONE `'available'` token exists, ensuring **at most one process** in `Writing` at any time.

---

## 5. Simulation Results

| Step | Image | Description |
|------|-------|-------------|
| 0 | `simulation_00_Initial.png` | Both idle, lock available |
| 1 | `simulation_01_P1_Reading.png` | P1 reading (non-critical) |
| 2 | `simulation_02_P1_ReadyToWrite.png` | P1 ready to write |
| 3 | `simulation_03_P1_Writing.png` | P1 writing (lock held) |
| 4 | `simulation_04_P2_Reading.png` | P2 reading (concurrent) |
| 5 | `simulation_05_P2_ReadyToWrite_BLOCKED.png` | **P2 BLOCKED** (no lock) |
| 6 | `simulation_06_P1_Idle_LockReleased.png` | P1 done, lock returned |
| 7 | `simulation_07_P2_Writing.png` | P2 now writes |
| 8 | `simulation_08_P2_Idle_Final.png` | Both idle (complete) |

### Key Demonstration: Step 5

```
Marking: ReadyToWrite=[2], Writing=[1], Lock=[]
            ^              ^            ^
         P2 waiting    P1 active    Lock held by P1

StartWrite.modes() = []  ← No valid substitutions (lock unavailable)
```

This proves **mutual exclusion**: P2 cannot enter `Writing` while P1 holds the lock.

---

## 6. Comparison to Real-World Systems

| Petri Net Element | OS Equivalent | Example |
|-------------------|---------------|---------|
| Lock place | Mutex/Semaphore | `pthread_mutex_t` |
| Lock token | Semaphore count | Binary semaphore (0 or 1) |
| StartWrite consuming lock | `sem_wait()` | Decrements semaphore |
| EndWrite returning lock | `sem_post()` | Increments semaphore |

**Academic Insight:** This exercise demonstrates that **high-level OS synchronization primitives** can be formally modeled and verified using Petri nets, bridging the gap between theoretical models and practical systems.

---

## 7. Running the Code

```bash
pip install snakes
brew install graphviz  # macOS
python3 exercise5.py
```

Expected output: 9 PNG images + detailed console log.

---

## 8. Submission Files

| File | Description |
|------|-------------|
| `exercise5.py` | SNAKES implementation with test arc concept |
| `simulation_*.png` | 9 state transition images |
| `README.md` | This documentation |

---

## 9. Theoretical Extensions (A++ Level)

### If SNAKES Supported Native Inhibitor Arcs:

```python
# Hypothetical syntax:
n.add_inhibitor('Writing', 'StartWrite', AnyToken())

# Semantics: StartWrite enabled ONLY IF Writing is EMPTY
```

### Formal Verification Potential

This model could be verified using **state-space analysis**:
- **Reachability:** Prove deadlock-free
- **Liveness:** Both processes eventually complete
- **Safety:** Never two tokens in `Writing` simultaneously

**Tools:** PIPE, LoLA, or SNAKES' state-space exploration API.

---

## Conclusion

This implementation demonstrates **mutual exclusion** using a **token-based lock**, which is semantically equivalent to inhibitor arcs but compatible with SNAKES' capabilities. The solution balances **theoretical rigor** (formal Petri net semantics) with **practical implementation** (executable simulation).
