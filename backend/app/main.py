from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Depends, HTTPException, Request

from app.config import Settings
from app.llm.ollama import LLMProviderError, OllamaProvider
from app.llm.provider import LLMProvider
from app.schemas import ChatRequest, ChatResponse
from app.services.chat import ChatService


@asynccontextmanager
async def lifeSpan(app: FastAPI):
    settings = Settings()

    async with httpx.AsyncClient(
        base_url=settings.ollama_base_url, timeout=120.0
    ) as client:
        app.state.llm_provider = OllamaProvider(
            client=client, model=settings.ollama_model
        )

        yield


app = FastAPI(title="AgentVerse API", version="0.2.0", lifespan=lifeSpan)


def get_chat_service(request: Request) -> ChatService:
    provider: LLMProvider = request.app.state.llm_provider
    return ChatService(provider)

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
