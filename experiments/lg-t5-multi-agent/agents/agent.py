from typing import Optional, List

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from states.state import State

load_dotenv()

class Agent:
    """
    Abstract base class for an intelligent agent using a language model.
    Provides a structure for state management and interaction logic.
    Subclasses should override the `__call__` method for specific use cases.
    """

    def __init__(self, state: State, name: str, prompt: ChatPromptTemplate, tools: Optional[List] = None, temperature: int = 0):
        """
        Initializes the Agent.

        Args:
            state (State): The initial state of the agent.
            name (str): The agent's name for identification.
            prompt (ChatPromptTemplate): The prompt template for generating model inputs.
            tools (Optional[List]): Optional tools the agent can use during reasoning.
            temperature (int): Temperature setting for the language model.
        """
        self.state = state
        self.name = name
        self.prompt = prompt
        self.llm = ChatOpenAI(temperature=temperature)
        if tools:
            self.llm = self.llm.bind_tools(tools)

        self.runnable = self.prompt | self.llm

    def __call__(self, state: State):
        """
        Defines the agent's behavior when invoked.
        Must be implemented by subclasses.

        Args:
            state (State): The input state to process.

        Returns:
            dict: The updated state after processing.
        """
        raise NotImplementedError("The `__call__` method must be implemented by subclasses.")