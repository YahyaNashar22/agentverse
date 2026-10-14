import asyncio

from app.services.chat import ChatService


class FakeLLMProvider:
    async def generate(self, prompt: str) -> str:
        return f"Fake response to: {prompt}"

    
def test_chat_service():
    provider = FakeLLMProvider()
    service = ChatService(provider)

    result = asyncio.run(service.chat("Hello AgentVerse"))

    assert result == "Fake response to: Hello AgentVerse"