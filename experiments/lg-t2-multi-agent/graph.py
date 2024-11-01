import functools

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agents.agent import create_agent
from nodes.node import agent_node
from prompts.system_prompt import SYSTEM_PROMPT, PRIMARY_PROMPT, CONVERSATION_PROMPT
from states.state import State
from tools.tavily import tavily_tool

load_dotenv()

llm = ChatOpenAI()


def router(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "search_tool"
    else:
        return END


def create_graph():
    workflow = StateGraph(State)

    primary_message = ""
    primary_agent = create_agent(llm, CONVERSATION_PROMPT, [tavily_tool], system_message=primary_message)
    primary_node = functools.partial(agent_node, agent=primary_agent, name="primary")

    workflow.add_node("primary", primary_node)

    tool_node = ToolNode(tools=[tavily_tool])
    workflow.add_node("search_tool", tool_node)

    workflow.add_conditional_edges(
        "primary",
        router
    )

    workflow.add_edge(START, "primary")
    workflow.add_edge("search_tool", "primary")

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
