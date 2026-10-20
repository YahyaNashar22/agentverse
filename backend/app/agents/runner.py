from collections.abc import Callable
from uuid import uuid4

from agents.events import AgentEvent
from app.agents.models import AgentDefinition, AgentResult
from app.llm.models import ChatMessage
from app.llm.provider import LLMProvider
from app.tools.registry import ToolRegistry

EventCallback = Callable[[AgentEvent], None]


class AgentRunner:
    def __init__(self, provider: LLMProvider, tools: ToolRegistry) -> None:
        self._provider = provider
        self._tools = tools

    async def run(
        self, agent: AgentDefinition, task: str, on_event: EventCallback | None = None
    ) -> AgentResult:

        run_id = str(uuid4())

        def emit(event_type, data=None):
            if on_event is not None:
                on_event(
                    AgentEvent(
                        type=event_type,
                        agent_id=agent.id,
                        run_id=run_id,
                        data=data or {},
                    )
                )

        messages = [
            ChatMessage(role="system", content=agent.instructions),
            ChatMessage(role="user", content=task),
        ]

        tool_definitions = self._tools.allowed_definitions(agent.allowed_tools)

        tools_used: list[str] = []

        emit("run.started", {"task": task})
        try:
            for step in range(1, agent.max_steps + 1):
                emit("agent.thinking", {"step": step})
                response = await self._provider.complete(
                    messages=messages, tools=tool_definitions
                )

                messages.append(response)

                # The model has finished without requesting tools.
                if not response.tool_calls:
                    if not response.content.strip():
                        result = AgentResult(
                            agent_id=agent.id,
                            response="The mode returned no answer.",
                            steps=step,
                            tools_used=tools_used,
                            status="failed",
                        )
                        emit("run.failed", {"reason": result.response})
                        return result

                    result = AgentResult(
                        agent_id=agent.id,
                        response=response.content,
                        steps=step,
                        tools_used=tools_used,
                        status="completed",
                    )
                    emit("run.completed", {"result": result.model_dump()})
                    return result

                # Do not execute tools if we cannot make
                # another model call to interpret their result.
                if step == agent.max_steps:
                    break

                for tool_call in response.tool_calls:
                    name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    emit("tool.started", {"tool": name})

                    # Enforce authorization in the backend.
                    if name not in agent.allowed_tools:
                        tool_result = '{"error": "Tool not permitted."}'
                    else:
                        tool_result = self._tools.execute(
                            name=name, arguments=arguments
                        )
                        tools_used.append(name)

                    emit("tool.completed", {"tool": name, "result": tool_result})
                    messages.append(
                        ChatMessage(role="tool", tool_name=name, content=tool_result)
                    )

            result = AgentResult(
                agent_id=agent.id,
                response="Execution stopped: step limit reached.",
                steps=agent.max_steps,
                tools_used=tools_used,
                status="step_limit_reached",
            )
            emit("run.failed", {"reason": result.response})
            return result

        except Exception:
            emit("run.failed", {"reason": "Agent execution failed."})
            raise
