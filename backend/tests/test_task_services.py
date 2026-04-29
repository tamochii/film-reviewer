from __future__ import annotations

import json

import pytest

from backend.app.services.tasks import classification, cot_compare, grid_search, json_extract, prompt_evaluator, roleplay


def test_classification_returns_accuracy_comparison(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(classification, "chat_completion", lambda messages, temperature=0.0: "积极")

    result = classification.run({"reviews": [{"id": 1, "text": "great", "label": "积极"}]})

    assert result["zero_shot"]["accuracy"] == 1.0
    assert result["few_shot"]["accuracy"] == 1.0
    assert result["zero_shot"]["items"][0]["predicted"] == "积极"


def test_json_extract_reports_parse_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(json_extract, "chat_completion", lambda messages, temperature=0.0: "not-json")

    result = json_extract.run({"review": "solid", "movie_title": "Test Movie"})

    assert "parse_error" in result["extraction"]
    assert result["extraction"]["raw_output"] == "not-json"


def test_cot_compare_returns_plain_and_cot(monkeypatch: pytest.MonkeyPatch) -> None:
    replies = iter(["plain analysis", "cot analysis"])
    monkeypatch.setattr(cot_compare, "chat_completion", lambda messages, temperature=0.0: next(replies))

    result = cot_compare.run({"plot_summary": "plot"})


    assert result == {"plain": "plain analysis", "cot": "cot analysis"}


def test_roleplay_appends_assistant_reply(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(roleplay, "chat_completion", lambda messages, temperature=0.7: "sharp reply")

    result = roleplay.run({"message": "hello", "history": []})

    assert result["reply"] == "sharp reply"
    assert result["history"][-1] == {"role": "assistant", "content": "sharp reply"}


def test_prompt_evaluator_parses_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        prompt_evaluator,
        "chat_completion",
        lambda messages, temperature=0.0: json.dumps({"clarity": 8, "completeness": 7, "format": 9}),
    )

    result = prompt_evaluator.run({"target_prompt": "classify this"})

    assert result["evaluation"]["clarity"] == 8


def test_grid_search_selects_best_variant(monkeypatch: pytest.MonkeyPatch) -> None:
    replies = iter(["少年生活", "恶魔战斗冲突", "主角目标冲突黑暗基调"])
    monkeypatch.setattr(grid_search, "chat_completion", lambda messages, temperature=0.0: next(replies))

    result = grid_search.run({"overview": "movie overview"})

    assert len(result["variants"]) == 3
    assert result["best_variant"] == "variant_3"
