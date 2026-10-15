import json
from collections.abc import Callable
from typing import Any

from app.llm.models import ToolDefinition
from app.tools.event_analytics import get_event_performance


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {
            "get_event_performance": get_event_performance
        }

        self._definitions = [
            ToolDefinition(
                function={
                    "name": "get_event_performance",
                    "description": (
                        "Get event category views, registrations "
                        "and conversion rates."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                    },
                }
            )
        ]

    def definitions(self) -> list[ToolDefinition]:
        return self._definitions

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        function = self._tools.get(name)

        if function is None:
            return json.dumps({"error": "Unknown or unauthorized tool."})

        if name == "get_event_performance" and arguments:
            return json.dumps({"error": "This tool accepts no arguments."})

        result = function(**arguments)

        return json.dumps(result)

    def allowed_definitions(self, allowed_names: list[str]) -> list[ToolDefinition]:
        return [
            definition
            for definition in self._definitions
            if definition.function["name"] in allowed_names
        ]
