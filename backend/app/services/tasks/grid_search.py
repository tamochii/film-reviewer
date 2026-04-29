from __future__ import annotations

import json

from backend.app.clients.deepseek import chat_completion
from backend.app.core.paths import data_file
from prompts import GRID_PROMPT_VARIANT_1, GRID_PROMPT_VARIANT_2, GRID_PROMPT_VARIANT_3


VARIANTS = {"variant_1": GRID_PROMPT_VARIANT_1, "variant_2": GRID_PROMPT_VARIANT_2, "variant_3": GRID_PROMPT_VARIANT_3}


def info_density(text: str) -> float:
    compact = text.replace(" ", "")
    if not compact:
        return 0.0
    return len(set(compact)) / len(compact)


def score_summary(text: str) -> float:
    categories = [
        ["主角", "少年", "电次", "他"],
        ["目标", "生活", "关系", "命运", "接近"],
        ["冲突", "反转", "危险", "战斗", "恶魔", "追杀"],
        ["基调", "残酷", "浪漫", "青春", "黑暗", "宿命"],
    ]
    coverage = sum(1 for keywords in categories if any(keyword in text for keyword in keywords))
    return info_density(text) + coverage * 0.2 - (len(text) / 1000)


def _default_overview() -> str:
    with open(data_file("movie.json"), "r", encoding="utf-8") as file:
        return json.load(file).get("overview", "")


def run(payload: dict) -> dict:
    overview = payload.get("overview") or _default_overview()
    variants = []
    for name, prompt_template in VARIANTS.items():
        prompt = prompt_template.format(overview=overview)
        summary = chat_completion([{"role": "user", "content": prompt}], temperature=0.0)
        variants.append({"name": name, "summary": summary, "length": len(summary), "density": info_density(summary), "score": score_summary(summary)})
    best = max(variants, key=lambda item: item["score"], default={"name": ""})
    return {"variants": variants, "best_variant": best["name"]}
