# Exercise 06 Solution: E-Scooter Rental Workflow via Coloured Petri Nets

**TU Clausthal**  
**Institute:** Software and Systems Engineering  
**Module:** Requirements Engineering  
**Assignment:** 06 – Coloured Petri Net Modeling  
**Author:** Siddharth D. Patni (sp01)  
**Submission Date:** 27.12.2024

---

## 1. Modeling Approach

Unlike standard Petri Nets where all tokens are identical, Coloured Petri Nets (CPNs) attach data to each token. This capability proves essential for tracking individual users and scooters through the rental lifecycle.

I structured the model around six places representing different phases of the customer journey, from an available user/scooter pool through to completed billing records.

---

## 2. Network Topology

### Token Repositories (Places)

| Place | Token Structure | Purpose |
|-------|-----------------|---------|
| CommuterPool | `(UserID, WalletBalance)` | Users available to rent |
| ScooterPool | `(ScooterID, StationLocation)` | Vehicles parked at stations |
| ReservedState | `(UserID, ScooterID)` | Active booking records |
| OnRide | `(UserID, ScooterID, StartTimestamp)` | Trips in progress |
| PaymentQueue | `(UserID, OwedAmount)` | Pending financial transactions |
| BillingHistory | `(UserID, PaidAmount, Status)` | Completed transaction records |

### State Transitions

| Transition | Consumes From | Produces To | Action Performed |
|------------|---------------|-------------|------------------|
| Reserve | CommuterPool, ScooterPool | ReservedState | Links user to specific vehicle |
| StartRide | ReservedState | OnRide | Records trip start timestamp |
| EndRide | OnRide | ScooterPool, PaymentQueue | Calculates fare, returns vehicle |
| ProcessPayment | PaymentQueue | BillingHistory, CommuterPool | Deducts balance, logs transaction |

---

## 3. Fare Computation

Following the time-based model from Exercise 04:

**Formula:** `TripTotal = StartupCharge + (TripMinutes × MinuteRate)`

**Parameters Used:**
- StartupCharge: €1.00 (covers maintenance overhead)
- MinuteRate: €0.20 (usage-proportional charge)

**Sample Calculation:**  
15-minute trip = €1.00 + (15 × €0.20) = **€4.00**

---

## 4. Simulation Progression

The script generates six state snapshots illustrating the complete workflow:

| Snapshot | What Changed |
|----------|--------------|
| `sim_scooter_00_Initial.png` | Starting state: 2 users, 2 scooters in pools |
| `sim_scooter_01_Reserved.png` | User_A claims Scooter_1 |
| `sim_scooter_02_Riding.png` | User_A's trip begins (timestamp recorded) |
| `sim_scooter_03_Concurrency_Reserved.png` | User_B claims Scooter_2 (parallel action) |
| `sim_scooter_04_RideEnded_PaymentPending.png` | User_A finishes, fare queued |
| `sim_scooter_05_PaymentComplete_UserReturned.png` | User_A's payment processed, back in pool |

---

## 5. Notable Model Properties

- **Parallel Execution:** Multiple users operate independently—no artificial sequencing
- **Identity Preservation:** Colored tokens maintain user/scooter IDs throughout transitions
- **Audit Capability:** BillingHistory place provides complete transaction records
- **Library Compliance:** Implementation uses only SNAKES library constructs

---

## 6. Running the Simulation

```bash
cd Exercise_06
python Solution_Exercise_06.py
```

**System Requirements:**
- Python 3.8 or newer
- SNAKES package: `pip install snakes`
- Graphviz rendering: `brew install graphviz` (macOS) or `apt install graphviz` (Linux)

---

## 7. Submission Contents

| File | Description |
|------|-------------|
| `Solution_Exercise_06.py` | CPN implementation source code |
| `sim_scooter_*.png` | Six simulation state images |
| `AOM_Models_Submission.md` | This documentation file |