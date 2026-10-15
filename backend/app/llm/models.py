from typing import Any, Literal

from pydantic import BaseModel, Field


class FunctionCall(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)

    
class ToolCall(BaseModel):
    function: FunctionCall

    
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_name: str | None = None

    
class ToolDefinition(BaseModel):
    type: Literal["function"] = "function"
    function: dict[str, Any]