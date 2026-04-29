import { useEffect, useState } from 'react';
import { getHealth, getRuns, getTasks, runTask } from './api/client';
import { Dashboard } from './components/Dashboard';
import { HistoryPanel } from './components/HistoryPanel';
import { ResultPanel } from './components/ResultPanel';
import { SettingsPanel } from './components/SettingsPanel';
import { TaskRunner } from './components/TaskRunner';
import type { ConfigStatus, RunRecord, TaskMeta } from './types';

export default function App() {
  const [tasks, setTasks] = useState<TaskMeta[]>([]);
  const [runs, setRuns] = useState<RunRecord[]>([]);
  const [config, setConfig] = useState<ConfigStatus | null>(null);
  const [selectedTaskId, setSelectedTaskId] = useState('classification');
  const [selectedRun, setSelectedRun] = useState<RunRecord | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getHealth(), getTasks(), getRuns()])
      .then(([health, taskResponse, runResponse]) => {
        setConfig(health.config);
        setTasks(taskResponse.tasks);
        setRuns(runResponse.runs);
      })
      .catch((error: Error) => setLoadError(error.message));
  }, []);

  const selectedTask = tasks.find((task) => task.id === selectedTaskId) || tasks[0];

  async function handleRun(payload: Record<string, unknown>) {
    const run = await runTask(selectedTaskId, payload);
    setSelectedRun(run);
    setRuns((current) => [run, ...current.filter((item) => item.id !== run.id)]);
    return run;
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <span className="eyebrow">Film Reviewer</span>
          <strong>Reviewer Studio</strong>
        </div>
        <span className={`connection ${config?.deepseek_configured ? 'online' : 'offline'}`}>{config?.deepseek_configured ? 'DeepSeek Online' : 'Config Missing'}</span>
      </header>

      <Dashboard config={config} tasks={tasks} runs={runs} />
      {loadError ? <div className="error-box">API unavailable: {loadError}</div> : null}

      <div className="workbench">
        <nav className="task-nav">
          {tasks.map((task) => (
            <button className={task.id === selectedTaskId ? 'active' : ''} key={task.id} onClick={() => setSelectedTaskId(task.id)}>
              <span>{task.label.split(' · ')[0]}</span>
              <strong>{task.label.split(' · ')[1]}</strong>
            </button>
          ))}
        </nav>
        {selectedTask ? <TaskRunner task={selectedTask} onRun={handleRun} /> : <section className="task-runner empty-state">Loading tasks...</section>}
        <HistoryPanel runs={runs} selectedTaskId={selectedTaskId} onSelectRun={setSelectedRun} />
      </div>

      <ResultPanel run={selectedRun} />
      <SettingsPanel config={config} />
    </main>
  );
}
