from __future__ import annotations

import json

from client import chat_completion
from paths import data_file
from prompts import GRID_PROMPT_VARIANT_1, GRID_PROMPT_VARIANT_2, GRID_PROMPT_VARIANT_3
from tmdb import hydrate_movie_record


def info_density(text: str) -> float:
    compact = text.replace(" ", "")
    if not compact:
        return 0.0
    return len(set(compact)) / len(compact)


def score_summary(text: str) -> float:
    categories = [
        ("主角", ["奥德修斯", "主角", "马特·达蒙"]),
        ("目标", ["归乡", "回家", "返回", "伊萨卡"]),
        ("冲突", ["冲突", "阻挠", "对抗", "危机", "求婚者", "风暴", "怪物"]),
        ("基调", ["史诗", "冒险", "宏大", "基调"]),
    ]
    coverage = 0
    for _, keywords in categories:
        if any(keyword in text for keyword in keywords):
            coverage += 1
    return info_density(text) + coverage * 0.2 - (len(text) / 1000)


def summarize(prompt_template: str, overview: str) -> str:
    prompt = prompt_template.format(overview=overview)
    return chat_completion([{"role": "user", "content": prompt}], temperature=0.0)


def main() -> None:
    with open(data_file("movie.json"), "r", encoding="utf-8") as file:
        movie = hydrate_movie_record(json.load(file))

    variants = {
        "variant_1": GRID_PROMPT_VARIANT_1,
        "variant_2": GRID_PROMPT_VARIANT_2,
        "variant_3": GRID_PROMPT_VARIANT_3,
    }

    best_name = ""
    best_score = float("-inf")
    for name, prompt_template in variants.items():
        result = summarize(prompt_template, movie["overview"])
        length = len(result)
        density = info_density(result)
        score = score_summary(result)
        print(f"{name}:")
        print(result)
        print(f"length={length}, density={density:.3f}, score={score:.3f}")
        print()
        if score > best_score:
            best_name = name
            best_score = score

    print(f"Best variant: {best_name}")


if __name__ == "__main__":
    main()
