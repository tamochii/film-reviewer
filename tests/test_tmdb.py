from unittest.mock import Mock

import pytest


def test_search_movie_returns_first_result(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")
    monkeypatch.setenv("TMDB_API_KEY", "tmdb-key")

    def fake_get(url, params, timeout):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "results": [
                {"id": 42, "title": "Example Movie", "release_date": "2026-05-01"}
            ]
        }
        return response

    monkeypatch.setattr("requests.get", fake_get)

    from tmdb import search_movie

    result = search_movie("Example Movie", 2026)

    assert result["id"] == 42
    assert result["title"] == "Example Movie"


def test_search_movie_raises_when_no_results(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")
    monkeypatch.setenv("TMDB_API_KEY", "tmdb-key")

    def fake_get(url, params, timeout):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"results": []}
        return response

    monkeypatch.setattr("requests.get", fake_get)

    from tmdb import search_movie

    with pytest.raises(ValueError):
        search_movie("Missing Movie", 2026)


def test_hydrate_movie_record_refreshes_fields_from_tmdb(monkeypatch):
    monkeypatch.setenv("TMDB_API_KEY", "tmdb-key")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")

    from tmdb import hydrate_movie_record

    monkeypatch.setattr(
        "tmdb.get_movie_details",
        lambda movie_id: {
            "id": movie_id,
            "title": "奥德赛",
            "release_date": "2026-07-15",
            "overview": "TMDB overview",
        },
    )

    record = hydrate_movie_record({"tmdb_id": 1368337, "title": "旧标题"})

    assert record["title"] == "奥德赛"
    assert record["overview"] == "TMDB overview"
    assert record["source"] == "TMDB"
