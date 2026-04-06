from langgraph.graph import StateGraph
from functools import partial
from .state import SharedState
from .nodes import load_lead, run_qualify_subgraph, run_pitch_subgraph, format_output
from .subgraph_qualify import build_qualify_subgraph
from .subgraph_pitch import build_pitch_subgraph

# 1. Instantiem subgrafurile
qualify_subgraph = build_qualify_subgraph()
pitch_subgraph = build_pitch_subgraph()

# 2. Construim graful principal
builder = StateGraph(SharedState)

builder.add_node("load_lead", load_lead)
# Injectam subgrafurile folosind partial
builder.add_node("qualify", partial(run_qualify_subgraph, subgraph=qualify_subgraph))
builder.add_node("pitch", partial(run_pitch_subgraph, subgraph=pitch_subgraph))
builder.add_node("format", format_output)

# 3. Definim fluxul
builder.set_entry_point("load_lead")
builder.add_edge("load_lead", "qualify")
builder.add_edge("qualify", "pitch")
builder.add_edge("pitch", "format")
builder.set_finish_point("format")

graph = builder.compile()

if __name__ == "__main__":
    graph.invoke({})
