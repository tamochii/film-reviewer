from __future__ import annotations

import json

from backend.app.clients.deepseek import chat_completion
from backend.app.core.paths import data_file
from prompts import FEW_SHOT_PROMPT, SIMPLE_PROMPT


def normalize_label(raw: str) -> str:
    text = raw.strip()
    if "积极" in text:
        return "积极"
    if "消极" in text:
        return "消极"
    return text


def classify(prompt_template: str, review: str) -> str:
    prompt = prompt_template.format(review=review)
    return normalize_label(chat_completion([{"role": "user", "content": prompt}], temperature=0.0))


def _load_reviews(payload: dict) -> list[dict]:
    if "reviews" in payload:
        return payload["reviews"]
    with open(data_file("reviews.json"), "r", encoding="utf-8") as file:
        return json.load(file)["reviews"]


def _run_variant(records: list[dict], prompt_template: str) -> dict:
    items = []
    correct = 0
    for item in records:
        predicted = classify(prompt_template, item["text"])
        is_correct = predicted == item.get("label")
        correct += int(is_correct)
        items.append({"id": item.get("id"), "text": item["text"], "gold": item.get("label"), "predicted": predicted, "correct": is_correct})
    return {"accuracy": correct / len(records) if records else 0.0, "items": items}


def run(payload: dict) -> dict:
    records = _load_reviews(payload)
    return {"zero_shot": _run_variant(records, SIMPLE_PROMPT), "few_shot": _run_variant(records, FEW_SHOT_PROMPT)}
