from langchain_core.messages import HumanMessage

from states.state import State
from langchain.tools import tool

# @tool
# def search_database(state: State):
#     """
#     Consulte a base de dados quando perguntarem sobre quantos produtos há nela
#     """
#     mock_info = "20 produtos na base de dados"
#     state["db_info"].append(HumanMessage(role="system", content=mock_info))
#     return {"db_info": state["db_info"]}

@tool
def search_database():
    """
    Consulte a base de dados quando perguntarem sobre quantos produtos há nela
    """
    return "Há 20 registros na base de dados"