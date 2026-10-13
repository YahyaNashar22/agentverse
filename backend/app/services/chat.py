from app.llm.provider import LLMProvider


class ChatService:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def chat(self, message: str) -> str:
        return await self._provider.generate(message)
