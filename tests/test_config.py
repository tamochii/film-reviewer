import pytest


def test_load_deepseek_settings_only_requires_deepseek_key(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.com/v1")
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-chat")
    monkeypatch.delenv("TMDB_API_KEY", raising=False)

    from config import load_deepseek_settings

    settings = load_deepseek_settings()

    assert settings.api_key == "deepseek-key"
    assert settings.base_url == "https://example.com/v1"
    assert settings.model == "deepseek-chat"


def test_load_settings_reads_required_environment(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.com/v1")
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-chat")
    monkeypatch.setenv("TMDB_API_KEY", "tmdb-key")
    monkeypatch.setenv("TMDB_BASE_URL", "https://tmdb.example/api")

    from config import load_settings

    settings = load_settings()

    assert settings.deepseek_api_key == "deepseek-key"
    assert settings.deepseek_base_url == "https://example.com/v1"
    assert settings.deepseek_model == "deepseek-chat"
    assert settings.tmdb_api_key == "tmdb-key"
    assert settings.tmdb_base_url == "https://tmdb.example/api"


def test_load_settings_rejects_missing_required_keys(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("TMDB_API_KEY", raising=False)

    from config import load_settings

    with pytest.raises(RuntimeError) as exc_info:
        load_settings()

    message = str(exc_info.value)
    assert "DEEPSEEK_API_KEY" in message
    assert "TMDB_API_KEY" in message


def test_load_tmdb_settings_only_requires_tmdb_key(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("TMDB_API_KEY", "tmdb-key")
    monkeypatch.setenv("TMDB_BASE_URL", "https://tmdb.example/api")

    from config import load_tmdb_settings

    settings = load_tmdb_settings()

    assert settings.api_key == "tmdb-key"
    assert settings.base_url == "https://tmdb.example/api"
