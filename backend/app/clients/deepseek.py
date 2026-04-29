from __future__ import annotations

from typing import Any

import requests

from backend.app.core.config import load_deepseek_settings


def chat_completion(messages: list[dict[str, str]], temperature: float = 0.0) -> str:
    settings = load_deepseek_settings()
    response = requests.post(
        f"{settings.base_url}/chat/completions",
        headers={"Authorization": f"Bearer {settings.api_key}", "Content-Type": "application/json"},
        json={"model": settings.model, "messages": messages, "temperature": temperature},
        timeout=60,
    )
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    return payload["choices"][0]["message"]["content"].strip()
