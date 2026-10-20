
import asyncio

from app.agents.events import AgentEvent
from app.agents.marketing import marketing_agent
from app.agents.runner import AgentRunner
from app.llm.models import ChatMessage, FunctionCall, ToolCall
from app.tools.registry import ToolRegistry


class FakeProvider:
    def __init__(self):
        self.calls = 0

    async def generate(self, prompt: str) -> str:
        return "Not used"

    async def complete(self, messages, tools):
        self.calls += 1

        if self.calls == 1:
            return ChatMessage(
                role="assistant",
                tool_calls=[
                    ToolCall(
                        function=FunctionCall(
                            name="get_event_performance",
                            arguments={},
                        )
                    )
                ],
            )

        return ChatMessage(
            role="assistant",
            content="Corporate has the highest conversion rate.",
        )


def test_agent_emits_execution_events():
    events: list[AgentEvent] = []

    runner = AgentRunner(
        provider=FakeProvider(),
        tools=ToolRegistry(),
    )

    result = asyncio.run(
        runner.run(
            agent=marketing_agent,
            task="Analyze our event data.",
            on_event=events.append,
        )
    )

    assert result.status == "completed"

    event_types = [event.type for event in events]

    assert event_types == [
        "run.started",
        "agent.thinking",
        "tool.started",
        "tool.completed",
        "agent.thinking",
        "run.completed",
    ]

    assert len({event.run_id for event in events}) == 1
    assert all(
        event.agent_id == marketing_agent.id
        for event in events
    )
