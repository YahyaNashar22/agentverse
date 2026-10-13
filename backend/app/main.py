from fastapi import FastAPI

app = FastAPI(
    title = "AgentVerse API",
    version = "0.1.0",
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "agentVerse-api"
    }