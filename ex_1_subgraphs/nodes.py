from ex_1_subgraphs.state import SharedState

# -------------------------
# NODE 1: DRAFT TEXT
# -------------------------
def draft_text(state: SharedState):
    print("\n[Node] Drafting initial text...")
    state["text"] = "The quick brown fox jumps over the lazy dog."
    return state


# -------------------------
# NODE 2: CALL SUBGRAPH
# -------------------------
def run_subgraph(state: SharedState, subgraph):
    print("\n[Node] Refining text via subgraph...")
    return subgraph.invoke(state)


# -------------------------
# NODE 3: FINAL OUTPUT
# -------------------------
def final_output(state: SharedState):
    print("\n[Node] Preparing final output...")
    state["text"] = f"[FINAL] {state['text']}"
    return state
