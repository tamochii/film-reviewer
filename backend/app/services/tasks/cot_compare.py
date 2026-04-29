from __future__ import annotations

import json

from backend.app.clients.deepseek import chat_completion
from backend.app.core.paths import data_file
from prompts import COT_PLOT_ANALYSIS_PROMPT, PLOT_ANALYSIS_PROMPT


def _default_plot_summary() -> str:
    with open(data_file("movie.json"), "r", encoding="utf-8") as file:
        movie = json.load(file)
    with open(data_file("plot_summary.txt"), "r", encoding="utf-8") as file:
        extra_summary = file.read().strip()
    return f"TMDB剧情简介：{movie.get('overview', '')}\n\n扩展剧情简介：{extra_summary}"


def _analyze(prompt_template: str, plot_summary: str) -> str:
    prompt = prompt_template.format(plot_summary=plot_summary)
    return chat_completion([{"role": "user", "content": prompt}], temperature=0.0)


def run(payload: dict) -> dict:
    plot_summary = payload.get("plot_summary") or _default_plot_summary()
    return {"plain": _analyze(PLOT_ANALYSIS_PROMPT, plot_summary), "cot": _analyze(COT_PLOT_ANALYSIS_PROMPT, plot_summary)}
