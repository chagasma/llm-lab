from crewai import Task

from agents.redator import redator

redigir = Task(
    description=(
        "1. Use os dados coletados de conteúdo para criar um post de LinkedIn atraente sobre {tema}.\n"
        "2. Incorpore palavras-chave de SEO de forma natural.\n"
        "3. Certifique-se de que o post esteja estruturado de forma cativante, com uma conclusão que faça o leitor refletir.\n"
    ),
    agent=redator,
    expected_output='Um texto de LinkedIn sobre {tema}'
)