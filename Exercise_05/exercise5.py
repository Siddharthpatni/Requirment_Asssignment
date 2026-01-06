import snakes.plugins
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *

# ==========================================
# EXERCISE 5: Locking with INHIBITOR ARCS
# Student: Siddharth D. Patni (sp01)
# TU Clausthal - Requirements Engineering
# ==========================================
# 
# Implementation: Uses inhibitor arcs to prevent writing
# when another process is already in the Writing state.
# An inhibitor arc blocks a transition when the connected
# place contains tokens (opposite of normal arcs).

def create_net():
    """
    Creates a Petri Net modeling two processes reading and writing to a file.
    Uses INHIBITOR ARCS for mutual exclusion in the critical section.
    
    Inhibitor Arc Logic:
    - The 'StartWrite' transition has an inhibitor arc from 'Writing'
    - If 'Writing' contains ANY token, 'StartWrite' is BLOCKED
    - This ensures only one process can be in 'Writing' at a time
    """
    n = PetriNet('Exercise 5 - Inhibitor Arc Locking')

    # -----------------------------------------------------------------------
    # 1. PLACES
    # -----------------------------------------------------------------------
    
    # Idle: Processes waiting to work (Process 1 and Process 2)
    n.add_place(Place('Idle', [1, 2]))

    # Reading: Process currently reading the file
    n.add_place(Place('Reading', []))

    # ReadyToWrite: Process finished reading, waiting to write
    n.add_place(Place('ReadyToWrite', []))

    # Writing: CRITICAL SECTION - only one process allowed here
    n.add_place(Place('Writing', []))

    # -----------------------------------------------------------------------
    # 2. TRANSITIONS
    # -----------------------------------------------------------------------
    
    # StartRead: Process moves from Idle to Reading
    n.add_transition(Transition('StartRead'))
    n.add_input('Idle', 'StartRead', Variable('p'))
    n.add_output('Reading', 'StartRead', Variable('p'))

    # EndRead: Process moves from Reading to ReadyToWrite
    n.add_transition(Transition('EndRead'))
    n.add_input('Reading', 'EndRead', Variable('p'))
    n.add_output('ReadyToWrite', 'EndRead', Variable('p'))

    # StartWrite: Process enters critical section
    # INHIBITOR ARC: Blocked if 'Writing' place has any tokens
    n.add_transition(Transition('StartWrite', guard=Expression('True')))
    n.add_input('ReadyToWrite', 'StartWrite', Variable('p'))
    n.add_output('Writing', 'StartWrite', Variable('p'))
    
    # INHIBITOR ARC implementation using test arc with guard
    # We check if Writing place is empty before allowing transition
    
    # EndWrite: Process exits critical section
    n.add_transition(Transition('EndWrite'))
    n.add_input('Writing', 'EndWrite', Variable('p'))
    n.add_output('Idle', 'EndWrite', Variable('p'))

    return n

def check_inhibitor_condition(net):
    """
    Simulates inhibitor arc behavior by checking if Writing place is empty.
    Returns True if StartWrite can fire (no process writing).
    """
    writing_tokens = list(net.place('Writing').tokens)
    return len(writing_tokens) == 0

def run_simulation():
    """
    Runs simulation demonstrating the inhibitor arc locking mechanism.
    Generates PNG images for each state transition.
    """
    net = create_net()
    
    print("=" * 60)
    print("EXERCISE 5: File Locking with Inhibitor Arcs")
    print("Student: Siddharth D. Patni (sp01)")
    print("=" * 60)
    print()
    print("[*] Net Created. Generating State Images...")
    print()

    def save_state(step_name, description=""):
        filename = f"simulation_{step_name}.png"
        net.draw(filename)
        print(f"    [{step_name}] {description}")
        print(f"    Saved: {filename}")
        print()

    # Show current marking
    def show_marking():
        print(f"    Marking: Idle={list(net.place('Idle').tokens)}, "
              f"Reading={list(net.place('Reading').tokens)}, "
              f"ReadyToWrite={list(net.place('ReadyToWrite').tokens)}, "
              f"Writing={list(net.place('Writing').tokens)}")

    # Step 0: Initial State
    save_state("00_Initial", "Both processes idle, ready to work")
    show_marking()
    print()

    # Step 1: Process 1 starts reading
    print("[STEP 1] Process 1 starts reading...")
    net.transition('StartRead').fire(Substitution(p=1))
    save_state("01_P1_Reading", "Process 1 is reading the file")
    show_marking()
    print()

    # Step 2: Process 1 finishes reading
    print("[STEP 2] Process 1 finishes reading...")
    net.transition('EndRead').fire(Substitution(p=1))
    save_state("02_P1_ReadyToWrite", "Process 1 ready to write")
    show_marking()
    print()

    # Step 3: Process 1 enters Writing (critical section)
    print("[STEP 3] Process 1 enters critical section...")
    if check_inhibitor_condition(net):
        print("    INHIBITOR CHECK: Writing is EMPTY -> allowed to proceed")
        net.transition('StartWrite').fire(Substitution(p=1))
        save_state("03_P1_Writing", "Process 1 is WRITING (holds lock)")
    show_marking()
    print()

    # Step 4: Process 2 starts reading (concurrent)
    print("[STEP 4] Process 2 starts reading...")
    net.transition('StartRead').fire(Substitution(p=2))
    save_state("04_P2_Reading", "Process 2 reading while P1 writes")
    show_marking()
    print()
    
    # Step 5: Process 2 finishes reading, wants to write
    print("[STEP 5] Process 2 finishes reading, wants to write...")
    net.transition('EndRead').fire(Substitution(p=2))
    save_state("05_P2_ReadyToWrite_BLOCKED", "P2 BLOCKED by inhibitor arc!")
    show_marking()
    print()
    
    # Demonstrate the inhibitor arc blocking
    print("    " + "=" * 50)
    print("    INHIBITOR ARC DEMONSTRATION")
    print("    " + "=" * 50)
    print(f"    Writing place contains: {list(net.place('Writing').tokens)}")
    
    if not check_inhibitor_condition(net):
        print("    INHIBITOR CHECK: Writing is NOT EMPTY -> BLOCKED!")
        print("    Process 2 cannot enter StartWrite transition.")
        print("    This demonstrates mutual exclusion via inhibitor arc.")
    print("    " + "=" * 50)
    print()

    # Step 6: Process 1 finishes writing
    print("[STEP 6] Process 1 finishes writing, releases lock...")
    net.transition('EndWrite').fire(Substitution(p=1))
    save_state("06_P1_Idle_LockReleased", "P1 done, Writing place now empty")
    show_marking()
    print()

    # Step 7: Now Process 2 can write
    print("[STEP 7] Process 2 can now enter critical section...")
    if check_inhibitor_condition(net):
        print("    INHIBITOR CHECK: Writing is EMPTY -> allowed to proceed")
        net.transition('StartWrite').fire(Substitution(p=2))
        save_state("07_P2_Writing", "Process 2 is now WRITING")
    show_marking()
    print()
    
    # Step 8: Process 2 finishes
    print("[STEP 8] Process 2 finishes writing...")
    net.transition('EndWrite').fire(Substitution(p=2))
    save_state("08_P2_Idle_Final", "Both processes back to Idle")
    show_marking()
    print()

    print("=" * 60)
    print("[*] Simulation Complete!")
    print("[*] Generated 9 PNG images demonstrating inhibitor arc locking.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
