import json
from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from app.analytics.service import AnalyticsService
from app.llm.models import ToolDefinition
from app.tools.event_analytics import get_event_performance


class PerformanceArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start_date:date | None = None
    end_date: date | None = None

class ToolRegistry:
    def __init__(self, analytics: AnalyticsService) -> None:
        self._analytics = analytics

        self._definitions = [
            ToolDefinition(
                function={
                    "name": "get_event_performance",
                    "description": (
                        "Retrieve verified event views, "
                        "registrations, conversion rates, "
                        "ad spend and cost per registration. "
                        "Dates are optional YYYY-MM-DD values."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Start date YYYY-MM-DD",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date YYYY-MM-DD",
                            },
                        },
                        "additionalProperties": False,
                    },
                }
            )
        ]

    def allowed_definitions(self, allowed_names: list[str]) -> list[ToolDefinition]:
        return [
            definition
            for definition in self._definitions
            if definition.function["name"] in allowed_names
        ]

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        if name != "get_event_performance":
            return json.dumps({
                "error": "Unknown or unauthorized tool."
            })

        try:
            args = PerformanceArgs.model_validate(arguments)

            if (args.start_date and args.end_date and args.start_date > args.end_date):
                raise ValidationError("Invalid date range.")

            result = get_event_performance(
                analytics=self._analytics,
                start_date=(args.start_date.isoformat() if args.start_date else None),
                end_date=(args.end_date.isoformat() if args.end_date else None)
            )

            return json.dumps(result)
        
        except (ValidationError, ValueError) as exc:
            return json.dumps({
                "error": "Invalid analytics request.",
                "detail": str(exc)
            })