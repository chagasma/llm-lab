from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from agents.primary import PrimaryAgent
from edges.conditions import should_search_database
from states.state import State, STATE
from tools.db_tools import search_database

tools = [search_database]
search_database_tool = ToolNode(tools)


def create_graph():
    workflow = StateGraph(State)

    # --------------
    #  Agents instances
    # --------------

    primary = PrimaryAgent(STATE, tools=tools)

    # --------------
    #  Nodes
    # --------------

    workflow.add_node(
        "primary",
        lambda state: primary.invoke(state)
    )

    # workflow.add_node(
    #     "search_db",
    #     lambda state: search_database(state)
    # )

    workflow.add_node("search_db", search_database_tool)

    # --------------
    #  Edges
    # --------------

    workflow.set_entry_point("primary")

    workflow.add_conditional_edges("primary", should_search_database)

    workflow.set_finish_point("primary")

    return workflow


def compile_workflow(workflow):
    checkpointer = MemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)
    return graph


def graph_visualization(app, image_path):
    try:
        graph = app.get_graph(xray=True)
        image_bytes = graph.draw_mermaid_png()

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        print(f"Graph saved to {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
