from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from states.state import State

load_dotenv()

llm = ChatOpenAI(temperature=0)


def primary_agent(state: State):
    return {"messages": [llm.invoke(state["messages"])]}
