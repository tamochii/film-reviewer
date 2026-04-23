from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"


def data_file(name: str) -> Path:
    return DATA_DIR / name
