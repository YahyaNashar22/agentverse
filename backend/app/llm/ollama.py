import httpx
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

from app.llm.models import ChatMessage, ToolCall, ToolDefinition


class OllamaMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)


class OllamaChatResponse(BaseModel):
    message: OllamaMessage


class LLMProviderError(Exception):
    pass


class OllamaProvider:
    def __init__(
        self,
        client: httpx.AsyncClient,
        model: str,
    ) -> None:
        self._client = client
        self._model = model

    async def generate(self, prompt: str) -> str:
        response = await self.complete(
            messages=[ChatMessage(role="user", content=prompt)], tools=[]
        )

        if not response.content.strip():
            raise LLMProviderError("Ollama returned no text.")

        return response.content

    async def complete(
        self, messages: list[ChatMessage], tools: list[ToolDefinition]
    ) -> ChatMessage:
        try:
            response = await self._client.post(
                "/api/chat",
                json={
                    "model": self._model,
                    "messages": [
                        message.model_dump(exclude_none=True, exclude_defaults=True)
                        for message in messages
                    ],
                    "tools": [tool.model_dump() for tool in tools],
                    "stream": False,
                    "think": False,
                },
            )

            response.raise_for_status()
            result = OllamaChatResponse.model_validate(response.json())

            return ChatMessage(
                role=result.message.role,
                content=result.message.content,
                tool_calls=result.message.tool_calls,
            )

        except httpx.HTTPError as exc:
            raise LLMProviderError("Unable to communicate with Ollama.") from exc

        except (ValueError, ValidationError) as exc:
            raise LLMProviderError("Ollama returned an invalid response.") from exc
