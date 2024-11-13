from crewai import Agent

from tools.tools import search_tool, scrape_tool

editor = Agent(
    role="Editor de conteúdo",
    goal='Editar um texto de LinkedIn para que ele tenha um tom mais informal.',
    backstory='Você está trabalhando na edição de um artigo para o LinkedIn.'
              'Você vai receber um texto do Redator de conteído e editá-lo para o tom de voz'
              'mais informal e divertido',
    tools=[search_tool, scrape_tool],
    verbose=True
)