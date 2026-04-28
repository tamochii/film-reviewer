from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _env_or_default(name: str, default: str) -> str:
    return os.getenv(name, "").strip() or default


@dataclass(frozen=True)
class DeepSeekSettings:
    api_key: str
    base_url: str
    model: str


@dataclass(frozen=True)
class TMDBSettings:
    api_key: str
    base_url: str


@dataclass(frozen=True)
class Settings:
    deepseek_api_key: str
    deepseek_base_url: str
    deepseek_model: str
    tmdb_api_key: str
    tmdb_base_url: str


def load_settings() -> Settings:
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    deepseek_base_url = _env_or_default("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    deepseek_model = _env_or_default("DEEPSEEK_MODEL", "deepseek-chat")
    tmdb_api_key = os.getenv("TMDB_API_KEY", "").strip()
    tmdb_base_url = _env_or_default("TMDB_BASE_URL", "https://api.themoviedb.org/3")

    missing = []
    if not deepseek_api_key:
        missing.append("DEEPSEEK_API_KEY")
    if not tmdb_api_key:
        missing.append("TMDB_API_KEY")

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return Settings(
        deepseek_api_key=deepseek_api_key,
        deepseek_base_url=deepseek_base_url,
        deepseek_model=deepseek_model,
        tmdb_api_key=tmdb_api_key,
        tmdb_base_url=tmdb_base_url,
    )


def load_deepseek_settings() -> DeepSeekSettings:
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing required environment variable: DEEPSEEK_API_KEY")

    return DeepSeekSettings(
        api_key=api_key,
        base_url=_env_or_default("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        model=_env_or_default("DEEPSEEK_MODEL", "deepseek-chat"),
    )


def load_tmdb_settings() -> TMDBSettings:
    api_key = os.getenv("TMDB_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing required environment variable: TMDB_API_KEY")

    return TMDBSettings(
        api_key=api_key,
        base_url=_env_or_default("TMDB_BASE_URL", "https://api.themoviedb.org/3"),
    )
