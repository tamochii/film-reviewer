from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.config import get_config_status


router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "config": get_config_status()}
