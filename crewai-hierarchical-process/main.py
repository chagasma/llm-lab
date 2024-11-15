from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

load_dotenv()

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# ----------------
#  Agents
# ----------------

# Agents are defined with attributes for backstory, cache, and verbose mode
researcher = Agent(
    role='Pesquisador',
    goal='Conduzir uma análise aprofundada',
    backstory='Analista de dados experiente com talento para descobrir tendências ocultas.',
    cache=True,
    verbose=True,
    tools=[search_tool, scrape_tool],  # This can be optionally specified; defaults to an empty list
    use_system_prompt=True,  # Enable or disable system prompts for this agent
    max_rpm=30,  # Limit on the number of requests per minute
    max_iter=5  # Maximum number of iterations for a final answer
)
writer = Agent(
    role='Escritor',
    goal='Criar conteúdo envolvente',
    backstory='Escritor criativo apaixonado por contar histórias em domínios técnicos.',
    cache=True,
    verbose=True,
    # tools=[]  # Optionally specify tools; defaults to an empty list
    use_system_prompt=True,  # Enable or disable system prompts for this agent
    max_rpm=30,  # Limit on the number of requests per minute
    max_iter=5  # Maximum number of iterations for a final answer
)

# ----------------
#  Tasks
# ----------------

research = Task(
    description=(
        "Realize uma pesquisa detalhada sobre {topic}, buscando fontes confiáveis e dados relevantes para sustentar a análise."
    ),
    agent=researcher,
    expected_output=(
        "Uma lista com pelo menos 5 fontes relevantes, incluindo resumos e links para acesso."
    )
)

write = Task(
    description=(
        "Com base na pesquisa realizada, redija um artigo informativo e engajador sobre {topic}, considerando o público-alvo."
    ),
    agent=writer,
    expected_output=(
        "Um artigo formatado em markdown, com cerca de 500 palavras, incluindo título e subtítulos."
    )
)


# ----------------
#  Crew
# ----------------

llm = ChatOpenAI(temperature=0)

# Establishing the crew with a hierarchical process and additional configurations
project_crew = Crew(
    tasks=[research, write],  # Tasks to be delegated and executed under the manager's supervision
    agents=[researcher, writer],
    manager_llm=llm,  # Mandatory if manager_agent is not set
    process=Process.hierarchical,  # Specifies the hierarchical management approach
    memory=True,  # Enable memory usage for enhanced task execution
    manager_agent=None,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
    planning=True,  # Enable planning feature for pre-execution strategy
)

# ----------------
#  Running
# ----------------

topic = 'Os impactos da IA generativa na educação'
inputs = {"topic": topic}
results = project_crew.kickoff(inputs=inputs)

print(results)