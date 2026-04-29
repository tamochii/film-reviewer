from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException

from backend.app.core.config import get_config_status
from backend.app.models.schemas import RunRecord, TaskListResponse
from backend.app.services.run_history import RunHistoryStore
from backend.app.services.tasks import run_task


router = APIRouter()

TASK_METADATA = [
    {"id": "classification", "label": "Task 1 · Sentiment Classification", "description": "Compare zero-shot and few-shot sentiment classification.", "result_type": "classification"},
    {"id": "json_extract", "label": "Task 2 · JSON Extraction", "description": "Extract structured metadata from a movie review.", "result_type": "json"},
    {"id": "cot_compare", "label": "Task 3 · CoT Comparison", "description": "Compare plain and chain-of-thought plot analysis.", "result_type": "comparison"},
    {"id": "roleplay", "label": "Task 4 · Roleplay Chat", "description": "Chat with a sharp professional movie critic persona.", "result_type": "chat"},
    {"id": "prompt_evaluator", "label": "Task 5 · Prompt Evaluator", "description": "Score a target prompt across evaluation dimensions.", "result_type": "evaluation"},
    {"id": "grid_search", "label": "Task 6 · Grid Search", "description": "Compare summary prompt variants and highlight the best result.", "result_type": "table"},
]


@router.get("/tasks", response_model=TaskListResponse)
def list_tasks() -> dict:
    return {"tasks": TASK_METADATA}


@router.post("/tasks/{task_id}/runs", response_model=RunRecord)
def create_run(task_id: str, payload: dict[str, Any]) -> dict:
    if task_id not in {task["id"] for task in TASK_METADATA}:
        raise HTTPException(status_code=404, detail="Task not found")
    started = time.perf_counter()
    model = str(get_config_status()["deepseek_model"])
    store = RunHistoryStore()
    try:
        output = run_task(task_id, payload)
    except Exception as exc:
        duration_ms = int((time.perf_counter() - started) * 1000)
        store.save_run(task_id=task_id, status="error", input_data=payload, output_data={}, error=str(exc), model=model, duration_ms=duration_ms)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    duration_ms = int((time.perf_counter() - started) * 1000)
    return store.save_run(task_id=task_id, status="success", input_data=payload, output_data=output, error=None, model=model, duration_ms=duration_ms)
