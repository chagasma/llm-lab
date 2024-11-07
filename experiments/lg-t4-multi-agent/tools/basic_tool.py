from langchain_core.tools import tool


@tool
def basic_tool():
    """
    Essa tool retorna a temperatura atual em Cotia.
    Caso o usuário te pergunte qual a temperatura em Cotia use essa tool para saber essa informação.
    """
    return "A temperatura em Cotia agora é de 22 graus"