from langgraph.graph import StateGraph

from agents.summarizer import SummarizerAgent
from prompts.summarizer_prompts import summarizer_prompt
from states.state import State


def create_graph():
    workflow = StateGraph(State)

    # agent instance
    summarizer = SummarizerAgent(State, name="summarizer", prompt=summarizer_prompt)

    # add node
    workflow.add_node(summarizer.name, summarizer)

    # add edges
    workflow.set_entry_point(summarizer.name)
    workflow.set_finish_point(summarizer.name)

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