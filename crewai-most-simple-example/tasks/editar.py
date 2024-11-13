from crewai import Task

from agents.editor import editor

editar = Task(
    description=(
        "Revisar a postage do LinkedIn em questão quanto a erros gramaticais e alinhamento com uma voz descontraída."
    ),
    agent=editor,
    expected_output='Um texto de LinkedIn pronto para a publicação'
)