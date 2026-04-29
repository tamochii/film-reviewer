import type { RunRecord } from '../types';

function renderClassification(output: Record<string, unknown>) {
  const zero = output.zero_shot as { accuracy?: number } | undefined;
  const few = output.few_shot as { accuracy?: number } | undefined;
  return (
    <div className="result-grid">
      <div className="score-card"><span>Zero-shot</span><strong>{Math.round((zero?.accuracy || 0) * 100)}%</strong></div>
      <div className="score-card"><span>Few-shot</span><strong>{Math.round((few?.accuracy || 0) * 100)}%</strong></div>
    </div>
  );
}

function renderGridSearch(output: Record<string, unknown>) {
  const variants = (output.variants || []) as Array<{ name: string; summary: string; score: number; length: number }>;
  return (
    <div className="variant-table">
      {variants.map((variant) => (
        <div className="variant-row" key={variant.name}>
          <strong>{variant.name}</strong>
          <span>{variant.summary}</span>
          <small>score {variant.score.toFixed(3)} · {variant.length} chars</small>
        </div>
      ))}
    </div>
  );
}

export function ResultPanel({ run }: { run: RunRecord | null }) {
  if (!run) {
    return <section className="result-panel empty-state">运行一个任务后，结构化结果会显示在这里。</section>;
  }

  return (
    <section className="result-panel">
      <div className="panel-heading horizontal">
        <div>
          <span className="eyebrow">Result</span>
          <h2>{run.task_id}</h2>
        </div>
        <span className={`status-pill ${run.status}`}>{run.status}</span>
      </div>
      {run.status === 'error' ? <div className="error-box">{run.error}</div> : null}
      {run.task_id === 'classification' ? renderClassification(run.output) : null}
      {run.task_id === 'grid_search' ? renderGridSearch(run.output) : null}
      <pre className="json-block">{JSON.stringify(run.output, null, 2)}</pre>
    </section>
  );
}
