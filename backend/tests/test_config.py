from app.core.config import Settings


def test_cors_origins_default() -> None:
    settings = Settings(_env_file=None)
    assert settings.cors_allowed_origins_list == ["http://localhost:5173"]


def test_cors_origins_from_csv_env(monkeypatch) -> None:
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        "https://rag-demo.vercel.app, https://staging.example.com",
    )

    settings = Settings(_env_file=None)

    assert settings.cors_allowed_origins_list == [
        "https://rag-demo.vercel.app",
        "https://staging.example.com",
    ]

    monkeypatch.delenv("CORS_ALLOWED_ORIGINS", raising=False)
