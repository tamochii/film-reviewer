from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.api.routes import tasks
from backend.app.main import create_app


def test_health_and_tasks() -> None:
    client = TestClient(create_app())

    assert client.get("/api/health").json()["status"] == "ok"

    task_payload = client.get("/api/tasks").json()
    assert len(task_payload["tasks"]) == 6
    assert task_payload["tasks"][0]["id"] == "classification"


def test_create_and_read_run(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("FILM_REVIEWER_DB_PATH", str(tmp_path / "runs.sqlite3"))
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-test")
    monkeypatch.setattr(tasks, "run_task", lambda task_id, payload: {"ok": task_id, "payload": payload})
    client = TestClient(create_app())

    created = client.post("/api/tasks/classification/runs", json={"review": "great"}).json()

    assert created["task_id"] == "classification"
    assert created["status"] == "success"
    assert created["output"] == {"ok": "classification", "payload": {"review": "great"}}

    listed = client.get("/api/runs").json()
    assert listed["runs"][0]["id"] == created["id"]
    assert client.get(f"/api/runs/{created['id']}").json()["id"] == created["id"]


def test_create_run_saves_failures(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("FILM_REVIEWER_DB_PATH", str(tmp_path / "runs.sqlite3"))

    def fail_task(task_id, payload):
        raise RuntimeError("upstream failed")

    monkeypatch.setattr(tasks, "run_task", fail_task)
    client = TestClient(create_app())

    response = client.post("/api/tasks/classification/runs", json={"review": "great"})

    assert response.status_code == 500
    assert "upstream failed" in response.json()["detail"]
    assert client.get("/api/runs").json()["runs"][0]["status"] == "error"
