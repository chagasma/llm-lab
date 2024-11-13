from dotenv import load_dotenv

from crew.equipe import equipe

load_dotenv()

tema_artigo = 'Alimentação saudável'
entradas = {"tema": tema_artigo}
resultado = equipe.kickoff(inputs=entradas)

print(resultado)