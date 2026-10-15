import asyncio

import httpx
import pytest

from app.llm.models import ChatMessage, ToolCall
from app.llm.ollama import OllamaProvider


@pytest.mark.parametrize(
    "message",
    [
        {"role": "assistant", "content": "Hello"},
        {
            "role": "assistant",
            "tool_calls": [
                {"function": {"name": "lookup", "arguments": {"query": "hello"}}}
            ],
        },
    ],
)
def test_complete_returns_chat_message(message):
    async def run():
        transport = httpx.MockTransport(
            lambda request: httpx.Response(200, json={"message": message})
        )
        async with httpx.AsyncClient(
            transport=transport, base_url="http://ollama"
        ) as client:
            return await OllamaProvider(client, "test").complete([], [])

    result = asyncio.run(run())

    assert isinstance(result, ChatMessage)
    assert result.role == "assistant"
    assert result.content == message.get("content", "")
    assert [call.model_dump() for call in result.tool_calls] == message.get(
        "tool_calls", []
    )
    assert all(isinstance(call, ToolCall) for call in result.tool_calls)
