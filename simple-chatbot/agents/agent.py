from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from states.state import State

load_dotenv()


class Agent:
    """
    Base class for an intelligent agent using a language model. This class provides
    shared methods and structure for agents that interact with a language model,
    enabling state management and customizable interaction logic. Specific agents
    should extend this class and implement the `invoke` method for custom behavior.
    """

    def __init__(self, state: State, tools: list, temperature=0):
        """
        Initializes the Agent
        """
        self.state = state
        self.llm = ChatOpenAI(temperature=temperature).bind_tools(tools)

    def update_state(self, key, value):
        """
        Updates the agent's state by setting a new value for a specified key.
        """
        self.state = {**self.state, key: value}

    def invoke(self, state: State):
        """
        Abstract method to interact with the language model. This method must be
        implemented by subclasses to define specific interaction logic.
        """
        raise NotImplementedError("The `invoke` method must be implemented by specific agents")
