from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from backend.app.models.schemas import RunListResponse, RunRecord
from backend.app.services.run_history import RunHistoryStore


router = APIRouter()


@router.get("/runs", response_model=RunListResponse)
def list_runs(task_id: str | None = Query(default=None), limit: int = Query(default=50, ge=1, le=200)) -> dict:
    return {"runs": RunHistoryStore().list_runs(task_id=task_id, limit=limit)}


@router.get("/runs/{run_id}", response_model=RunRecord)
def get_run(run_id: str) -> dict:
    record = RunHistoryStore().get_run(run_id)
    if not record:
        raise HTTPException(status_code=404, detail="Run not found")
    return record
