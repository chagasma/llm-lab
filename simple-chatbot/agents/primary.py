from agents.agent import Agent
from states.state import State


class PrimaryAgent(Agent):
    def invoke(self, state: State):
        agent_msg = self.llm.invoke(state["messages"])
        agent_response = agent_msg.content
        self.update_state("messages", agent_response)
        return self.state
