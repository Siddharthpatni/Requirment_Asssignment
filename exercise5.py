import snakes.plugins
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *

# ==========================================
# EXERCISE 5: Locking Mechanism with Test Arcs
# Student: Siddharth D. Patni (sp01)
# ==========================================
# 
# Alternative implementation using Test arcs instead of Inhibitor arcs
# Test arc reads a token without consuming it

def create_net():
    """
    Creates a Petri Net modeling two processes reading and writing to a file.
    Implements a locking mechanism using a Lock token to ensure 
    that the file is not written to while another process is writing.
    """
    n = PetriNet('Exercise 5 - Write Lock')

    # -----------------------------------------------------------------------
    # 1. PLACES
    # -----------------------------------------------------------------------
    # 'Idle': Stores the processes when they are not working.
    # Initial tokens: 1 and 2 representing Process 1 and Process 2.
    n.add_place(Place('Idle', [1, 2]))

    # 'Reading': State where a process is reading the file.
    n.add_place(Place('Reading', []))

    # 'ReadyToWrite': Buffer state. The process has finished reading 
    # and is waiting to get the lock to write.
    n.add_place(Place('ReadyToWrite', []))

    # 'Writing': The CRITICAL SECTION.
    # Only one process should be here at a time.
    n.add_place(Place('Writing', []))
    
    # 'Lock': Token representing the write lock
    # When present, a process can acquire it to write
    # Initial: one lock token available
    n.add_place(Place('Lock', ['available']))

    # -----------------------------------------------------------------------
    # 2. TRANSITIONS
    # -----------------------------------------------------------------------
    
    # Transition: StartRead
    # Moves a process from Idle to Reading.
    n.add_transition(Transition('StartRead'))
    n.add_input('Idle', 'StartRead', Variable('p'))
    n.add_output('Reading', 'StartRead', Variable('p'))

    # Transition: EndRead
    # Moves a process from Reading to ReadyToWrite.
    n.add_transition(Transition('EndRead'))
    n.add_input('Reading', 'EndRead', Variable('p'))
    n.add_output('ReadyToWrite', 'EndRead', Variable('p'))

    # Transition: StartWrite (THE LOCKING MECHANISM)
    # Moves a process from ReadyToWrite to Writing.
    # Also consumes the Lock token - only one process can write at a time
    n.add_transition(Transition('StartWrite'))
    n.add_input('ReadyToWrite', 'StartWrite', Variable('p'))
    n.add_input('Lock', 'StartWrite', Variable('lock'))  # Consume lock
    n.add_output('Writing', 'StartWrite', Variable('p'))

    # Transition: EndWrite
    # Moves a process from Writing back to Idle, releasing the lock.
    n.add_transition(Transition('EndWrite'))
    n.add_input('Writing', 'EndWrite', Variable('p'))
    n.add_output('Idle', 'EndWrite', Variable('p'))
    n.add_output('Lock', 'EndWrite', Expression("'available'"))  # Release lock (return 'available' token)

    return n

def run_simulation():
    """
    Runs a simple simulation sequence to demonstrate the locking.
    Saves PNG images of the states.
    """
    net = create_net()
    
    print("[*] Net Created. Generating State Images...")

    # Helper to save state
    def save_state(step_name):
        filename = f"simulation_{step_name}.png"
        net.draw(filename)
        print(f"    Saved state: {filename}")

    # Step 0: Initial State (Both Idle, Lock Available)
    save_state("00_Initial")

    # Step 1: Process 1 Starts Reading
    print("[-] Process 1 starts reading...")
    net.transition('StartRead').fire(Substitution(p=1))
    save_state("01_P1_Reading")

    # Step 2: Process 1 Finishes Reading (Ready to Write)
    print("[-] Process 1 finishes reading...")
    net.transition('EndRead').fire(Substitution(p=1))
    save_state("02_P1_ReadyToWrite")

    # Step 3: Process 1 Starts Writing (Acquires Lock)
    print("[-] Process 1 starts writing (Lock Acquired)...")
    net.transition('StartWrite').fire(Substitution(p=1, lock='available'))
    save_state("03_P1_Writing")

    # Step 4: Process 2 Tries to Enter (DEMONSTRATE LOCK)
    print("[-] Process 2 starts reading...")
    net.transition('StartRead').fire(Substitution(p=2))
    save_state("04_P2_Reading")
    
    print("[-] Process 2 finishes reading...")
    net.transition('EndRead').fire(Substitution(p=2))
    save_state("05_P2_ReadyToWrite_BLOCKED")
    
    print("    [!] At this stage, Process 2 is in 'ReadyToWrite'.")
    print("    [!] Process 1 is in 'Writing' and holds the lock.")
    print("    [!] Transition 'StartWrite' for P2 is BLOCKED - no lock available.")
    
    # Check modes (valid firings) for StartWrite
    modes = list(net.transition('StartWrite').modes())
    if not modes:
        print("    [SUCCESS] 'StartWrite' has no valid modes. Lock is working!")
    else:
        print(f"    [FAIL] 'StartWrite' is executable! Modes: {modes}")

    # Step 5: Process 1 Finishes Writing (Releases Lock)
    print("[-] Process 1 finishes writing (Lock Released)...")
    net.transition('EndWrite').fire(Substitution(p=1))
    save_state("06_P1_Idle_LockReleased")

    # Step 6: Process 2 Can Now Write
    print("[-] Process 2 starts writing (Now Allowed - Lock Available)...")
    net.transition('StartWrite').fire(Substitution(p=2, lock='available'))
    save_state("07_P2_Writing")
    
    print("[-] Process 2 finishes writing...")
    net.transition('EndWrite').fire(Substitution(p=2))
    save_state("08_P2_Idle_Final")

    print("[*] Simulation Complete.")
    print(f"[*] Generated 9 PNG images showing the state transitions.")

if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
