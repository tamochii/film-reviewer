from __future__ import annotations

from backend.app.services.tasks import classification, cot_compare, grid_search, json_extract, prompt_evaluator, roleplay


TASKS = {
    "classification": classification.run,
    "json_extract": json_extract.run,
    "cot_compare": cot_compare.run,
    "roleplay": roleplay.run,
    "prompt_evaluator": prompt_evaluator.run,
    "grid_search": grid_search.run,
}


def run_task(task_id: str, payload: dict) -> dict:
    if task_id not in TASKS:
        raise KeyError(f"Unknown task: {task_id}")
    return TASKS[task_id](payload)
