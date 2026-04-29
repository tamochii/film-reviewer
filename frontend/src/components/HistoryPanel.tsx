import type { RunRecord } from '../types';

type Props = {
  runs: RunRecord[];
  selectedTaskId: string;
  onSelectRun: (run: RunRecord) => void;
};

export function HistoryPanel({ runs, selectedTaskId, onSelectRun }: Props) {
  const filtered = runs.filter((run) => run.task_id === selectedTaskId).slice(0, 8);
  return (
    <aside className="history-panel">
      <div className="panel-heading">
        <span className="eyebrow">History</span>
        <h2>最近运行</h2>
      </div>
      {filtered.length === 0 ? <p className="empty-state">还没有这个任务的运行记录。</p> : null}
      <div className="run-list">
        {filtered.map((run) => (
          <button className="run-card" key={run.id} onClick={() => onSelectRun(run)}>
            <span className={`status-pill ${run.status}`}>{run.status}</span>
            <strong>{run.duration_ms}ms</strong>
            <small>{new Date(run.created_at).toLocaleString()}</small>
          </button>
        ))}
      </div>
    </aside>
  );
}
