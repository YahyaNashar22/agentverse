from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Depends, HTTPException, Request

from app.config import Settings
from app.llm.ollama import LLMProviderError, OllamaProvider
from app.llm.provider import LLMProvider
from app.schemas import ChatRequest, ChatResponse
from app.services.chat import ChatService
from app.agents.marketing import marketing_agent
from app.agents.models import AgentResult
from app.agents.runner import AgentRunner
from app.schemas import AgentRunRequest
from app.tools.registry import ToolRegistry


@asynccontextmanager
async def lifeSpan(app: FastAPI):
    settings = Settings()

    async with httpx.AsyncClient(
        base_url=settings.ollama_base_url, timeout=120.0
    ) as client:
        app.state.llm_provider = OllamaProvider(
            client=client, model=settings.ollama_model
        )

        app.state.tool_registry = ToolRegistry()

        app.state.agent_runner = AgentRunner(
            provider=app.state.llm_provider, tools=app.state.tool_registry
        )

        yield


app = FastAPI(title="AgentVerse API", version="0.2.0", lifespan=lifeSpan)


def get_chat_service(request: Request) -> ChatService:
    provider: LLMProvider = request.app.state.llm_provider
    return ChatService(provider)


def get_agent_runner(request: Request) -> AgentRunner:
    return request.app.state.agent_runner


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "agentVerse-api"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, service: ChatService = Depends(get_chat_service)):
    try:
        reply = await service.chat(body.message)
        return ChatResponse(reply=reply)

    except LLMProviderError as exc:
        raise HTTPException(
            status_code=502, detail="The LLM provider failed to generate a response."
        ) from exc


@app.post("/api/agents/marketing/run", response_model=AgentResult)
async def run_marketing_agent(body: AgentRunRequest, runner: AgentRunner = Depends(get_agent_runner)):
    try:
        return await runner.run(agent=marketing_agent, task=body.task)

    except LLMProviderError as exc:
        raise HTTPException(status_code=502, detail="The LLM provider failed.") from exc