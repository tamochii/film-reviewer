import { useState } from 'react';
import type { RunRecord, TaskMeta } from '../types';

type Props = {
  task: TaskMeta;
  onRun: (payload: Record<string, unknown>) => Promise<RunRecord>;
};

const defaults: Record<string, string> = {
  classification: '使用 data/reviews.json 中的固定样本运行 zero-shot 与 few-shot 对比。',
  json_extract: '这部电影节奏紧凑，人物关系复杂但情感落点清晰，几处反转可能涉及剧透。',
  cot_compare: '主角在危险世界中追求普通生活，却被关系、欲望和恶魔冲突不断推向选择。',
  roleplay: '评价一下这部电影的节奏和角色塑造。',
  prompt_evaluator: '请判断下面这条影评的情感是积极还是消极，只输出 JSON。',
  grid_search: '一个少年与恶魔缔结契约后卷入危险战斗，并在残酷现实里寻找亲密关系和生活目标。',
};

export function TaskRunner({ task, onRun }: Props) {
  const [text, setText] = useState(defaults[task.id] || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setLoading(true);
    setError(null);
    try {
      await onRun(buildPayload(task.id, text));
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="task-runner">
      <div className="panel-heading">
        <span className="eyebrow">Experiment Workspace</span>
        <h2>{task.label}</h2>
        <p>{task.description}</p>
      </div>
      <label className="input-label" htmlFor="task-input">实验输入</label>
      <textarea id="task-input" value={text} onChange={(event) => setText(event.target.value)} rows={9} />
      <div className="runner-actions">
        <button className="primary-button" disabled={loading} onClick={submit}>{loading ? 'Running...' : 'Run Experiment'}</button>
        <span>{task.result_type}</span>
      </div>
      {error ? <div className="error-box">{error}</div> : null}
    </section>
  );
}

function buildPayload(taskId: string, text: string): Record<string, unknown> {
  if (taskId === 'classification') return {};
  if (taskId === 'json_extract') return { review: text, movie_title: 'Chainsaw Man - The Movie: Reze Arc' };
  if (taskId === 'cot_compare') return { plot_summary: text };
  if (taskId === 'roleplay') return { message: text, history: [] };
  if (taskId === 'prompt_evaluator') return { target_prompt: text };
  if (taskId === 'grid_search') return { overview: text };
  return { text };
}
