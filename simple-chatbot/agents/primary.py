from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from states.state import State

load_dotenv()


class PrimaryAgent:
    def __init__(self, state: State, temperature=0):
        self.state = state
        self.llm = ChatOpenAI(temperature=temperature)

    def update_state(self, key, value):
        self.state = {**self.state, key: value}

    def invoke(self, state: State):
        agent_msg = self.llm.invoke(state["messages"])
        agent_response = agent_msg.content
        self.update_state("messages", agent_response)
        return self.state
