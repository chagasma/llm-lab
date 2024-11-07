from typing import Literal

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()

members = ["primary_assistant", "scheduling_assistant"]
SUPERVISOR_PROMPT = (
    "Você é um supervisor encarregado de gerenciar uma conversa entre os"
    " seguintes trabalhadores: {members}. Dado o seguinte pedido do usuário,"
    " responda com o próximo agente a agir. Cada agente realizará uma"
    " tarefa e responderá com seus resultados e status. Quando terminar,"
    " responda com FINISH."
)

options = ["FINISH"] + members

class RouteResponse(BaseModel):
    next: Literal[*options]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SUPERVISOR_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Dada a conversa acima, quem deve agir a seguir?"
            " Ou devemos FINISH? Selecione uma das opções: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

llm = ChatOpenAI()

def supervisor_agent(state):
    supervisor_chain = prompt | llm.with_structured_output(RouteResponse)
    return supervisor_chain.invoke(state)