from langgraph.graph import StateGraph
from ex_1_subgraphs.state import SharedState


# -------------------------
# SUBGRAPH NODE
# -------------------------
def subgraph_text(state: SharedState):
    print("[Subgraph] Adding text from subgraph...")
    state["text"] += " (refined by subgraph)"
    return state


# -------------------------
# BUILD SUBGRAPH
# -------------------------
def build_subgraph():
    graph = StateGraph(SharedState)

    graph.add_node("refine", subgraph_text)
    graph.set_entry_point("refine")

    return graph.compile()
