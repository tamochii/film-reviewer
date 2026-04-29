from __future__ import annotations

import requests

from backend.app.core.config import load_tmdb_settings


def search_movie(query: str, year: int) -> dict:
    settings = load_tmdb_settings()
    response = requests.get(
        f"{settings.base_url}/search/movie",
        params={"api_key": settings.api_key, "query": query, "year": year, "language": "zh-CN"},
        timeout=30,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        raise ValueError(f"No TMDB movie found for query={query!r}, year={year}")
    return results[0]


def get_movie_details(movie_id: int) -> dict:
    settings = load_tmdb_settings()
    response = requests.get(
        f"{settings.base_url}/movie/{movie_id}",
        params={"api_key": settings.api_key, "language": "zh-CN"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def hydrate_movie_record(movie: dict) -> dict:
    movie_id = movie.get("tmdb_id")
    if not movie_id:
        return movie
    details = get_movie_details(movie_id)
    return {
        **movie,
        "tmdb_id": details.get("id", movie_id),
        "title": details.get("title", movie.get("title", "")),
        "release_date": details.get("release_date", movie.get("release_date", "")),
        "overview": details.get("overview", movie.get("overview", "")),
        "source": "TMDB",
    }
