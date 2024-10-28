from langgraph.graph import add_messages
from typing_extensions import TypedDict, Annotated


class State(TypedDict):
    messages: Annotated[list, add_messages]
    db_info: Annotated[list, add_messages]

STATE: State = {
    "messages": [],
    "db_info": []
}