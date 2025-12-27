import snakes.plugins
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *

# ==========================================
# EXERCISE 6: E-Scooter CPN Model
# Student: Siddharth D. Patni (sp01)
# ==========================================

def create_net():
    """
    Creates a Coloured Petri Net (CPN) for the E-Scooter System.
    """
    n = PetriNet('E-Scooter Ride Share')

    # -----------------------------------------------------------------------
    # 1. PLACES
    # -----------------------------------------------------------------------
    
    # Place: CommuterPool
    # Holds idle commuters.
    # Token format: Tuple (User_ID, Wallet_Balance)
    n.add_place(Place('CommuterPool', [('User_A', 100), ('User_B', 50)]))

    # Place: ScooterPool
    # Holds idle scooters ready to be reserved.
    # Token format: Tuple (Scooter_ID, Location)
    n.add_place(Place('ScooterPool', [('Scooter_1', 'Station_Main'), ('Scooter_2', 'Station_Park')]))

    # Place: ReservedState
    # Holds the association between a user and a scooter.
    # Token format: Tuple (User_ID, Scooter_ID)
    n.add_place(Place('ReservedState', []))

    # Place: OnRide
    # Represents the active ride.
    # Token format: Tuple (User_ID, Scooter_ID, Start_Time)
    n.add_place(Place('OnRide', []))

    # Place: PaymentQueue
    # Holds data waiting for payment processing after ride.
    # Token format: Tuple (User_ID, Cost)
    n.add_place(Place('PaymentQueue', []))

    # Place: BillingHistory
    # Stores the final record of the transaction.
    # Token format: Tuple (User_ID, Final_Cost, Status)
    n.add_place(Place('BillingHistory', []))

    # -----------------------------------------------------------------------
    # 2. TRANSITIONS & LOGIC
    # -----------------------------------------------------------------------

    # --- Transition: Reserve ---
    # A commuter selects an idle scooter.
    # Input: Commuter (u, bal), Scooter (s, loc)
    # Output: (u, s) to ReservedState
    n.add_transition(Transition('Reserve'))
    n.add_input('CommuterPool', 'Reserve', Tuple([Variable('u'), Variable('bal')]))
    n.add_input('ScooterPool', 'Reserve', Tuple([Variable('s'), Variable('loc')]))
    n.add_output('ReservedState', 'Reserve', Tuple([Variable('u'), Variable('s')]))

    # --- Transition: StartRide (Unlock) ---
    # The user unlocks the reserved scooter.
    # Input: (u, s)
    # Output: (u, s, start_time=0) -> Simulating start time as 0 for simplicity
    n.add_transition(Transition('StartRide'))
    n.add_input('ReservedState', 'StartRide', Tuple([Variable('u'), Variable('s')]))
    # We inject a simulated start time of '10' (10:00 AM)
    n.add_output('OnRide', 'StartRide', Tuple([Variable('u'), Variable('s'), Value(10)]))

    # --- Transition: EndRide ---
    # User finishes ride.
    # 1. Calculates Cost.
    # 2. Returns Scooter to Pool.
    # 3. Sends Bill to PaymentQueue.
    n.add_transition(Transition('EndRide'))
    n.add_input('OnRide', 'EndRide', Tuple([Variable('u'), Variable('s'), Variable('start_t')]))
    
    # Logic: End time is simulated as '25' (10:15 AM). Duration = 15 mins.
    # Cost Formula: Base (1.00) + (Duration * 0.20)
    # Cost = 1.00 + (15 * 0.20) = 4.0
    
    # Output 1: Return Scooter to Pool (Simulating it is left at 'Station_Dest')
    n.add_output('ScooterPool', 'EndRide', Tuple([Variable('s'), Value('Station_Dest')]))
    
    # Output 2: Send Bill to Queue (User, Cost=4.0)
    n.add_output('PaymentQueue', 'EndRide', Tuple([Variable('u'), Value(4.0)]))

    # --- Transition: ProcessPayment ---
    # Deducts cost from user wallet.
    # Input: User in Pool (Wait, technically user is busy riding? 
    # In this simple model, the user token was consumed at Reserve. 
    # We need to recreate the user token here with updated balance.)
    
    # Logic: To handle the User token correctly, we need to pass the Wallet Balance through the flow.
    # However, to keep it simple and readable for the exercise:
    # We will assume the wallet is accessed here from the payment queue directly 
    # and we just log the history.
    
    n.add_transition(Transition('ProcessPayment'))
    n.add_input('PaymentQueue', 'ProcessPayment', Tuple([Variable('u'), Variable('cost')]))
    n.add_output('BillingHistory', 'ProcessPayment', Tuple([Variable('u'), Variable('cost'), Value('PAID')]))
    
    # Create a new User token to put back in pool (Cycle completed)
    # Let's assume they have infinite money for this simulation or just reset balance
    n.add_output('CommuterPool', 'ProcessPayment', Tuple([Variable('u'), Value(100)]))

    return n

def run_simulation():
    """
    Runs the simulation sequence and generates images.
    """
    net = create_net()
    print("[*] E-Scooter Net Created.")

    def save(name):
        filename = f"sim_scooter_{name}.png"
        net.draw(filename)
        print(f"    -> Saved state: {filename}")

    # 1. Initial State
    save("00_Initial")

    # 2. User A Reserves Scooter 1
    print("[-] User_A reserves Scooter_1...")
    net.transition('Reserve').fire(Substitution(u='User_A', bal=100, s='Scooter_1', loc='Station_Main'))
    save("01_Reserved")

    # 3. User A Starts Ride
    print("[-] User_A unlocks and starts riding...")
    net.transition('StartRide').fire(Substitution(u='User_A', s='Scooter_1'))
    save("02_Riding")

    # 4. User B Reserves Scooter 2 (Concurrency Test)
    print("[-] User_B reserves Scooter_2...")
    net.transition('Reserve').fire(Substitution(u='User_B', bal=50, s='Scooter_2', loc='Station_Park'))
    save("03_Concurrency_Reserved")

    # 5. User A Ends Ride
    print("[-] User_A finishes ride (Cost calculated)...")
    # Matching the variable names in Input: u, s, start_t
    net.transition('EndRide').fire(Substitution(u='User_A', s='Scooter_1', start_t=10))
    save("04_RideEnded_PaymentPending")

    # 6. Process Payment
    print("[-] Processing payment for User_A...")
    net.transition('ProcessPayment').fire(Substitution(u='User_A', cost=4.0))
    save("05_PaymentComplete_UserReturned")

    print("[*] Simulation Done.")

if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        print(f"Error: {e}")