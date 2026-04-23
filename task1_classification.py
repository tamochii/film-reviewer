from __future__ import annotations

import json

from client import chat_completion
from paths import data_file
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


def compute_accuracy(records: list[dict], predictor) -> float:
    correct = 0
    for item in records:
        if predictor(item["text"]) == item["label"]:
            correct += 1
    return correct / len(records)


def run_experiment(records: list[dict], prompt_template: str, name: str) -> float:
    print(f"=== {name} ===")
    correct = 0
    for item in records:
        predicted = classify(prompt_template, item["text"])
        if predicted == item["label"]:
            correct += 1
        print(f"Review {item['id']}: gold={item['label']} predicted={predicted}")
    accuracy = correct / len(records)
    print(f"{name} accuracy: {accuracy:.2%}")
    print()
    return accuracy


def main() -> None:
    with open(data_file("reviews.json"), "r", encoding="utf-8") as file:
        reviews = json.load(file)["reviews"]

    run_experiment(reviews, SIMPLE_PROMPT, "Zero-shot")
    run_experiment(reviews, FEW_SHOT_PROMPT, "Few-shot")


if __name__ == "__main__":
    main()
