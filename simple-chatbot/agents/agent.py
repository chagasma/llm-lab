from states.state import State


class Agent:
    def __init__(self, state: State, prompt: str):
        self.state = state
        self.prompt = prompt

    def update_state(self, key, value):
        self.state = {**self.state, key: value}
