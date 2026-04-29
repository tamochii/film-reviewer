from __future__ import annotations

import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"


def data_file(name: str) -> Path:
    return DATA_DIR / name


def database_path() -> Path:
    configured = os.getenv("FILM_REVIEWER_DB_PATH", "").strip()
    if configured:
        return Path(configured)
    return DATA_DIR / "runs.sqlite3"
