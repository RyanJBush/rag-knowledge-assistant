from app.core.config import get_settings


def test_default_storage_paths_are_backend_relative() -> None:
    get_settings.cache_clear()
    settings = get_settings()

    assert settings.upload_dir == "data/uploads"
    assert settings.vector_store_dir == "data/vector_store"
