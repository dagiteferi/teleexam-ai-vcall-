from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App settings
    app_env: str = "development"
    log_level: str = "INFO"
    port: int = 8001

    # Provider selection
    llm_provider: str = "groq"
    stt_provider: str = "assemblyai"
    tts_provider: str = "cartesia"
    embedding_provider: str = "voyage"

    # API keys
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    cerebras_api_key: Optional[str] = None
    assemblyai_api_key: Optional[str] = None
    deepgram_api_key: Optional[str] = None
    cartesia_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    voyage_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None

    # Models
    groq_model: str = "llama-3.1-8b-instant"

    # Database
    sqlalchemy_database_url: str = (
        "postgresql://user:password@localhost:5432/teleexam"
    )

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # LiveKit
    livekit_url: str = "ws://localhost:7880"
    livekit_api_key: Optional[str] = None
    livekit_api_secret: Optional[str] = None


settings = Settings()