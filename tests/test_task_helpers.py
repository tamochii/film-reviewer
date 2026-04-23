import json


def test_compute_accuracy_counts_matching_labels():
    from task1_classification import compute_accuracy

    records = [
        {"text": "a", "label": "积极"},
        {"text": "b", "label": "消极"},
        {"text": "c", "label": "积极"},
    ]

    predictions = {"a": "积极", "b": "积极", "c": "积极"}

    result = compute_accuracy(records, lambda text: predictions[text])

    assert result == 2 / 3


def test_parse_json_response_returns_error_payload_for_invalid_json():
    from task2_json_extract import parse_json_response

    result = parse_json_response("not json")

    assert "parse_error" in result
    assert result["raw_output"] == "not json"


def test_info_density_ignores_spaces():
    from task6_grid_search import info_density

    assert info_density("aa bb") == 2 / 4


def test_score_summary_rewards_broader_coverage():
    from task6_grid_search import score_summary

    short_summary = "奥德修斯踏上归乡之旅。"
    rich_summary = "奥德修斯在战后踏上归乡之旅，途中对抗风暴与求婚者，整体基调充满史诗冒险感。"

    assert score_summary(rich_summary) > score_summary(short_summary)


def test_evaluate_prompt_response_parses_valid_json(monkeypatch):
    from task5_prompt_evaluator import parse_evaluator_response

    payload = json.dumps({"clarity": 8, "completeness": 9, "format": 8}, ensure_ascii=False)

    result = parse_evaluator_response(payload)

    assert result["clarity"] == 8


def test_data_file_paths_are_relative_to_project_files():
    from paths import ROOT_DIR, data_file

    assert data_file("movie.json") == ROOT_DIR / "data" / "movie.json"
