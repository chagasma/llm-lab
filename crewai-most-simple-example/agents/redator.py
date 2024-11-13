from crewai import Agent

from tools.tools import search_tool, scrape_tool

redator = Agent(
    role="Redator de conteúdo",
    goal='Escreva um texto divertido e factualmente correto para o LinkedIn sobre {tema}',
    backstory='Você está trabalhando na redação de um artigo para o LinkedIn sobre {tema}.'
              'Você vai utilizar os dados coletados pelo Buscador de Conteudo para escrever um texto'
              'interessante, divertido e factualmente correto para o LinkedIn.',
    tools=[search_tool, scrape_tool],
    verbose=True
)