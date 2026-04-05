from ex_3_time_travel.state import SharedState


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
# NODE 3: HUMAN-IN-LOOP
# -------------------------
def human_review(state: SharedState):
    print("\n[Node] Human Review")
    print("Current Output:", state["text"])

    decision = input("Approve or edit? (yes/edit): ")

    if decision.lower() == "edit":
        new_text = input("Enter updated text: ")
        state["text"] = new_text

    return state