from __future__ import annotations

import pytest

from backend.app.core.config import get_config_status, load_deepseek_settings, load_tmdb_settings


def test_deepseek_settings_use_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", " deepseek-key ")
    monkeypatch.delenv("DEEPSEEK_BASE_URL", raising=False)
    monkeypatch.delenv("DEEPSEEK_MODEL", raising=False)

    settings = load_deepseek_settings()

    assert settings.api_key == "deepseek-key"
    assert settings.base_url == "https://api.deepseek.com/v1"
    assert settings.model == "deepseek-chat"


def test_tmdb_settings_require_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TMDB_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="TMDB_API_KEY"):
        load_tmdb_settings()


def test_config_status_does_not_expose_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    monkeypatch.setenv("TMDB_API_KEY", "secret-tmdb")
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-test")

    status = get_config_status()

    assert status == {
        "deepseek_configured": True,
        "tmdb_configured": True,
        "deepseek_base_url": "https://api.deepseek.com/v1",
        "deepseek_model": "deepseek-test",
        "tmdb_base_url": "https://api.themoviedb.org/3",
    }
    assert "secret" not in repr(status)
