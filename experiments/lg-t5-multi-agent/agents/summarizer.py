from agents.agent import Agent
from states.state import State


class SummarizerAgent(Agent):
    def __call__(self, state: State):
        input_attribute = "messages"
        output_attribute = "messages"

        agent_msg = self.runnable.invoke(state[input_attribute])
        agent_response = agent_msg.content
        return {output_attribute: agent_response}