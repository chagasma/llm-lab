from crewai import Crew

from agents.buscador import buscador
from agents.editor import editor
from agents.redator import redator
from tasks.buscar import buscar
from tasks.editar import editar
from tasks.redigir import redigir

equipe = Crew(
    agents=[buscador, redator, editor],
    tasks=[buscar, redigir, editar],
    verbose=True
)