from __future__ import annotations

import json

from backend.app.clients.deepseek import chat_completion
from prompts import PROMPT_EVALUATOR_PROMPT, SIMPLE_PROMPT


def parse_evaluator_response(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        return {"parse_error": str(exc), "raw_output": raw}


def run(payload: dict) -> dict:
    target_prompt = payload.get("target_prompt") or SIMPLE_PROMPT
    prompt = PROMPT_EVALUATOR_PROMPT.format(target_prompt=target_prompt)
    raw = chat_completion([{"role": "user", "content": prompt}], temperature=0.0)
    return {"evaluation": parse_evaluator_response(raw)}
