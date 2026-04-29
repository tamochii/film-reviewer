import { useEffect, useState } from 'react';
import type { ChatMessage, RunRecord, TaskMeta } from '../types';

type Props = {
  task: TaskMeta;
  currentRun: RunRecord | null;
  roleplayHistory: ChatMessage[];
  onRoleplayHistoryChange: (history: ChatMessage[]) => void;
  onRun: (payload: Record<string, unknown>) => Promise<RunRecord>;
  onSelectRun: (run: RunRecord) => void;
};

const sampleReviews = [
  '前面铺垫又长又闷，但最后那场和解还是让我买账了。',
  '镜头确实漂亮，可我看完全程只剩疲惫。',
  '它的问题不少，可结尾回收足够让我原谅大半。',
];

const defaults = {
  jsonReview: '这部电影节奏紧凑，人物关系复杂但情感落点清晰，几处反转可能涉及剧透。',
  movieTitle: 'Chainsaw Man - The Movie: Reze Arc',
  plot: '主角在危险世界中追求普通生活，却被关系、欲望和恶魔冲突不断推向选择。故事通过亲密关系的诱惑和暴力行动的后果，形成多次转折。',
  chat: '评价一下这部电影的节奏和角色塑造。',
  prompt: '请判断下面这条影评的情感是积极还是消极，只输出 JSON。',
  overview: '一个少年与恶魔缔结契约后卷入危险战斗，并在残酷现实里寻找亲密关系和生活目标。',
};

export function TaskRunner({ task, currentRun, roleplayHistory, onRoleplayHistoryChange, onRun, onSelectRun }: Props) {
  const [jsonReview, setJsonReview] = useState(defaults.jsonReview);
  const [movieTitle, setMovieTitle] = useState(defaults.movieTitle);
  const [plot, setPlot] = useState(defaults.plot);
  const [chatText, setChatText] = useState(defaults.chat);
  const [prompt, setPrompt] = useState(defaults.prompt);
  const [overview, setOverview] = useState(defaults.overview);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (currentRun?.task_id === 'roleplay') {
      const history = currentRun.output.history as ChatMessage[] | undefined;
      if (history) onRoleplayHistoryChange(history);
    }
  }, [currentRun, onRoleplayHistoryChange]);

  async function submit(payload: Record<string, unknown>) {
    setLoading(true);
    setError(null);
    try {
      const run = await onRun(payload);
      if (run.task_id === 'roleplay') {
        onRoleplayHistoryChange((run.output.history as ChatMessage[] | undefined) || roleplayHistory);
        setChatText('');
      }
      onSelectRun(run);
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

      {task.id === 'classification' ? (
        <div className="task-visual classification-setup">
          <div className="dataset-strip">
            {sampleReviews.map((review, index) => <article key={review}><span>Sample {index + 1}</span><p>{review}</p></article>)}
          </div>
          <button className="primary-button wide" disabled={loading} onClick={() => submit({})}>{loading ? 'Running...' : 'Run Zero-shot vs Few-shot'}</button>
        </div>
      ) : null}

      {task.id === 'json_extract' ? (
        <div className="task-visual">
          <label className="input-label">电影名称</label>
          <input className="text-input" value={movieTitle} onChange={(event) => setMovieTitle(event.target.value)} />
          <label className="input-label">影评文本</label>
          <textarea value={jsonReview} onChange={(event) => setJsonReview(event.target.value)} rows={8} />
          <button className="primary-button wide" disabled={loading} onClick={() => submit({ review: jsonReview, movie_title: movieTitle })}>{loading ? 'Extracting...' : 'Extract Structured JSON'}</button>
        </div>
      ) : null}

      {task.id === 'cot_compare' ? (
        <div className="task-visual">
          <div className="comparison-hint"><span>Plain analysis</span><span>Step-by-step CoT</span></div>
          <label className="input-label">剧情简介</label>
          <textarea value={plot} onChange={(event) => setPlot(event.target.value)} rows={9} />
          <button className="primary-button wide" disabled={loading} onClick={() => submit({ plot_summary: plot })}>{loading ? 'Comparing...' : 'Compare Reasoning Styles'}</button>
        </div>
      ) : null}

      {task.id === 'roleplay' ? (
        <div className="chat-console">
          <div className="chat-thread">
            {roleplayHistory.length === 0 ? <div className="critic-intro">刻薄但专业的电影评论家已就位。抛一个观点给他。</div> : null}
            {roleplayHistory.map((message, index) => <div className={`chat-bubble ${message.role}`} key={`${message.role}-${index}`}>{message.content}</div>)}
          </div>
          <div className="chat-composer">
            <textarea value={chatText} onChange={(event) => setChatText(event.target.value)} rows={3} placeholder="问问这位影评人..." />
            <button className="primary-button" disabled={loading || !chatText.trim()} onClick={() => submit({ message: chatText, history: roleplayHistory })}>{loading ? 'Sending...' : 'Send'}</button>
          </div>
        </div>
      ) : null}

      {task.id === 'prompt_evaluator' ? (
        <div className="task-visual">
          <div className="rubric-grid"><span>Clarity</span><span>Completeness</span><span>Format</span></div>
          <label className="input-label">目标提示词</label>
          <textarea value={prompt} onChange={(event) => setPrompt(event.target.value)} rows={8} />
          <button className="primary-button wide" disabled={loading} onClick={() => submit({ target_prompt: prompt })}>{loading ? 'Evaluating...' : 'Evaluate Prompt'}</button>
        </div>
      ) : null}

      {task.id === 'grid_search' ? (
        <div className="task-visual">
          <div className="variant-preview"><span>50 字摘要</span><span>2 句核心剧情</span><span>主角/目标/冲突/基调</span></div>
          <label className="input-label">电影简介</label>
          <textarea value={overview} onChange={(event) => setOverview(event.target.value)} rows={8} />
          <button className="primary-button wide" disabled={loading} onClick={() => submit({ overview })}>{loading ? 'Searching...' : 'Run Prompt Grid Search'}</button>
        </div>
      ) : null}

      {error ? <div className="error-box">{error}</div> : null}
    </section>
  );
}
