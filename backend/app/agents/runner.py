from app.agents.models import AgentDefinition, AgentResult
from app.llm.models import ChatMessage
from app.llm.provider import LLMProvider
from app.tools.registry import ToolRegistry


class AgentRunner:
    def __init__(self, provider: LLMProvider, tools: ToolRegistry) -> None:
        self._provider = provider
        self._tools = tools

    async def run(self, agent: AgentDefinition, task: str) -> AgentResult:
        messages = [
            ChatMessage(role="system", content=agent.instructions),
            ChatMessage(role="user", content=task),
        ]

        tool_definitions = self._tools.allowed_definitions(agent.allowed_tools)

        tools_used: list[str] = []

        for step in range(1, agent.max_steps + 1):
            response = await self._provider.complete(
                messages=messages, tools=tool_definitions
            )

            messages.append(response)

            # The model has finished without requesting tools.
            if not response.tool_calls:
                if not response.content.strip():
                    return AgentResult(
                        agent_id=agent.id,
                        response="The mode returned no answer.",
                        steps=step,
                        tools_used=tools_used,
                        status="failed",
                    )

                return AgentResult(
                    agent_id=agent.id,
                    response=response.content,
                    steps=step,
                    tools_used=tools_used,
                    status="completed",
                )

            # Do not execute tools if we cannot make
            # another model call to interpret their result.
            if step == agent.max_steps:
                break

            for tool_call in response.tool_calls:
                name = tool_call.function.name
                arguments = tool_call.function.arguments

                # Enforce authorization in the backend.
                if name not in agent.allowed_tools:
                    result = '{"error": "Tool not permitted."}'
                else:
                    result = self._tools.execute(name=name, arguments=arguments)
                    tools_used.append(name)

                messages.append(
                    ChatMessage(role="tool", tool_name=name, content=result)
                )

        return AgentResult(
            agent_id=agent.id,
            response="Execution stopped: step limit reached.",
            steps=agent.max_steps,
            tools_used=tools_used,
            status="step_limit_reached",
        )
