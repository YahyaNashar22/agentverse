import httpx
from pydantic import BaseModel, ValidationError


class OllamaMessage(BaseModel):
    content: str


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
        try:
            response = await self._client.post(
                "/api/chat",
                json={
                    "model": self._model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "think": False,
                },
            )

            response.raise_for_status()
            result = OllamaChatResponse.model_validate(response.json())

            if not result.message.content.strip():
                raise LLMProviderError("Ollama returned an empty response")

            return result.message.content

        except httpx.HTTPError as exc:
            raise LLMProviderError("Unable to communicate with Ollama.") from exc

        except (ValueError, ValidationError) as exc:
            raise LLMProviderError("Ollama returned an invalid response.") from exc
