
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Document RAG Backend"
    DEBUG: bool = False

    DATABASE_URL: str
    REDIS_URL: str

    QDRANT_URL: str
    QDRANT_COLLECTION: str = "documents"

    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    REDIS_CHAT_TTL_SECONDS: int = 86400
    EMBEDDING_MODEL: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    EMBEDDING_DIMENSION: int = 384
    MAX_UPLOAD_SIZE_MB: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
