from crewai import Task

from agents.buscador import buscador

buscar = Task(
    description=(
        "1. Priorize as útlimas tendências, os principais atores e as notícias mais relevantes sobre {tema}.\n"
        "2. Identifique o público-alvo, considerando seus interesses e pontos de dor.\n"
        "3. Inclua palavras chave de SEO qe dados ou fontes relevantes."
    ),
    agent=buscador,
    expected_output='Um plano de tendências sobre {tema}, com as palavras mais relevantes de SEO e as últimas notícias.'
)