from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

load_dotenv()

# ----------------
#  Agents
# ----------------

# Agents are defined with attributes for backstory, cache, and verbose mode
joke_teller = Agent(
    role='Contador de Piadas',
    goal='Criar piadas engraçadas baseadas no input do usuário: {user_input}',
    backstory='Humorista bem-humorado e criativo, capaz de transformar qualquer tema em uma piada.',
    cache=True,
    verbose=True,
    # tools=[],  # This can be optionally specified; defaults to an empty list
    use_system_prompt=True,  # Enable or disable system prompts for this agent
    max_rpm=30,  # Limit on the number of requests per minute
    max_iter=5  # Maximum number of iterations for a final answer
)

explainer = Agent(
    role='Explicador',
    goal='Fornecer explicações claras e objetivas para perguntas simples. O usuário te fez essa pergunta: {user_input}',
    backstory='Professor apaixonado por ensinar conceitos complexos de forma acessível.',
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

tell_joke = Task(
    description=(
        "Baseado no tema fornecido, crie uma piada engraçada e original.\n"
        "Input do usuário: {user_input}"
    ),
    agent=joke_teller,
    expected_output=(
        "Uma piada curta e engraçada baseada no tema especificado pelo usuário."
    )
)

explain_topic = Task(
    description=(
        "Forneça uma explicação clara e objetiva para a pergunta do usuário."
    ),
    agent=explainer,
    expected_output=(
        "Uma explicação concisa e acessível sobre o tema especificado pelo usuário.\n"
        "Input do usuário: {user_input}"
    )
)


# ----------------
#  Crew
# ----------------

llm = ChatOpenAI(temperature=0)

# Establishing the crew with a hierarchical process and additional configurations
project_crew = Crew(
    tasks=[tell_joke, explain_topic],  # Tasks to be delegated and executed under the manager's supervision
    agents=[joke_teller, explainer],
    manager_llm=llm,  # Mandatory if manager_agent is not set
    process=Process.hierarchical,  # Specifies the hierarchical management approach
    memory=True,  # Enable memory usage for enhanced task execution
    manager_agent=None,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
    planning=True,  # Enable planning feature for pre-execution strategy
)

# ----------------
#  Running
# ----------------

user_input = 'Me conte uma piada sobre carros'
inputs = {"user_input": user_input}
results = project_crew.kickoff(inputs=inputs)

print(results)