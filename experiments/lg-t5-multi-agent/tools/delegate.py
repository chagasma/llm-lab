from typing import Literal

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class DelegateInput(BaseModel):
    worker: Literal["primary_assistant", "scheduling_assistant", "event_assistant"] = Field(
        description="Os agentes que você pode escolher para delegar as tasks. As opções são: 'primary_assistant', 'scheduling_assistant' ou 'event_assistant'."
    )

class Delegate(BaseTool):
    name: str = "delegate-tool"
    description: str = "Tool utilizada para delegar a task atual para um dos agentes: 'primary_assistant', 'scheduling_assistant' ou 'event_assistant'."

    def _run(self, worker: Literal["primary_assistant", "scheduling_assistant", "event_assistant"]) -> str:
        return worker

    def _arun(self):
        raise NotImplementedError("The `_arun` method not implemented yet.")