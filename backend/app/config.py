from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
