from __future__ import annotations

import json

from client import chat_completion
from paths import data_file
from prompts import COT_PLOT_ANALYSIS_PROMPT, PLOT_ANALYSIS_PROMPT
from tmdb import hydrate_movie_record


def run_analysis(prompt_template: str, plot_summary: str) -> str:
    prompt = prompt_template.format(plot_summary=plot_summary)
    return chat_completion([{"role": "user", "content": prompt}], temperature=0.0)


def main() -> None:
    with open(data_file("movie.json"), "r", encoding="utf-8") as file:
        movie = hydrate_movie_record(json.load(file))

    with open(data_file("plot_summary.txt"), "r", encoding="utf-8") as file:
        extra_summary = file.read().strip()

    plot_summary = f"TMDB剧情简介：{movie['overview']}\n\n扩展剧情简介：{extra_summary}"

    plain = run_analysis(PLOT_ANALYSIS_PROMPT, plot_summary)
    cot = run_analysis(COT_PLOT_ANALYSIS_PROMPT, plot_summary)

    print("=== Without CoT ===")
    print(plain)
    print()
    print("=== With CoT ===")
    print(cot)


if __name__ == "__main__":
    main()
