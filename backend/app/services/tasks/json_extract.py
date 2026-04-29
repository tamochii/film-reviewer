from __future__ import annotations

import json

from backend.app.clients.deepseek import chat_completion
from prompts import JSON_EXTRACTION_PROMPT


def parse_json_response(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        return {"parse_error": str(exc), "raw_output": raw}


def run(payload: dict) -> dict:
    prompt = JSON_EXTRACTION_PROMPT.format(review=payload.get("review", ""), movie_title=payload.get("movie_title", ""))
    raw = chat_completion([{"role": "user", "content": prompt}], temperature=0.0)
    return {"extraction": parse_json_response(raw)}
