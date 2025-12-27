# AOM Models Submission - Exercise 06

**TU Clausthal**  
**Department:** Institut für Software and Systems Engineering  
**Course:** Requirements Engineering  
**Exercise:** 06 (Coloured Petri Net - E-Scooter System)  
**Submitted By:** Siddharth D. Patni (sp01)  
**Date:** 27.12.2024

---

## 1. Introduction

This document presents a Coloured Petri Net (CPN) model for the E-Scooter Ride-Share System using the SNAKES library. The model captures the complete workflow from reservation to payment processing.

---

## 2. CPN Model Structure

### 2.1 Places (Token Types)

| Place | Token Format | Description |
|-------|--------------|-------------|
| CommuterPool | (User_ID, Wallet_Balance) | Idle commuters ready to ride |
| ScooterPool | (Scooter_ID, Location) | Available scooters at stations |
| ReservedState | (User_ID, Scooter_ID) | Active reservations |
| OnRide | (User_ID, Scooter_ID, Start_Time) | Active rides in progress |
| PaymentQueue | (User_ID, Cost) | Pending payments |
| BillingHistory | (User_ID, Final_Cost, Status) | Completed transactions |

### 2.2 Transitions

| Transition | Input | Output | Description |
|------------|-------|--------|-------------|
| Reserve | CommuterPool, ScooterPool | ReservedState | User reserves a scooter |
| StartRide | ReservedState | OnRide | User unlocks and begins ride |
| EndRide | OnRide | ScooterPool, PaymentQueue | Ride ends, cost calculated |
| ProcessPayment | PaymentQueue | BillingHistory, CommuterPool | Payment processed |

---

## 3. Cost Calculation

**Formula:** `TotalFee = UnlockFee + (Duration × Rate)`

- **UnlockFee:** €1.00
- **Rate:** €0.20 per minute
- **Example:** 15 min ride = €1.00 + (15 × €0.20) = €4.00

---

## 4. Simulation Results

The Python script generates the following state diagrams:

1. **sim_scooter_00_Initial.png** - Initial state with 2 users and 2 scooters
2. **sim_scooter_01_Reserved.png** - User_A reserves Scooter_1
3. **sim_scooter_02_Riding.png** - User_A starts riding
4. **sim_scooter_03_Concurrency_Reserved.png** - User_B reserves Scooter_2 (concurrent)
5. **sim_scooter_04_RideEnded_PaymentPending.png** - User_A ends ride, payment pending
6. **sim_scooter_05_PaymentComplete_UserReturned.png** - Payment processed, user returned to pool

---

## 5. Key Features Demonstrated

- **Concurrency:** Multiple users can reserve different scooters simultaneously
- **Token Flow:** Proper movement of colored tokens through the net
- **State Tracking:** Complete audit trail from reservation to billing
- **SNAKES CPN Compliance:** Uses only SNAKES library for Petri Net modeling

---

## 6. Files Included

- `Solution_Exercise_06.py` - Python CPN implementation
- `sim_scooter_*.png` - Generated simulation diagrams (6 images)
- `AOM_Models_Submission.md` - This documentation

---

## 7. Running the Code

```bash
python Solution_Exercise_06.py
```

**Requirements:**
- Python 3.x
- SNAKES library (`pip install snakes`)
- Graphviz (`brew install graphviz` on macOS)