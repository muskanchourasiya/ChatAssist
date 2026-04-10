from langgraph.graph import StateGraph, END
from app.graph.state import GraphState

from app.graph.nodes import (
    guardrails_node,
    retrieve_node,
    prompt_node,
    llm_node
)

def build_graph():

    graph = StateGraph(GraphState)

    graph.add_node("guardrails", guardrails_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("prompt", prompt_node)
    graph.add_node("llm", llm_node)

    graph.set_entry_point("guardrails")

    graph.add_edge("guardrails", "retrieve")
    graph.add_edge("retrieve", "prompt")
    graph.add_edge("prompt", "llm")
    graph.add_edge("llm", END)

    return graph.compile()