import functools

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from agents.agent import Agent
from nodes.node import agent_node
from prompts.system_prompt import PRIMARY_PROMPT, EVENT_PROMPT
from states.state import State
from tools.db_tools import get_events, create_event
from tools.tavily import tavily_tool

load_dotenv()

llm = ChatOpenAI()


def primary_router(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls[0]["name"] == tavily_tool.name:
        return "search_tool"
    else:
        return END


def event_router(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls[0]["name"] == get_events.name:
        return "get_events_tool"
    elif last_message.tool_calls[0]["name"] == create_event.name:
        return "create_event_tool"
    else:
        return END


# -----------------------
#    Agents instances
# -----------------------

primary_message = ""
primary_agent_instance = Agent(llm, PRIMARY_PROMPT, [tavily_tool], primary_message)

event_message = ""
event_agent_instance = Agent(llm, EVENT_PROMPT, [get_events, create_event], event_message)


def create_graph():
    workflow = StateGraph(State)

    # -----------------------
    #    Agents Nodes
    # -----------------------

    primary_agent = primary_agent_instance.create_agent()
    primary_node = functools.partial(agent_node, agent=primary_agent, name="primary")

    event_agent = event_agent_instance.create_agent()
    event_node = functools.partial(agent_node, agent=event_agent, name="event")

    workflow.add_node("primary", primary_node)
    workflow.add_node("event", event_node)

    # -----------------------
    #    Tools Nodes
    # -----------------------

    search_tool = ToolNode(tools=[tavily_tool])
    workflow.add_node("search_tool", search_tool)

    get_events_tool = ToolNode(tools=[get_events])
    workflow.add_node("get_events_tool", get_events_tool)

    create_event_tool = ToolNode(tools=[create_event])
    workflow.add_node("create_event_tool", create_event_tool)

    # -----------------------
    #    Edges
    # -----------------------

    workflow.add_conditional_edges(
        "primary",
        primary_router
    )

    workflow.add_conditional_edges(
        "event",
        event_router
    )

    workflow.add_edge(START, "primary")
    workflow.add_edge("search_tool", "primary")

    workflow.add_edge("get_events_tool", "event")
    workflow.add_edge("create_event_tool", "event")

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
