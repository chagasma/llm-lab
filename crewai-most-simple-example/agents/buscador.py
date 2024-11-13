from crewai import Agent

from tools.tools import search_tool, scrape_tool

buscador = Agent(
    role="Buscador de conteúdo",
    goal='Busque conteúdo online sobre o tema {tema}',
    backstory='Você está trabalhando na criação de artigos para o LinkedIn sobre {tema}.'
              'Você vai fazer uma busca de informações na internet, coletá-las e agrupá-las.'
              'Seu trabalho servirá de base para o Redator de Conteúdo',
    tools=[search_tool, scrape_tool],
    verbose=True
)