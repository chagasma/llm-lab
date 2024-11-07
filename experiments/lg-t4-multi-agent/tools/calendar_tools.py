import json
import os
from datetime import timedelta, datetime
from typing import List, Optional

import requests
from dotenv import load_dotenv

from langchain_core.tools import tool

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")


@tool
def get_calendar_events(start_time: str, end_time: str):
    """
    Consulta eventos em um calendário específico para um usuário.
    Retorna todos os eventos dentro do intervalo de tempo especificado.
    Exemplo de como escrever o start_time e o end_time:
    {
        "start_time": "2024-11-02T00:00:00Z",
        "end_time": "2024-11-02T23:59:59Z"
    }
    O retorno da tool será um array, se ele estiver vazio significa que não há eventos marcados
    Se for o caso, apenas informe que não há eventos marcados
    """
    endpoint = "/get-calendar-events"
    url = f"{API_BASE_URL}{endpoint}"

    payload = {
        "user_id": "nay",
        "calendar_id": os.getenv('CALENDAR_ID'),
        "start_time": start_time,
        "end_time": end_time
    }

    res = requests.post(url, json=payload)

    res.raise_for_status()

    return json.dumps(res.json(), ensure_ascii=False)


@tool
def create_calendar_event(
        summary: str,
        description: str,
        start_time: str,
        attendees: List[str],
        end_time: Optional[str] = None,
) -> str:
    """
    Cria um novo evento no calendário.
    Args:
        summary: Título do evento (ex: "Consulta - Atendimento Autismo")
        description: Descrição detalhada do evento
        start_time: Data e hora de início no formato "YYYY-MM-DDTHH:MM:SSZ"
        attendees: Lista de emails dos participantes
        end_time: (Opcional) Data e hora de término. Se não fornecido, será 1 hora após o início
    """
    if not end_time:
        start_datetime = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_datetime = start_datetime + timedelta(hours=1)
        end_time = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        'user_id': "nay",
        'summary': summary,
        'description': description,
        'start_time': start_time,
        'end_time': end_time,
        'attendees': attendees,
        'calendar_id': os.getenv('CALENDAR_ID')
    }

    endpoint = "/create-calendar-event"
    url = f"{API_BASE_URL}{endpoint}"

    res = requests.post(url, json=payload)

    res.raise_for_status()

    return json.dumps(res.json(), ensure_ascii=False)
