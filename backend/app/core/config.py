from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RAG Knowledge Assistant"
    app_env: str = "development"
    api_prefix: str = "/api"
    log_level: str = "INFO"

    upload_dir: str = "backend/data/uploads"
    vector_store_dir: str = "backend/data/vector_store"

    max_upload_mb: int = 10
    chunk_size: int = Field(default=800, ge=200, le=2000)
    chunk_overlap: int = Field(default=120, ge=0, le=500)
    top_k: int = Field(default=4, ge=1, le=10)

    embedding_provider: str = "sentence-transformers"
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_provider: str = "mock"
    llm_model: str = "local"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
