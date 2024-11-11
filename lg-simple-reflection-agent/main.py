import asyncio
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph

load_dotenv()

# --------------------------------------
#   llm
# --------------------------------------

llm = ChatOpenAI()

# --------------------------------------
#   Generate
# --------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an essay assistant tasked with writing excellent 5-paragraph essays."
            " Generate the best essay possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generate = prompt | llm

# # --------------------------------------
#
# essay = ""
# request = HumanMessage(
#     content="Write an essay on why the little prince is relevant in modern childhood"
# )
#
# for chunk in generate.stream({"messages": [request]}):
#     print(chunk.content, end="")
#     essay += chunk.content
#
# # --------------------------------------

# --------------------------------------
#   Reflect
# --------------------------------------

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a teacher grading an essay submission. Generate critique and recommendations for the user's submission."
            " Provide detailed recommendations, including requests for length, depth, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
reflect = reflection_prompt | llm

# # --------------------------------------
#
# reflection = ""
# for chunk in reflect.stream({"messages": [request, HumanMessage(content=essay)]}):
#     print(chunk.content, end="")
#     reflection += chunk.content
#
# # --------------------------------------
#
# for chunk in generate.stream({
#     "messages": [request, AIMessage(content=essay), HumanMessage(content=reflection)],
# }):
#     print(chunk.content, end="")

# --------------------------------------
#   Define Graph
# --------------------------------------

class State(TypedDict):
    messages: Annotated[list, add_messages]

async def generation_node(state: State) -> State:
    return {"messages": [await generate.ainvoke(state["messages"])]}

async def reflection_node(state: State) -> State:
    cls_map = {"ai": HumanMessage, "human": AIMessage}
    translated = [state["messages"][0]] + [
        cls_map[msg.type](content=msg.content) for msg in state["messages"][1:]
    ]
    res = await reflect.ainvoke(translated)
    return {"messages": [HumanMessage(content=res)]}

workflow = StateGraph(State)
workflow.add_node("generate", generation_node)
workflow.add_node("reflect", reflection_node)
workflow.add_edge(START, "generate")

def should_continue(state: State):
    if len(state["messages"]) > 6:
        return END
    return "reflect"

workflow.add_conditional_edges("generate", should_continue)
workflow.add_edge("reflect", "generate")

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# --------------------------------------

config = {"configurable": {"thread_id": "1"}}

# --------------------------------------

async def execute_event(graph, config):
    async for event in graph.astream({
        "messages": [
            HumanMessage(
                content="Generate an essay on the topicality of The Little Prince and its message in modern life"
            )
        ]
    }, config):
        print(event)
        print("----")

# --------------------------------------

asyncio.run(execute_event(graph, config))

# --------------------------------------

state = graph.get_state(config)

ChatPromptTemplate.from_messages(state.values["messages"]).pretty_print()