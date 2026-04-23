from __future__ import annotations

import json

from client import chat_completion
from paths import data_file
from prompts import JSON_EXTRACTION_PROMPT
from tmdb import hydrate_movie_record


def parse_json_response(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        return {"parse_error": str(exc), "raw_output": raw}


def extract_review_metadata(review: str, movie_title: str) -> dict:
    prompt = JSON_EXTRACTION_PROMPT.format(review=review, movie_title=movie_title)
    raw = chat_completion([{"role": "user", "content": prompt}], temperature=0.0)
    return parse_json_response(raw)


def main() -> None:
    with open(data_file("reviews.json"), "r", encoding="utf-8") as file:
        data = json.load(file)

    with open(data_file("movie.json"), "r", encoding="utf-8") as file:
        movie = hydrate_movie_record(json.load(file))

    for item in data["reviews"]:
        result = extract_review_metadata(item["text"], movie["title"])
        print(f"Review {item['id']}:")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
