from __future__ import annotations

from backend.app.services.run_history import RunHistoryStore


def test_run_history_saves_lists_and_gets_runs(tmp_path) -> None:
    store = RunHistoryStore(tmp_path / "runs.sqlite3")

    first = store.save_run(
        task_id="classification",
        status="success",
        input_data={"review": "a"},
        output_data={"label": "积极"},
        error=None,
        model="deepseek-chat",
        duration_ms=12,
    )
    second = store.save_run(
        task_id="json_extract",
        status="error",
        input_data={"review": "b"},
        output_data={},
        error="bad upstream",
        model="deepseek-chat",
        duration_ms=5,
    )

    runs = store.list_runs()

    assert [run["id"] for run in runs] == [second["id"], first["id"]]
    assert store.get_run(first["id"])["output"] == {"label": "积极"}
    assert store.get_run("missing") is None
