from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph

from agents.primary import PrimaryAgent
from states.state import State, STATE


def create_graph():
    workflow = StateGraph(State)

    # --------------
    #  Agents instances
    # --------------

    primary = PrimaryAgent(STATE)

    # --------------
    #  Nodes
    # --------------

    workflow.add_node(
        "primary",
        lambda state: primary.invoke(state)
    )

    # --------------
    #  Edges
    # --------------

    workflow.set_entry_point("primary")
    workflow.set_finish_point("primary")

    return workflow


def compile_workflow(workflow):
    checkpointer = MemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)
    return graph
