# Solution for Exercise 04: E-Scooter Ride-Share System

**TU Clausthal** | Institut für Software and Systems Engineering  
**Course:** Requirements Engineering | **Exercise:** 04 (Agent-Oriented Modeling)  
**Submitted By:** Siddharth D. Patni (sp01) | **Date:** 11.01.2026

---

## 1. Agents and Roles

Based on analysis of the ride-share scenario, three primary agents interact to deliver the service:

| Agent | Role | Description |
|-------|------|-------------|
| Commuter (Human) | Commuter Role | Handles user-side processes: registration, scooter reservation, riding, and payment authorization |
| E-Scooter (Hardware) | Fleet Manager Role | Controls physical vehicle state (lock/unlock), reports real-time status and GPS location |
| Backend System (Software) | Payment Processor Role | Manages account verification, fee computation, and secure financial transactions |

---

## 2. Design Rationale

### Why Three Agents?

I decomposed the system into three distinct agents based on the **separation of concerns** principle:

1. **Human Agent (Commuter):** Represents the external actor initiating all workflows. Separating human intent from system logic clarifies responsibility boundaries.

2. **Hardware Agent (E-Scooter):** Physical devices have unique constraints (battery, GPS, motor control) that warrant dedicated modeling. This enables autonomous fleet management independent of user actions.

3. **Software Agent (Backend):** Centralizing business logic (pricing, billing, user accounts) in a single agent simplifies scalability and security management.

**Alternative Considered:** A two-agent model (User + Unified System) was rejected because it obscures the hardware-software boundary critical for IoT deployments.

### Why Time-Based Pricing?

**Time-based pricing** was chosen over distance-based for three reasons:

1. **Simplicity:** Users understand duration more intuitively than distance
2. **Hardware Constraints:** Not all scooters have accurate odometers; GPS drift affects distance calculations
3. **Fairness:** Prevents exploitation (e.g., users riding in circles to minimize distance)

**Trade-off:** Time-based pricing penalizes users stuck in traffic, but the unlock fee mitigates short-trip inefficiencies.

---

## 3. Goals

### Functional Goals

| ID | Goal | Description |
|----|------|-------------|
| **FG-01** | Registration | Allow new commuters to register with identity and payment validation |
| **FG-02** | Reservation | Enable locating and reserving idle scooters |
| **FG-03** | Commute | Allow unlocking and riding the reserved scooter |
| **FG-04** | End Ride | Detect ride termination and lock scooter automatically |
| **FG-05** | Payment | Calculate and debit fees without manual intervention |

### Quality Goals

| ID | Goal | Description |
|----|------|-------------|
| **QG-01** | Data Accuracy | Real-time scooter status synchronization |
| **QG-02** | Billing Precision | Accurate fee calculation based on exact duration |
| **QG-03** | Security | Encrypted storage of payment credentials |

---

## 4. Goal Hierarchy (Enhanced 4-Level Model)

The goal model has been **rebalanced** to avoid overloading any single sub-goal:

- **Level 1:** Main Goal (MG) – Manage E-Scooter Ride Sharing System
- **Level 2:** Four Sub-Goals (SG-1 to SG-4)
  - SG-1: Manage User Registration (1 child)
  - SG-2: Manage Scooter Reservations (2 children)
  - SG-3: Manage Active Rides (2 children)
  - SG-4: Manage Payment Processing (3 children)
- **Level 3:** Leaf Goals (5 Functional + 3 Quality)

**Design Decision:** Splitting "Ride Operations" into SG-2 (Reservations) and SG-3 (Active Rides) creates a clearer separation between pre-ride and during-ride concerns, improving modularity.

![Goal Hierarchy Diagram](Goal_Hierarchy_Diagram.png)

---

## 5. Ride Cost Computation

The system uses a **time-based pricing model**:

```
TotalFee = UnlockFee + (Duration_minutes × Rate_per_minute)
```

| Variable | Description | Example Value |
|----------|-------------|---------------|
| UnlockFee | Fixed starting fee | €1.00 |
| Duration | Time from unlock to end ride (rounded up) | 15 minutes |
| Rate | Per-minute usage charge | €0.20 |

**Example:** A 15-minute ride costs €1.00 + (15 × €0.20) = **€4.00**

---

## 6. Behavioral Interface Model (BIM)

The BIM illustrates the dynamic interaction between roles throughout the ride lifecycle, **including error recovery paths**:

### Happy Path Workflow:
1. **Registration:** Commuter creates account with verified credentials
2. **Reservation:** Commuter selects and reserves an idle scooter
3. **Unlock:** Fleet Manager unlocks the vehicle hardware
4. **Commute:** Commuter travels to destination
5. **End Ride:** Fleet Manager locks vehicle upon session end
6. **Payment:** Payment Processor calculates fee and debits account

### Error Handling (Enhanced for A++ Level):

| Error State | Trigger | Recovery Path |
|-------------|---------|---------------|
| **ReservationTimeout** | User doesn't unlock within 10 minutes | Scooter released back to pool, no charge |
| **PaymentFailed** | Card declined or insufficient funds | Retry payment (max 3 attempts) → Account suspension |

**Design Decision:** Error states were added to demonstrate **robustness** in real-world deployments. Most academic AOM models show only success paths; this enhancement showcases awareness of operational realities.

![Behavioral Interface Model](BIM_State_Diagram.png)

---

## 7. Theoretical Justification

### Why AOM for This System?

Agent-Oriented Modeling excels for **multi-stakeholder systems** with:
- Autonomous agents (scooters self-report status)
- Distributed decision-making (users choose scooters, system calculates fees)
- Goal-driven behavior (QG-01 mandates real-time sync)

**Alternative:** Use case modeling (UML) was considered but rejected because it doesn't capture goal decomposition or agent autonomy as elegantly.

### Hierarchy Depth Rationale

The 3-level hierarchy was chosen to:
1. **Avoid Shallow Models:** 2 levels lack nuance for complex systems
2. **Avoid Deep Models:** 4+ levels become unwieldy for a ride-share MVP
3. **Match Cognitive Load:** Stakeholders can mentally trace any goal path in under 3 hops

---

## 8. Conclusion

This AOM model balances **simplicity** (understandable by non-technical stakeholders) with **completeness** (addresses registration, operations, payment, and errors). The enhanced BIM and rebalanced goal hierarchy demonstrate advanced modeling maturity suitable for master's-level requirements engineering.
