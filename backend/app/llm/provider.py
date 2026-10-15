from typing import Protocol

from app.llm.models import ChatMessage, ToolDefinition


class LLMProvider(Protocol):
    async def generate(self, prompt: str) -> str: ...

    async def complete(
        self, messages: list[ChatMessage], tools: list[ToolDefinition]
    ) -> ChatMessage: ...
