from functools import partial
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from ex_3_time_travel.state import SharedState
from ex_3_time_travel.subgraph import build_subgraph
from ex_3_time_travel.nodes import draft_text, run_subgraph, human_review


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
    # -------------------------
    # TIME TRAVEL DEMO
    # -------------------------

    app = build_graph()

    config = {"configurable": {"thread_id": "thread-1"}}

    print("\n=== RUN 1: Initial run (pauses before review) ===")
    app.invoke({"text": ""}, config=config)
    print("[Paused before review node]")

    print("\n=== RUN 1 (continued): Resume for human review ===")
    app.invoke(None, config=config)

    print("\n=== RUN 2: TIME TRAVEL (Start from subgraph) ===")

    # Find the checkpoint where "subgraph" is the next node to run
    history = list(app.get_state_history(config))
    target = next(s for s in history if s.next == ("subgraph",))

    # Modify state at the checkpoint before replaying
    updated_config = app.update_state(target.config, {"text": "Overridden before subgraph."})

    # Replay from the updated checkpoint — pauses before review
    app.invoke(None, config=updated_config)
    print("[Paused before review node]")

    print("\n=== RUN 2 (continued): Resume for human review ===")
    result = app.invoke(None, config=config)

    print("\nFinal output after time travel + human review:")
    print(result["text"])