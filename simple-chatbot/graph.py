from langgraph.graph import StateGraph

from agents.primary import primary_agent
from states.state import State


def create_graph():
    workflow = StateGraph(State)

    # --------------
    #  Nodes
    # --------------

    workflow.add_node("primary", primary_agent)

    # --------------
    #  Edges
    # --------------

    workflow.set_entry_point("primary")
    workflow.set_finish_point("primary")

    return workflow


def compile_workflow(workflow):
    graph = workflow.compile()
    return graph
