from functools import partial
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph
from ex_1_subgraphs.state import SharedState
from ex_1_subgraphs.subgraph import build_subgraph
from ex_1_subgraphs.nodes import draft_text, run_subgraph, final_output


# -------------------------
# BUILD MAIN GRAPH
# -------------------------
def build_graph():
    subgraph = build_subgraph()

    graph = StateGraph(SharedState)

    graph.add_node("draft", draft_text)
    graph.add_node("subgraph", partial(run_subgraph, subgraph=subgraph))
    graph.add_node("final", final_output)

    graph.set_entry_point("draft")

    graph.add_edge("draft", "subgraph")
    graph.add_edge("subgraph", "final")

    return graph.compile()


# -------------------------
# RUN WORKFLOW
# -------------------------
if __name__ == "__main__":
    app = build_graph()

    print("\n=== RUN: SUBGRAPHS DEMO ===")
    result = app.invoke({"text": ""})

    print("\nFinal Output:")
    print(result["text"])
