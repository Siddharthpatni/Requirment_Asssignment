# Exercise 04 Solution: Urban Mobility E-Scooter Platform

**TU Clausthal**  
**Institute:** Software and Systems Engineering  
**Module:** Requirements Engineering  
**Assignment:** 04 – Agent-Oriented Modeling  
**Author:** Siddharth D. Patni (sp01)  
**Submission Date:** 11.01.2026

---

## 1. System Actors and Their Responsibilities

After analyzing the ride-share scenario, I identified three distinct actors that collaborate to deliver the service. Each actor plays a specific part in the overall workflow.

| Actor Type | Role Name | Core Responsibilities |
|------------|-----------|----------------------|
| End User (Human) | Rider | Initiates the rental journey: signs up, picks a vehicle, travels, and approves the charge |
| Physical Device (IoT) | Vehicle Controller | Governs hardware functions—motor engagement, GPS tracking, and availability broadcasting |
| Cloud Service (Software) | Billing Engine | Orchestrates account validation, duration tracking, fare determination, and fund transfer |

---

## 2. System Objectives

I structured the objectives into two categories: capabilities the platform must provide (functional) and performance standards it must meet (quality-focused).

### Functional Objectives

- **FO-01 (Onboarding):** New riders complete a signup flow where their credentials and card details undergo verification before activation.
- **FO-02 (Vehicle Claim):** Riders browse nearby vehicles via the app map, select one, and claim it—instantly marking it unavailable to others.
- **FO-03 (Trip Execution):** Once claimed, the vehicle motor activates, allowing the rider to travel freely until reaching their stop.
- **FO-04 (Trip Termination):** Parking the vehicle and tapping "End" triggers an automatic motor shutdown and GPS-based location update.
- **FO-05 (Automated Billing):** The platform computes travel charges and processes the transaction without requiring manual input.

### Quality Objectives

- **QO-01 (Live Inventory):** Vehicle availability reflects real-world status within seconds to prevent double-bookings.
- **QO-02 (Accurate Charges):** Fare calculations use server-recorded timestamps to ensure riders pay exactly what they owe.
- **QO-03 (Data Protection):** Sensitive payment credentials remain encrypted and are accessed only during the debit operation.

### Objective Hierarchy (3 Tiers)

The diagram below illustrates how the main platform goal decomposes into sub-objectives and finally into specific leaf-level tasks:

```mermaid
graph TD
    %% Tier 1: Platform Goal
    PG["<b>Platform Goal:<br/>Operate Urban Scooter Rental</b>"]
    
    %% Tier 2: Sub-Objectives
    SO1["<b>SO-1: Enable<br/>User Onboarding</b>"]
    SO2["<b>SO-2: Facilitate<br/>Trip Lifecycle</b>"]
    SO3["<b>SO-3: Execute<br/>Financial Settlement</b>"]
    
    %% Tier 3: Leaf Objectives - Functional
    FO01["FO-01: Verify<br/>Rider Credentials"]
    FO02["FO-02: Allow<br/>Vehicle Claiming"]
    FO03["FO-03: Activate<br/>Motor for Travel"]
    FO04["FO-04: Detect Stop<br/>& Secure Vehicle"]
    FO05["FO-05: Compute Fare<br/>& Charge Card"]
    
    %% Tier 3: Leaf Objectives - Quality
    QO01["QO-01: Sync<br/>Availability Live"]
    QO02["QO-02: Ensure<br/>Billing Accuracy"]
    QO03["QO-03: Encrypt<br/>Payment Data"]
    
    %% Connections Tier 1 to 2
    PG --> SO1
    PG --> SO2
    PG --> SO3
    
    %% Connections Tier 2 to 3
    SO1 --> FO01
    SO2 --> FO02
    SO2 --> FO03
    SO2 --> FO04
    SO2 --> QO01
    SO3 --> FO05
    SO3 --> QO02
    SO3 --> QO03
    
    %% Visual Styling
    style PG fill:#2c3e50,stroke:#1a252f,color:#ecf0f1
    style SO1 fill:#27ae60,stroke:#1e8449,color:#fff
    style SO2 fill:#27ae60,stroke:#1e8449,color:#fff
    style SO3 fill:#27ae60,stroke:#1e8449,color:#fff
    style FO01 fill:#f39c12,stroke:#d68910,color:#000
    style FO02 fill:#f39c12,stroke:#d68910,color:#000
    style FO03 fill:#f39c12,stroke:#d68910,color:#000
    style FO04 fill:#f39c12,stroke:#d68910,color:#000
    style FO05 fill:#f39c12,stroke:#d68910,color:#000
    style QO01 fill:#58d68d,stroke:#2ecc71,color:#000
    style QO02 fill:#58d68d,stroke:#2ecc71,color:#000
    style QO03 fill:#58d68d,stroke:#2ecc71,color:#000
```

**Color Key:**
- 🔵 **Tier 1:** Overall platform mission
- 🟢 **Tier 2:** Major capability areas
- 🟡 **Tier 3 (Gold):** Functional leaf objectives
- 🟢 **Tier 3 (Mint):** Quality leaf objectives

---

## 3. Fare Calculation Logic

I chose a **duration-based pricing model** since the assignment allows flexibility in formula design.

### Pricing Formula

$$\text{TripCost} = \text{StartFee} + (\text{Minutes} \times \text{PerMinuteRate})$$

**Component Breakdown:**

| Component | Meaning | Sample Value |
|-----------|---------|--------------|
| StartFee | One-time unlock charge | €1.00 |
| Minutes | Elapsed time from unlock to lock | Variable |
| PerMinuteRate | Ongoing usage charge | €0.20 |

**Calculation Example:**  
A 12-minute trip costs: €1.00 + (12 × €0.20) = **€3.40**

---

## 4. Behavioral Interface Model (BIM)

The state diagram below traces a complete rental session, showing how control passes between the three roles.

### Workflow Narrative

1. **Account Setup:** A first-time user registers and provides payment information
2. **Vehicle Selection:** The rider claims an available scooter through the app
3. **Travel Phase:** Vehicle Controller unlocks the motor; rider travels
4. **Session Close:** Rider ends the trip; Vehicle Controller locks hardware
5. **Settlement:** Billing Engine calculates duration-based fare and charges the card

### State Flow Diagram

```mermaid
stateDiagram-v2
    direction LR
    
    [*] --> Signup: First-time User
    Signup --> ClaimVehicle: Credentials Verified
    ClaimVehicle --> ActivateMotor: Vehicle Confirmed
    ActivateMotor --> Travel: Motor Engaged
    Travel --> EndSession: Rider Stops
    EndSession --> CalculateFare: Trip Data Logged
    CalculateFare --> ChargeCard: Amount Determined
    ChargeCard --> [*]: Payment Successful
```

---

## Closing Remarks

This solution models a real-world urban mobility scenario using agent-oriented principles. The three-role decomposition mirrors how actual ride-share platforms separate user interfaces, IoT device management, and financial backends. The time-based billing formula keeps the model simple while remaining practical.
