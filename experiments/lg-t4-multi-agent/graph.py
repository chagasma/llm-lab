import functools

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from agents.agent import Agent
from nodes.node import agent_node
from prompts.primary_prompts import PRIMARY_PROMPT
from prompts.scheduling_prompts import SCHEDULING_PROMPT
from states.state import State
from tools.basic_tool import basic_tool
from tools.calendar_tools import create_calendar_event

load_dotenv()

llm = ChatOpenAI()

# ----------------------------
#    Agents instances
# ----------------------------

primary_agent_tools = [basic_tool]
primary_agent_instance = Agent(llm, primary_agent_tools, PRIMARY_PROMPT)

scheduling_agent_tools = [create_calendar_event]
scheduling_agent_instance = Agent(llm, scheduling_agent_tools, SCHEDULING_PROMPT)

# ----------------------------
#    Create Graph
# ----------------------------

def create_graph():
    workflow = StateGraph(State)

    # ----------------------------
    #    Agents Nodes
    # ----------------------------

    primary_assistant = primary_agent_instance.create_agent()
    primary_assistant_node = functools.partial(agent_node, agent=primary_assistant, name="primary_assistant")

    scheduling_assistant = scheduling_agent_instance.create_agent()
    scheduling_assistant_node = functools.partial(agent_node, agent=scheduling_assistant, name="scheduling_assistant")

    workflow.add_node("primary_assistant", primary_assistant_node)
    workflow.add_node("scheduling_assistant", scheduling_assistant_node)

    # ----------------------------
    #    Tool Node
    # ----------------------------

    tools = [
        create_calendar_event,
        basic_tool
    ]

    tool_node = ToolNode(tools)
    workflow.add_node("call_tool", tool_node)

    # ----------------------------
    #    Router
    # ----------------------------

    def router(state):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "call_tool"
        if "FINAL ANSWER" in last_message.content:
            return END
        return "continue"

    # ----------------------------
    #    Edges
    # ----------------------------

    workflow.add_edge(START, "primary_assistant")

    workflow.add_conditional_edges(
        "primary_assistant",
        router,
        {"continue": "scheduling_assistant", "call_tool": "call_tool", END: END},
    )

    workflow.add_conditional_edges(
        "scheduling_assistant",
        router,
        {"continue": "primary_assistant", "call_tool": "call_tool", END: END},
    )

    workflow.add_conditional_edges(
        "call_tool",
        lambda x: x["sender"],
        {
            "primary_assistant": "primary_assistant",
            "scheduling_assistant": "scheduling_assistant",
        },
    )

    return workflow

# ----------------------------
#    Compile Workflow
# ----------------------------

def compile_workflow(workflow):
    checkpointer = MemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)
    return graph

# ----------------------------
#    Graph Visualization
# ----------------------------

def graph_visualization(app, image_path):
    try:
        graph = app.get_graph(xray=True)
        image_bytes = graph.draw_mermaid_png()

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        print(f"Graph saved to {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")