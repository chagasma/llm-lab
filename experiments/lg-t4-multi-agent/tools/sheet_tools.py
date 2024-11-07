import json
import os
import requests
from typing import Optional

from langchain_core.tools import tool

API_BASE_URL = os.getenv("API_BASE_URL")

@tool
def get_sheets_events(worksheet_name: Optional[str] = None) -> str:
    """
    Consulta todos os registros de uma planilha específica.
    Se o nome de uma worksheet for fornecido, retorna os registros dessa worksheet específica.
    """
    spreadsheet_id = os.getenv('SPREADSHEET_ID')

    endpoint = "/get_sheets_all_records"
    url = f"{API_BASE_URL}{endpoint}"

    payload = {
        "spreadsheet_id": spreadsheet_id,
        "worksheet_name": worksheet_name
    }

    res = requests.post(url, json=payload)

    res.raise_for_status()

    return json.dumps(res.json(), ensure_ascii=False)
