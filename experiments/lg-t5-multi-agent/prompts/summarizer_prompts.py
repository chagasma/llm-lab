from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_MESSAGE = dedent(f'''
Você é um agente especializado em gerar resumos de conversas
As conversas seguem uma estrutura de mensagens dos usuários e dos assistentes
Faça um resumo conciso e eficiente das conversas apresentadas
''')

summarizer_prompt = ChatPromptTemplate.from_messages([
    ('system', SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="messages")
])
