from langchain_core.tools import tool


@tool
def get_events():
    """Get all the events from a database"""
    return [
        {
            "event_name": "Reunião de Planejamento",
            "start_date": "2024-11-15T10:00:00",
            "end_date": "2024-11-15T11:00:00",
            "local": "Sala de Conferências 1",
            "description": "Discussão sobre o planejamento estratégico para o próximo trimestre."
        },
        {
            "event_name": "Workshop de Inovação",
            "start_date": "2024-11-20T14:00:00",
            "end_date": "2024-11-20T17:00:00",
            "local": "Auditório Principal",
            "description": "Workshop voltado para novas técnicas e práticas de inovação."
        },
        {
            "event_name": "Evento de Networking",
            "start_date": "2024-12-01T18:00:00",
            "end_date": "2024-12-01T21:00:00",
            "local": "Espaço de Eventos",
            "description": "Oportunidade para conhecer outros profissionais da área."
        }
    ]


@tool
def create_event(event_name: str, start_date: str, end_date: str, local: str, description: str):
    """Create an event into the database"""
    return {
        "event_name": event_name,
        "start_date": start_date,
        "end_date": end_date,
        "local": local,
        "description": description
    }
