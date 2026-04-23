from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


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
    deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").strip()
    deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip()
    tmdb_api_key = os.getenv("TMDB_API_KEY", "").strip()
    tmdb_base_url = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3").strip()

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
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").strip(),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip(),
    )


def load_tmdb_settings() -> TMDBSettings:
    api_key = os.getenv("TMDB_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing required environment variable: TMDB_API_KEY")

    return TMDBSettings(
        api_key=api_key,
        base_url=os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3").strip(),
    )
