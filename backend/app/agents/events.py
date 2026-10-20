from typing import Any, Literal
from pydantic import BaseModel, Field

EventType = Literal[
    "run.started",
    "agent.thinking",
    "tool.started",
    "tool.completed",
    "run.completed",
    "run.failed",
]


class AgentEvent(BaseModel):
    type: EventType
    agent_id: str
    run_id: str
    data: dict[str, Any] = Field(default_factory=dict)
