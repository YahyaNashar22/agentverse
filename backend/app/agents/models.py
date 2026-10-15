from pydantic import BaseModel, Field


class AgentDefinition(BaseModel):
    id: str
    name: str
    instructions: str
    allowed_tools: list[str] = Field(default_factory=list)
    max_steps: int = Field(default=4, ge=1, le=10)


class AgentResult(BaseModel):
    agent_id: str
    response: str
    steps: int
    tools_used: list[str]
    status: str