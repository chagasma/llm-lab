from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class Agent:
    def __init__(self, llm, prompt, tools, system_message):
        self.llm = llm
        self.prompt = prompt
        self.tools = tools
        self.system_message = system_message

    def create_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            MessagesPlaceholder(variable_name="messages")
        ])

        return prompt

    def create_agent(self):
        prompt = self.create_prompt()
        prompt = prompt.partial(system_message=self.system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in self.tools]))
        return prompt | self.llm.bind_tools(self.tools)
