import functools

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from agents.agent import create_agent
from nodes.node import agent_node
from states.state import State
from tools.repl import python_repl
from tools.tavily import tavily_tool

load_dotenv()


llm = ChatOpenAI()

research_agent = create_agent(
    llm,
    [tavily_tool],
    system_message="You should provide accurate data for the chart_generator to use.",
)
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

chart_agent = create_agent(
    llm,
    [python_repl],
    system_message="Any charts you display will be visible by the user.",

)
chart_node = functools.partial(agent_node, agent=chart_agent, name="chart_generator")

"""
Define Tool Node
"""

tools = [tavily_tool, python_repl]
tool_node = ToolNode(tools)


def router(state):
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        return END
    return "continue"


"""
Define the Graph
"""

workflow = StateGraph(State)

workflow.add_node("Researcher", research_node)
workflow.add_node("chart_generator", chart_node)
workflow.add_node("call_tool", tool_node)

workflow.add_conditional_edges(
    "Researcher",
    router,
    {"continue": "chart_generator", "call_tool": "call_tool", END: END},
)

workflow.add_conditional_edges(
    "chart_generator",
    router,
    {"continue": "Researcher", "call_tool": "call_tool", END: END}
)

workflow.add_conditional_edges(
    "call_tool",
    lambda x: x["sender"],
    {
        "Researcher": "Researcher",
        "chart_generator": "chart_generator",
    }
)

workflow.add_edge(START, "Researcher")

graph = workflow.compile()

""" ------
 Run
"""

events = graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Fetch the UK's GDP over the past 5 years,"
                        " then draw a line graph of it."
                        " Once you code it up, finish."
            )
        ],
    },
    {"recursion_limit": 150},
)

for s in events:
    print(s)
    print("-----")
