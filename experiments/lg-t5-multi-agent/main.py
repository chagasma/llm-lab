import os
from textwrap import dedent

from graph.graph import create_graph, compile_workflow, graph_visualization

workflow = create_graph()
graph = compile_workflow(workflow)

if os.getenv("AMBIENT") == 'DEV':
    graph_visualization(graph, "./docs/img/graph.png")

if __name__ == "__main__":
    summary_input = dedent('''
    Conversa:
    
    user: Olá, meu nome é Mauro
    assistant: Olá, Mauro! Como posso ajudá-lo?
    user: Eu gostaria de realizar um agendamento por favor!
    assistant: Temos horários disponíveis para a próxima terça 14h
    user: Show! Pode marcar!
    assistant: Agendamento marcado.
    ''')

    summary = ""
    events = graph.stream(
        {"messages": summary_input},
        stream_mode="values"
    )

    for event in events:
        summary = event['messages'][-1].content

    print(summary)
