from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class Agent:
    def __init__(self, llm, tools, system_message):
        self.llm = llm
        self.tools = tools
        self.system_message = system_message

    @staticmethod
    def create_prompt():
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Você é um assistente de IA útil, colaborando com outros assistentes."
                " Use as ferramentas fornecidas para progredir na resposta à pergunta."
                " Se não conseguir responder completamente, tudo bem, outro assistente com ferramentas diferentes"
                " ajudará a partir de onde você parou. Execute o que puder para fazer progresso."
                " Se você ou qualquer outro assistente tiver a resposta final ou o resultado,"
                " prefixe sua resposta com FINAL ANSWER para que a equipe saiba que deve parar."
                " Você tem acesso às seguintes ferramentas: {tool_names}.\n\n"
                "{system_message}"
            ),
            MessagesPlaceholder(variable_name="messages")
        ])

        return prompt

    def create_agent(self, tools_required = False):
        prompt = self.create_prompt()
        prompt = prompt.partial(system_message=self.system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in self.tools]))
        if tools_required:
            return prompt | self.llm.bind_tools(self.tools, tool_choice='required')
        return prompt | self.llm.bind_tools(self.tools)