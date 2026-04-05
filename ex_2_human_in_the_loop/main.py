from functools import partial
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from ex_2_human_in_the_loop.state import SharedState
from ex_2_human_in_the_loop.nodes import draft_text, run_subgraph, human_review
from ex_2_human_in_the_loop.subgraph import build_subgraph

# -------------------------
# BUILD MAIN GRAPH
# -------------------------
def build_graph():
    subgraph = build_subgraph()

    graph = StateGraph(SharedState)

    graph.add_node("draft", draft_text)
    graph.add_node("subgraph", partial(run_subgraph, subgraph=subgraph))
    graph.add_node("review", human_review)

    graph.set_entry_point("draft")

    graph.add_edge("draft", "subgraph")
    graph.add_edge("subgraph", "review")

    return graph.compile(checkpointer=MemorySaver(), interrupt_before=["review"])


# -------------------------
# RUN WORKFLOW
# -------------------------
if __name__ == "__main__":
    app = build_graph()

    config = {"configurable": {"thread_id": "thread-1"}}

    print("\n=== RUN 1: Draft text (pause before review) ===")
    app.invoke({"text": ""}, config=config)
    print("[Paused before review node]")

    print("\n=== RUN 1 (continued): Resume for human review ===")
    result = app.invoke(None, config=config)

    print("\nFinal Output:")
    print(result["text"])