from __future__ import annotations

import json

from client import chat_completion
from prompts import PROMPT_EVALUATOR_PROMPT, SIMPLE_PROMPT


def parse_evaluator_response(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        return {"parse_error": str(exc), "raw_output": raw}


def evaluate_prompt(target_prompt: str) -> dict:
    prompt = PROMPT_EVALUATOR_PROMPT.format(target_prompt=target_prompt)
    raw = chat_completion([{"role": "user", "content": prompt}], temperature=0.0)
    return parse_evaluator_response(raw)


def main() -> None:
    print(json.dumps(evaluate_prompt(SIMPLE_PROMPT), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
