from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "RAG Knowledge Assistant"
    app_version: str = "1.0.0"
    debug: bool = False

    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    upload_dir: Path = base_dir / "data" / "uploads"
    vector_store_dir: Path = base_dir / "data" / "vector_store"
    db_path: Path = base_dir / "data" / "metadata.db"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Chunking
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Retrieval
    top_k: int = 5

    # LLM (abstracted - starts with extractive mode)
    llm_provider: str = "extractive"  # "extractive" | "openai" | "anthropic"
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # CORS
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
