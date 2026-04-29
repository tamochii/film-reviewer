import type { ConfigStatus, RunRecord, TaskMeta } from '../types';

type Props = {
  config: ConfigStatus | null;
  tasks: TaskMeta[];
  runs: RunRecord[];
};

export function Dashboard({ config, tasks, runs }: Props) {
  const successful = runs.filter((run) => run.status === 'success').length;
  return (
    <section className="dashboard-grid">
      <div className="hero-card">
        <span className="eyebrow">Reviewer Studio</span>
        <h1>智能影评实验工作台</h1>
        <p>在浏览器里运行六个 Prompt Engineering 实验，查看结构化输出，并保留每次实验历史。</p>
      </div>
      <div className="metric-card">
        <span>Tasks</span>
        <strong>{tasks.length}</strong>
        <p>全部任务可运行</p>
      </div>
      <div className="metric-card">
        <span>Runs</span>
        <strong>{runs.length}</strong>
        <p>{successful} successful</p>
      </div>
      <div className="metric-card">
        <span>Model</span>
        <strong>{config?.deepseek_model || 'unknown'}</strong>
        <p>{config?.deepseek_configured ? 'DeepSeek configured' : 'Missing DeepSeek key'}</p>
      </div>
    </section>
  );
}
