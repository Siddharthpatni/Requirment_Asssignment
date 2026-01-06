# Exercise 06: E-Scooter CPN Model

**TU Clausthal**  
**Institute:** Software and Systems Engineering  
**Module:** Requirements Engineering  
**Assignment:** 06 – Coloured Petri Net Model  
**Author:** Siddharth D. Patni (sp01)  
**Date:** 27.12.2024

---

## 1. Overview

This exercise implements a **Coloured Petri Net (CPN)** model for the E-Scooter Ride-Share System based on the AOM Goal and Behavioral Interface Models from Exercise 04.

### Key Features:
- **2 Commuters:** User_A (€100 balance), User_B (€50 balance)
- **2 Scooters:** Scooter_1 (Station_Main), Scooter_2 (Station_Park)
- **Complete Workflow:** Reservation → Riding → Cost Calculation → Payment

---

## 2. CPN Model Structure

### Places (Token Types)

| Place | Token Format | Initial State |
|-------|--------------|---------------|
| `CommuterPool` | (User_ID, Wallet) | [('User_A', 100), ('User_B', 50)] |
| `ScooterPool` | (Scooter_ID, Location) | [('Scooter_1', 'Station_Main'), ('Scooter_2', 'Station_Park')] |
| `ReservedState` | (User_ID, Scooter_ID) | [] |
| `OnRide` | (User_ID, Scooter_ID, Start_Time) | [] |
| `PaymentQueue` | (User_ID, Cost) | [] |
| `BillingHistory` | (User_ID, Cost, Status) | [] |

### Transitions

| Transition | Description |
|------------|-------------|
| `Reserve` | Commuter claims an idle scooter |
| `StartRide` | Scooter unlocked, ride begins |
| `EndRide` | Ride ends, cost calculated, scooter returned |
| `ProcessPayment` | Fee debited, user returns to pool |

---

## 3. Cost Calculation

**Formula:** `Cost = Base Fee + (Duration × Rate)`

| Parameter | Value |
|-----------|-------|
| Base Fee | €1.00 |
| Rate | €0.20/min |
| Simulated Duration | 15 minutes |
| **Total Cost** | **€4.00** |

---

## 4. Simulation Results

| Step | Image | Description |
|------|-------|-------------|
| 0 | `sim_scooter_00_Initial.png` | Initial: 2 users, 2 scooters |
| 1 | `sim_scooter_01_Reserved.png` | User_A reserves Scooter_1 |
| 2 | `sim_scooter_02_Riding.png` | User_A starts riding |
| 3 | `sim_scooter_03_Concurrency_Reserved.png` | User_B reserves Scooter_2 (concurrent) |
| 4 | `sim_scooter_04_RideEnded_PaymentPending.png` | User_A ends ride, €4.00 fee queued |
| 5 | `sim_scooter_05_PaymentComplete_UserReturned.png` | Payment processed |

---

## 5. Mapping from AOM Models

| AOM Goal/Role | CPN Element |
|---------------|-------------|
| Commuter Role | Tokens in CommuterPool |
| Fleet Manager Role | Transitions (Reserve, StartRide, EndRide) |
| Payment Processor Role | Transition (ProcessPayment) |
| Registration (FG-01) | User tokens in CommuterPool |
| Reservation (FG-02) | Reserve transition |
| Commute (FG-03) | OnRide place |
| End Ride (FG-04) | EndRide transition |
| Payment (FG-05) | ProcessPayment transition |

---

## 6. Running the Code

```bash
pip install snakes
brew install graphviz  # macOS
python3 Solution_Exercise_06.py
```

---

## 7. Submission Files

| File | Description |
|------|-------------|
| `Solution_Exercise_06.py` | SNAKES CPN implementation |
| `sim_scooter_*.png` | 6 simulation state images |
| `AOM_Goal_Model.pdf` | Goal hierarchy diagram |
| `AOM_BIM.pdf` | Behavioral Interface Model |
| `README.md` | This documentation |
