from typing import Annotated

from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import ToolMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import add_messages, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel
from typing_extensions import TypedDict

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]
    ask_human: bool


class RequestAssistance(BaseModel):
    """
    Escalate the conversation to an expert.
    Use this if you are unable to assist directly or if the user requires support beyond your permissions.
    To use this function, relay the user's 'request' so the expert can provide the right guidance.
    """
    request: str


tool = TavilySearchResults(max_results=2)
tools = [tool]
llm = ChatOpenAI()
llm_with_tools = llm.bind_tools(tools + [RequestAssistance])

"""
Next, define the chatbot node. 
The primary modification here is flip the ask_human flag if we see that the chat bot has invoked the RequestAssistance flag.
"""


def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    ask_human = False
    if (
            response.tool_calls
            and response.tool_calls[0]["name"]
    ):
        ask_human = True

    return {"messages": [response], "ask_human": ask_human}


workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", ToolNode(tools=[tool]))


def create_response(response: str, ai_message: AIMessage):
    return ToolMessage(
        content=response,
        tool_call_id=ai_message.tool_call[0]["id"]
    )


def human_node(state: State):
    new_messages = []
    if not isinstance(state["messages"][-1], ToolMessage):
        # Typically, the user will have updated the state during the interrupt.
        # If they choose not to, we will include a placeholder ToolMessage to
        # let the LLM continue.
        new_messages.append(
            create_response("No response from human.", state["messages"][-1])
        )
    return {
        "messages": new_messages,
        "ask_human": False,
    }


workflow.add_node("human", human_node)

"""
Next, define the conditional logic. 
The select_next_node will route to the human node if the flag is set. 
Otherwise, it lets the prebuilt tools_condition function choose the next node.

Recall that the tools_condition function simply checks to see if the chatbot has responded with any tool_calls in its response message. 
If so, it routes to the action node. Otherwise, it ends the graph.
"""


def select_next_node(state: State):
    if state["ask_human"]:
        return "human"
    # Otherwise, we can route as before
    return tools_condition(state)


workflow.add_conditional_edges(
    "chatbot",
    select_next_node,
    {"human": "human", "tools": "tools", END: END}
)

workflow.add_edge("tools", "chatbot")
workflow.add_edge("human", "chatbot")
workflow.add_edge(START, "chatbot")

memory = MemorySaver()

graph = workflow.compile(
    checkpointer=memory,
    # We interrupt before 'human' here instead.
    interrupt_before=["human"],
)

user_input = "I need some expert guidance for building this AI agent. Could you request assistance for me?"
config = {"configurable": {"thread_id": "1"}}
# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

snapshot = graph.get_state(config)
print(snapshot.next)

ai_message = snapshot.values["messages"][-1]
human_response = (
    "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
    " It's much more reliable and extensible than simple autonomous agents."
)
tool_message = create_response(human_response, ai_message)
graph.update_state(config, {"messages": [tool_message]})

events = graph.stream(None, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
