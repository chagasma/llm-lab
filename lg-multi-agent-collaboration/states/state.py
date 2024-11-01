import operator
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str
