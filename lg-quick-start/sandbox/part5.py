from typing import Annotated

from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import ToolMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

load_dotenv()

memory = MemorySaver()


class State(TypedDict):
    messages: Annotated[list, add_messages]


workflow = StateGraph(State)

tool = TavilySearchResults(max_results=2)
tools = [tool]
llm = ChatOpenAI()
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


workflow.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges(
    "chatbot",
    tools_condition
)

workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")

graph = workflow.compile(
    checkpointer=memory,
    # This is new!
    interrupt_before=["tools"]
    # Note: can also interrupt __after__ tools, if desired.
    # interrupt_after=["tools"]
)

user_input = "I'm learning LangGraph. Could you do some research on it for me?"
config = {"configurable": {"thread_id": "2"}}
# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
existing_message.pretty_print()

events = graph.stream(None, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

answer = (
    "LangGraph is a library for building stateful, multi-actor applications with LLMs."
)
new_messages = [
    # The LLM API expects some ToolMessage to match its tool call. We'll satisfy that here.
    ToolMessage(content=answer, tool_call_id=existing_message.tool_calls[0]["id"]),
    # And then directly "put words in the LLM's mouth" by populating its response.
    AIMessage(content=answer),
]

"""
We annotated messages with the pre-built add_messages function. 
This instructs the graph to always append values to the existing list, rather than overwriting the list directly. 
The same logic is applied here, so the messages we passed to update_state were appended in the same way!

The update_state function operates as if it were one of the nodes in your graph! 
By default, the update operation uses the node that was last executed, but you can manually specify it below. 
Let's add an update and tell the graph to treat it as if it came from the "chatbot".
"""
new_messages[-1].pretty_print()
# graph.update_state(
#     config,
#     {"messages": new_messages},
# )

graph.update_state(
    config,
    {"messages": [AIMessage(content="I'm an AI expert!")]},
    # Which node for this function to act as. It will automatically continue
    # processing as if this node just ran.
    as_node="chatbot",
)

print("\n\nLast 2 messages;")
print(graph.get_state(config).values["messages"][-2:])

# snapshot = graph.get_state(config)
# print(snapshot.values["messages"][-3:])
# print(snapshot.next)

snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
print("Original")
print("Message ID", existing_message.id)
print(existing_message.tool_calls[0])
new_tool_call = existing_message.tool_calls[0].copy()
new_tool_call["args"]["query"] = "LangGraph human-in-the-loop workflow"
new_message = AIMessage(
    content=existing_message.content,
    tool_calls=[new_tool_call],
    # Important! The ID is how LangGraph knows to REPLACE the message in the state rather than APPEND this messages
    id=existing_message.id,
)

print("Updated")
print(new_message.tool_calls[0])
print("Message ID", new_message.id)
graph.update_state(config, {"messages": [new_message]})

print("\n\nTool calls")
print(graph.get_state(config).values["messages"][-1].tool_calls)

events = graph.stream(None, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

"""
You've used interrupt_before and update_state to manually modify the state as a part of a human-in-the-loop workflow. 
Interruptions and state modifications let you control how the agent behaves. 
Combined with persistent checkpointing, it means you can pause an action and resume at any point. 
Your user doesn't have to be available when the graph interrupts!

The graph code for this section is identical to previous ones. 
The key snippets to remember are to add .compile(..., interrupt_before=[...]) (or interrupt_after) if you want to explicitly pause the graph whenever it reaches a node. 
Then you can use update_state to modify the checkpoint and control how the graph should proceed.
"""
