# Solution for Exercise 04: E-Scooter Ride-Share System

**TU Clausthal** | Institut für Software and Systems Engineering  
**Course:** Requirements Engineering | **Exercise:** 04 (Agent-Oriented Modeling)  
**Submitted By:** Nikunj | **Date:** 11.01.2026

---

## 1. Agents and Roles

| Agent | Role | Description |
|-------|------|-------------|
| Commuter (Human) | Commuter Role | Handles user-side processes: registration, scooter reservation, riding, and payment authorization |
| E-Scooter (Hardware) | Fleet Manager Role | Controls physical vehicle state (lock/unlock), reports real-time status and GPS location |
| Backend System (Software) | Payment Processor Role | Manages account verification, fee computation, and secure financial transactions |

---

## 2. Design Rationale

### Three-Agent Decomposition
Separating human (Commuter), hardware (E-Scooter), and software (Backend) agents follows the *separation of concerns* principle, enabling independent development and deployment of each system component.

### Time-Based Pricing Choice
Selected over distance-based due to:
1. User comprehension simplicity
2. Hardware reliability (GPS accuracy issues)
3. Fairness (prevents gaming via circular routes)

---

## 3. Goals

### Functional Goals

| ID | Goal | Description |
|----|------|-------------|
| FG-01 | Registration | Allow new commuters to register with identity and payment validation |
| FG-02 | Reservation | Enable locating and reserving idle scooters |
| FG-03 | Commute | Allow unlocking and riding the reserved scooter |
| FG-04 | End Ride | Detect ride termination and lock scooter automatically |
| FG-05 | Payment | Calculate and debit fees without manual intervention |

### Quality Goals

| ID | Goal | Description |
|----|------|-------------|
| QG-01 | Data Accuracy | Real-time scooter status synchronization |
| QG-02 | Billing Precision | Accurate fee calculation based on exact duration |
| QG-03 | Security | Encrypted storage of payment credentials |

---

## 4. Ride Cost Computation

### Formula

```
TotalFee = UnlockFee + (Duration_minutes × Rate_per_min)
```

### Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| UnlockFee | Fixed starting fee | €1.00 |
| Duration | Time from unlock to end ride (rounded up) | 15 minutes |
| Rate | Per-minute usage charge | €0.20 |

**Example:** A 15-minute ride costs €1.00 + (15 × €0.20) = **€4.00**

---

## 5. Behavioral Interface Model (BIM)

The BIM illustrates the complete interaction workflow, **including error recovery paths**.

### Happy Path

1. Registration → Account creation
2. Reservation → Scooter selection
3. Unlock → Motor activation
4. Commute → Travel period
5. End Ride → Vehicle lock
6. Payment → Fee deduction

### Error Handling

| Error State | Trigger | Recovery |
|-------------|---------|----------|
| ReservationTimeout | User doesn't unlock within 10 min | Scooter released, no charge |
| PaymentFailed | Insufficient funds / card declined | Retry (max 3×) → Suspension |

### BIM State Diagram

```mermaid
stateDiagram-v2
    [*] --> Unregistered
    
    Unregistered --> Registering: Submit Registration
    Registering --> Registered: Validation Success
    Registering --> Unregistered: Validation Failed
    
    Registered --> SearchingScooter: Find Scooter
    SearchingScooter --> ScooterReserved: Reserve Scooter
    SearchingScooter --> Registered: No Scooter Available
    
    ScooterReserved --> ScooterUnlocked: Unlock Scooter
    ScooterReserved --> Registered: Reservation Timeout (10 min)
    
    ScooterUnlocked --> Riding: Start Ride
    Riding --> RideEnded: End Ride
    
    RideEnded --> PaymentProcessing: Calculate Fee
    PaymentProcessing --> PaymentComplete: Payment Success
    PaymentProcessing --> PaymentFailed: Payment Failed
    
    PaymentFailed --> PaymentProcessing: Retry Payment
    PaymentFailed --> AccountSuspended: Max Retries (3x)
    
    PaymentComplete --> Registered: Ready for Next Ride
    AccountSuspended --> [*]
```

---

## 6. Goal Hierarchy Diagram (Enhanced 4-Level Model)

The goal hierarchy has been **rebalanced** to distribute complexity evenly:

- **Level 1 (Blue):** Main Goal – Manage E-Scooter Ride Sharing
- **Level 2 (Green):** Four Sub-Goals:
  - SG-1: Manage User Registration
  - SG-2: Manage Scooter Reservations
  - SG-3: Manage Active Rides
  - SG-4: Manage Payment Processing
- **Level 3 (Yellow/Light Green):** Leaf Goals (5 Functional + 3 Quality)

### Hierarchy Balance
Splitting "Ride Operations" into Reservations (SG-2) and Active Rides (SG-3) creates clearer separation of concerns and prevents one sub-goal from dominating the model.

### Goal Hierarchy Diagram

```mermaid
graph TD
    subgraph Level1["Level 1 - Main Goal"]
        MG["🎯 Manage E-Scooter Ride Sharing"]
    end
    
    subgraph Level2["Level 2 - Sub-Goals"]
        SG1["📝 SG-1: Manage User Registration"]
        SG2["🔍 SG-2: Manage Scooter Reservations"]
        SG3["🛴 SG-3: Manage Active Rides"]
        SG4["💳 SG-4: Manage Payment Processing"]
    end
    
    subgraph Level3["Level 3 - Functional Goals"]
        FG1["FG-01: Registration"]
        FG2["FG-02: Reservation"]
        FG3["FG-03: Commute"]
        FG4["FG-04: End Ride"]
        FG5["FG-05: Payment"]
    end
    
    subgraph Level3Q["Level 3 - Quality Goals"]
        QG1["QG-01: Data Accuracy"]
        QG2["QG-02: Billing Precision"]
        QG3["QG-03: Security"]
    end
    
    MG --> SG1
    MG --> SG2
    MG --> SG3
    MG --> SG4
    
    SG1 --> FG1
    SG1 --> QG3
    
    SG2 --> FG2
    SG2 --> QG1
    
    SG3 --> FG3
    SG3 --> FG4
    
    SG4 --> FG5
    SG4 --> QG2
    
    style MG fill:#4285f4,stroke:#333,color:#fff
    style SG1 fill:#34a853,stroke:#333,color:#fff
    style SG2 fill:#34a853,stroke:#333,color:#fff
    style SG3 fill:#34a853,stroke:#333,color:#fff
    style SG4 fill:#34a853,stroke:#333,color:#fff
    style FG1 fill:#fbbc04,stroke:#333
    style FG2 fill:#fbbc04,stroke:#333
    style FG3 fill:#fbbc04,stroke:#333
    style FG4 fill:#fbbc04,stroke:#333
    style FG5 fill:#fbbc04,stroke:#333
    style QG1 fill:#ea4335,stroke:#333,color:#fff
    style QG2 fill:#ea4335,stroke:#333,color:#fff
    style QG3 fill:#ea4335,stroke:#333,color:#fff
```

---

## Summary

This solution provides a comprehensive Agent-Oriented Model for the E-Scooter Ride-Share System, covering:

1. **Agent identification** with clear role separation
2. **Goal decomposition** into functional and quality goals
3. **Cost computation** with transparent pricing formula
4. **Behavioral modeling** with state diagrams including error handling
5. **Goal hierarchy** with balanced 4-level structure