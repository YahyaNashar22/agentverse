import asyncio
from collections.abc import AsyncIterator
from contextlib import suppress

from app.agents.events import AgentEvent
from app.agents.models import AgentDefinition
from app.agents.runner import AgentRunner


async def stream_agent_run(
    runner: AgentRunner, agent: AgentDefinition, task: str
) -> AsyncIterator[str]:

    queue: asyncio.Queue[AgentEvent | None] = asyncio.Queue()

    def on_event(event: AgentEvent) -> None:
        queue.put_nowait(event)

    async def execute() -> None:
        try:
            await runner.run(agent=agent, task=task, on_event=on_event)
        except Exception:
            # The runner emits run.failed on ordinary errors.
            # Log the traceback here rather than expose it.
            import logging

            logging.getLogger(__name__).exception("Agent execution failed")
        finally:
            queue.put_nowait(None)

    worker = asyncio.create_task(execute())

    try:
        while True:
            event = await queue.get()

            if event is None:
                break

            yield event.model_dump_json() + "\n"

    finally:
        if not worker.done():
            worker.cancel()

        with suppress(asyncio.CancelledError):
            await worker
