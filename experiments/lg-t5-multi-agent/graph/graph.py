from langgraph.graph import StateGraph

from prompts.chief_prompts import chief_prompt

from agents.chief import ChiefAgent
from states.state import State
from tools.delegate import Delegate


def create_graph():
    workflow = StateGraph(State)

    # tools
    delegate_tool = Delegate()

    # agent instance
    chief = ChiefAgent(State, name="chief", prompt=chief_prompt, tools=[delegate_tool])

    # add node
    workflow.add_node(chief.name, chief)
    workflow.add_node(delegate_tool.name, delegate_tool)

    # add edges
    workflow.set_entry_point(chief.name)

    workflow.add_edge(chief.name, delegate_tool.name)

    workflow.set_finish_point(delegate_tool.name)

    return workflow


def compile_workflow(workflow):
    graph = workflow.compile()
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