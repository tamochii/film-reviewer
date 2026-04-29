from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class TaskMeta(BaseModel):
    id: str
    label: str
    description: str
    result_type: str


class TaskListResponse(BaseModel):
    tasks: list[TaskMeta]


class RunRecord(BaseModel):
    id: str
    task_id: str
    status: Literal["success", "error"]
    input: dict[str, Any]
    output: dict[str, Any]
    error: str | None
    model: str
    duration_ms: int
    created_at: str


class RunListResponse(BaseModel):
    runs: list[RunRecord]
