from langchain_core.messages import HumanMessage, AIMessage


def agent_node(state, agent, name):
    result = agent.invoke(state)
    # print(f'RESULT: {result}')
    return {
        "messages": [AIMessage(content=result.content, name=name)]
    }