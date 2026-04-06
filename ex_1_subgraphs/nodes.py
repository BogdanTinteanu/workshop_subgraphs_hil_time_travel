from .state import SharedState

def load_lead(state: SharedState):
    print("[Node] Loading lead data...")
    return {
        "lead_name": "Ion Popescu",
        "company": "SecureBank SRL",
        "industry": "Banking/Fintech",
        "budget": "120,000 USD"
    }

def run_qualify_subgraph(state: SharedState, subgraph):
    print("\n[Node] Invocare Subgraf Calificare...")
    return subgraph.invoke(state)

def run_pitch_subgraph(state: SharedState, subgraph):
    print("\n[Node] Invocare Subgraf Pitch...")
    return subgraph.invoke(state)

def format_output(state: SharedState):
    print("\n--- REZULTAT FINAL ---")
    print(f"STATUS: {state['qualification']}")
    print(f"MOTIV: {state['qualification_reason']}")
    print(f"PITCH:\n{state['pitch']}")
    print("----------------------")
    return state
