from typing import Annotated

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages, StateGraph, START, END
from typing_extensions import TypedDict

from IPython.display import Image, display

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


workflow = StateGraph(State)

llm = ChatOpenAI()


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


workflow.add_node("chatbot", chatbot)

workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

graph = workflow.compile()

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except:
    pass


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["/q", "/quit", "/exit"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
