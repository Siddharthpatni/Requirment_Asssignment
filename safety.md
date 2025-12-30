# Exam Study Notes: Software for Safety-Critical Autonomic Systems

> Comprehensive Guide Based on Lecture Slides & Exam Structure

---

## 🏗️ Topic 1: Technical Reliability (Exam Task 1)

**Source:** SsaS-part1.pdf

### 1.1 Mathematical Foundations

**Reliability Function $R(t)$:** Probability of no failure up to time $t$.

$$R(t) = e^{-\lambda t}$$

*(Where $\lambda$ is the constant failure rate).*

**Failure Probability $F(t)$:**

$$F(t) = 1 - R(t) = 1 - e^{-\lambda t}$$

**Mean Time To Failure (MTTF):**

$$MTTF = \int_{0}^{\infty} R(t) dt = \frac{1}{\lambda}$$

**Availability ($A_{\infty}$):**

The probability that a system is working at any random time.

$$A_{\infty} = \frac{MTBF}{MTBF + MTTR} = \frac{\mu}{\mu + \lambda}$$

- **MTBF** (Mean Time Between Failures): $1/\lambda$
- **MTTR** (Mean Time To Repair): $1/\mu$

#### Diagram: The Bathtub Curve (Failure Rate over Time)

```
Failure Rate (λ)
   ^
   |  Early Failures      Random Failures (Useful Life)      Wear-out
   |  (Decreasing)           (Constant λ)                  (Increasing)
   | \                                                       /
   |  \                                                     /
   |   \___________________________________________________/
   +------------------------------------------------------------> Time (t)
```

---

### 1.2 Reliability Block Diagrams (RBD)

Used to calculate the total system reliability $R_S$ based on components.

| Type | Logic | Formula | Diagram |
|------|-------|---------|---------|
| **Series** | AND (All must work) | $R_S = R_1 \cdot R_2 \cdot ... \cdot R_n$ | `[E1]--[E2]` |
| **Parallel** | OR (One must work) | $R_S = 1 - \prod_{i=1}^{n} (1 - R_i)$ | `[E1] // [E2]` |

#### RBD Examples:

**Series (AND):**
```
IN ---> [ E1 ] ---> [ E2 ] ---> OUT
```
> Fails if ANY component fails.

**Parallel (OR):**
```
       +--> [ E1 ] --+
IN --->|             |---> OUT
       +--> [ E2 ] --+
```
> Fails only if ALL components fail.

---

## 🛡️ Topic 2: Functional Safety & SIS (Exam Task 2)

**Source:** SsaS-part1.pdf

### 2.1 Key Definitions (IEC 61508)

| Term | Definition |
|------|------------|
| **EUC** | Equipment Under Control (The machine/plant) |
| **SIS** | Safety Instrumented System (The control system protecting the EUC) |
| **SIL** | Safety Integrity Level (1 to 4). Higher SIL = Lower probability of failure required |
| **Safe State** | The condition the system must enter if a failure is detected (usually Power Off / Stop) |

---

### 2.2 Operational Modes (Low vs. High Demand)

IEC 61508 defines two modes of operation for safety functions, which determine the metric used for SIL calculation.

#### 1. Low Demand Mode

- **Definition:** The safety function is demanded infrequently (frequency of demand $\le$ 1 per year).
- **Example:** Airbag system, Emergency Shutdown (ESD) in a chemical plant, Fire suppression.
- **Metric:** **PFD** (Probability of Failure on Demand).
  - This measures the probability that the system will fail to perform its function when asked.
  - Calculated as an average probability over the proof test interval ($PFD_{avg}$).

#### 2. High Demand / Continuous Mode

- **Definition:** The safety function is demanded frequently (frequency of demand > 1 per year) or operates continuously.
- **Example:** Speed control of a turbine, Dynamic stability control in a car, Continuous level monitoring.
- **Metric:** **PFH** (Probability of Failure per Hour).
  - This measures the rate of dangerous failures per hour (frequency).

#### SIL Target Failure Measures

| SIL Level | Low Demand (PFD) | High Demand (PFH) |
|-----------|------------------|-------------------|
| **SIL 4** | $10^{-5} \le PFD < 10^{-4}$ | $10^{-9} \le PFH < 10^{-8}$ |
| **SIL 3** | $10^{-4} \le PFD < 10^{-3}$ | $10^{-8} \le PFH < 10^{-7}$ |
| **SIL 2** | $10^{-3} \le PFD < 10^{-2}$ | $10^{-7} \le PFH < 10^{-6}$ |
| **SIL 1** | $10^{-2} \le PFD < 10^{-1}$ | $10^{-6} \le PFH < 10^{-5}$ |

---

### 2.3 Failure Classification (FMEA Table)

| Failure Mode | Effect | Classification |
|--------------|--------|----------------|
| Open Circuit | Signal Loss -> Safe State (Stop) | **Safe Failure** |
| Short Circuit | Stuck "ON" -> Dangerous | **Dangerous Failure** |

**Safe Failure Fraction (SFF):**

$$SFF = \frac{\sum \lambda_S + \sum \lambda_{DD}}{\sum \lambda_{total}}$$

*(Where $\lambda_S$ = Safe Failures, $\lambda_{DD}$ = Dangerous Detected Failures).*

---

### 2.4 Hardware Fault Tolerance (HFT) & Architectures

**HFT:** The number of hardware faults a system can tolerate and still perform its safety function.

#### Common Architectures (MooN - M out of N)

| Architecture | Description | HFT | Pros | Cons |
|--------------|-------------|-----|------|------|
| **1oo1** (1 out of 1) | Single channel. System trips if the single sensor detects danger. | 0 | Lowest Cost, Simple. | No Redundancy. High PFD (Low Safety). |
| **1oo2** (1 out of 2) | Dual channel. System trips if either sensor A OR sensor B detects danger. | 1 | High Safety (Low PFD). Tolerates 1 dangerous failure. | Low Availability (High Spurious Trip Rate). |
| **2oo2** (2 out of 2) | Dual channel. System trips only if both sensor A AND sensor B detect danger. | 0 | High Availability (Low Spurious Trip Rate). | Low Safety (High PFD). Fails dangerously if one sensor fails. |
| **2oo3** (2 out of 3) | Triple channel. System trips if any 2 sensors detect danger. | 1 | Best balance of Safety (SIL 3) and Availability. | High Cost (3 sensors + complex logic). |

#### Voting Logic Diagrams

**1oo2 (Safety - OR Logic):**
```
      +----[ Sensor A ]----+
      |                    |
IN ---+                    +----( Logic: OR )---- Trip Signal
      |                    |      (Safe)
      +----[ Sensor B ]----+
```
*(Trips if A OR B sees danger)*

**2oo2 (Availability - AND Logic):**
```
      +----[ Sensor A ]----+
      |                    |
IN ---+                    +----( Logic: AND )--- Trip Signal
      |                    |      (Risky)
      +----[ Sensor B ]----+
```
*(Trips only if A AND B see danger)*

#### SIL Requirements for Type A Subsystems (Simple Devices)

| SFF | HFT = 0 | HFT = 1 | HFT = 2 |
|-----|---------|---------|---------|
| < 60% | SIL 1 | SIL 2 | SIL 3 |
| 60% - < 90% | SIL 2 | SIL 3 | SIL 4 |
| 90% - < 99% | SIL 3 | SIL 4 | SIL 4 |
| > 99% | SIL 3 | SIL 4 | SIL 4 |

---

## 🔄 Topic 3: Software Lifecycle & Process (Exam Task 3)

**Source:** SsaS-part3.pdf / SsaS-part2.pdf

### 3.1 The V-Model (IEC 61508-3)

#### Diagram: The V-Model

```
      (Specification)                         (Verification)
      
    [ Requirements ] <---------------------> [ Validation Test ]
           \                                       /
      [ Architecture ] <-----------------> [ Integration Test ]
             \                                   /
       [ System Design ] <-------------> [ System Test ]
               \                               /
         [ Module Design ] <-------> [ Module Test ]
                   \                       /
                    \                     /
                     [  Implementation   ]
```

- **Left Side:** Specification & Design.
- **Right Side:** Testing & Verification.
- **Bottom:** Coding.
- **Traceability:** Every requirement must link to code and a test case.

---

### 3.2 Verification Methods

| Method | Description |
|--------|-------------|
| **Static Analysis** | Checking code without running it (e.g., MISRA checks). |
| **Review** | Manual examination of documents/code. |
| **Walkthrough** | Informal presentation of code to peers. |
| **Formal Verification** | Mathematical proof of correctness (e.g., using CTL). |

---

### 3.3 Configuration Management (CM)

- **Purpose:** Unique identification of all items (docs, code, tools) to achieve SIL.
- **Key Concept:** "Version" vs "Revision".
- **Configuration:** A set of defined revisions.

---

## 🧪 Topic 4: Testing & Coverage (Exam Task 4)

**Source:** SsaS-part2.pdf / SsaS-part3.pdf

### 4.1 Coverage Metrics

| Metric | Description |
|--------|-------------|
| **Statement Coverage** | Has every line of code run? (Weakest). |
| **Branch/Decision Coverage** | Has every if/else taken both True and False paths? |
| **MC/DC** | Modified Condition / Decision Coverage |

#### MC/DC (Modified Condition / Decision Coverage)

- **Requirement:** Required for SIL 3/4.
- **Definition:** Each condition in a compound boolean expression must independently affect the decision.
- **N+1 Rule:** If you have N conditions, you need at least N+1 test cases.

**Example:** `if (A and B)`

| Test | A | B | Output | Purpose |
|------|---|---|--------|---------|
| 1 | 1 | 1 | 1 | Baseline |
| 2 | 0 | 1 | 0 | Proves A independent |
| 3 | 1 | 0 | 0 | Proves B independent |

---

### 4.2 State Machines (Automata)

Used to model safety logic (e.g., Emergency Stop).

#### Diagram:
```
     (Start)
        |
        v
    +--------+        (Start Pressed)       +-------+
    |  STOP  |----------------------------->| READY |
    +--------+                              +-------+
        ^                                     |   ^
        | (Safety Trip)                       |   |
        +------------------------+            |   |
                                 |            |   | (Start Pressed)
                                 |            v   |
                                 |          +-------+
                                 +----------|  RUN  |
                                            +-------+
```

- **Testing:** Requires **Transition Coverage** (testing every arrow/path in the diagram).

---

### 4.3 Control Flow Diagram (CFD)

Visualizes code logic for testing.

- **Diamond:** Decision (`if`).
- **Rectangle:** Action (`x = 1`).
- **Arrows:** Flow.

#### CFD Example:
```
        [ Start ]
            |
            v
       /--------\
      /    A?    \
      \          /
       \--------/
      /    |     \
  (Yes)    |      (No)
    v      |        v
[ x = 1 ]  |    [ x = 0 ]
    |      |        |
    +------+--------+
           |
           v
        [ End ]
```

---

### 4.4 MISRA C (Common Rules)

Safety subset for C programming.

> [!IMPORTANT]
> **Key MISRA C Rules:**
> - ❌ No dynamic memory (`malloc`, `free`).
> - ❌ No `goto`.
> - ❌ No standard I/O (`printf`, `scanf`) in production code.
> - ✅ Use fixed-width integers (`int32_t`) instead of generic (`int`).

---

## 📋 Quick Reference Summary

| Topic | Key Concepts |
|-------|--------------|
| **Reliability** | $R(t) = e^{-\lambda t}$, MTTF = $1/\lambda$, RBD (Series/Parallel) |
| **Functional Safety** | SIL 1-4, PFD/PFH, SFF, HFT, MooN architectures |
| **Software Lifecycle** | V-Model, Traceability, Configuration Management |
| **Testing** | Statement/Branch/MC/DC Coverage, State Machines, CFD |



## graph TD

## Start((Start)) --> Init[out = in]

## Init --> Dec1{in >= ALARM?}

    

## Dec1 -- Yes --> Set0[out = 0]

## Set0 --> Return((Return out))

    

## Dec1 -- No --> Dec2{in > WARN?}

    

## Dec2 -- Yes --> Inc[count++]

## Inc --> Dec3{count > MAX?}

    

## Dec3 -- Yes --> Limit[out = WARN]

## Limit --> Return

## Dec3 -- No --> Return

    

## Dec2 -- No --> Reset[count = 0]

## Reset --> Return


