import type { ReactNode } from 'react';
import type { ChatMessage, RunRecord } from '../types';

type ClassificationItem = { id: number; text: string; gold: string; predicted: string; correct: boolean };
type ClassificationVariant = { accuracy: number; items: ClassificationItem[] };
type GridVariant = { name: string; summary: string; score: number; length: number; density: number };

function percent(value = 0) {
  return `${Math.round(value * 100)}%`;
}

function renderAccuracyBar(label: string, variant?: ClassificationVariant) {
  const accuracy = variant?.accuracy || 0;
  return <div className="accuracy-card"><div><span>{label}</span><strong>{percent(accuracy)}</strong></div><div className="bar-track"><i style={{ width: percent(accuracy) }} /></div></div>;
}

function renderClassification(output: Record<string, unknown>) {
  const zero = output.zero_shot as ClassificationVariant | undefined;
  const few = output.few_shot as ClassificationVariant | undefined;
  const items = few?.items || zero?.items || [];
  return <div className="visual-result">{renderAccuracyBar('Zero-shot', zero)}{renderAccuracyBar('Few-shot', few)}<div className="prediction-table">{items.map((item) => <div className="prediction-row" key={item.id}><span>{item.id}</span><p>{item.text}</p><b>{item.gold}</b><strong className={item.correct ? 'ok' : 'bad'}>{item.predicted}</strong></div>)}</div></div>;
}

function renderJsonExtract(output: Record<string, unknown>) {
  const extraction = output.extraction as Record<string, unknown> | undefined;
  if (!extraction) return null;
  if (extraction.parse_error) return <div className="error-box">JSON parse failed: {String(extraction.parse_error)}</div>;
  const keywords = Array.isArray(extraction.keywords) ? extraction.keywords : [];
  return <div className="json-visual"><div className="field-card"><span>Movie</span><strong>{String(extraction.movie_name || '-')}</strong></div><div className="field-card"><span>Sentiment</span><strong>{String(extraction.sentiment_score || '-')}</strong></div><div className="field-card"><span>Spoiler</span><strong>{String(extraction.has_spoiler ?? '-')}</strong></div><div className="keyword-cloud">{keywords.map((keyword) => <span key={String(keyword)}>{String(keyword)}</span>)}</div></div>;
}

function renderCot(output: Record<string, unknown>) {
  return <div className="cot-grid"><article><span>Without CoT</span><p>{String(output.plain || '')}</p></article><article><span>With CoT</span><p>{String(output.cot || '')}</p></article></div>;
}

function renderRoleplay(output: Record<string, unknown>) {
  const history = (output.history || []) as ChatMessage[];
  return <div className="chat-thread result-chat">{history.map((message, index) => <div className={`chat-bubble ${message.role}`} key={`${message.role}-${index}`}>{message.content}</div>)}</div>;
}

function renderPromptEvaluator(output: Record<string, unknown>) {
  const evaluation = output.evaluation as Record<string, unknown> | undefined;
  if (!evaluation) return null;
  if (evaluation.parse_error) return <div className="error-box">Evaluator JSON parse failed: {String(evaluation.parse_error)}</div>;
  return <div className="score-meter-grid">{['clarity', 'completeness', 'format'].map((key) => { const raw = evaluation[key]; const score = typeof raw === 'number' ? raw : Number(raw) || 0; return <div className="meter-card" key={key}><span>{key}</span><strong>{score}/10</strong><div className="bar-track"><i style={{ width: `${score * 10}%` }} /></div><small>{String(evaluation[`${key}_reason`] || evaluation[`${key}Reason`] || '')}</small></div>; })}</div>;
}

function renderGridSearch(output: Record<string, unknown>) {
  const variants = ((output.variants || []) as GridVariant[]).slice().sort((a, b) => b.score - a.score);
  const best = String(output.best_variant || '');
  const maxScore = Math.max(...variants.map((variant) => variant.score), 1);
  return <div className="ranked-variants">{variants.map((variant, index) => <article className={variant.name === best ? 'best' : ''} key={variant.name}><div><span>#{index + 1} {variant.name}</span>{variant.name === best ? <b>Best</b> : null}</div><p>{variant.summary}</p><div className="bar-track"><i style={{ width: `${Math.max(8, (variant.score / maxScore) * 100)}%` }} /></div><small>score {variant.score.toFixed(3)} · density {variant.density.toFixed(3)} · {variant.length} chars</small></article>)}</div>;
}

export function ResultPanel({ run }: { run: RunRecord | null }) {
  if (!run) return <section className="result-panel empty-state">运行一个任务后，适配该任务的可视化结果会显示在这里。</section>;
  const renderers: Record<string, (output: Record<string, unknown>) => ReactNode> = { classification: renderClassification, json_extract: renderJsonExtract, cot_compare: renderCot, roleplay: renderRoleplay, prompt_evaluator: renderPromptEvaluator, grid_search: renderGridSearch };
  return <section className="result-panel"><div className="panel-heading horizontal"><div><span className="eyebrow">Visual Result</span><h2>{run.task_id}</h2></div><span className={`status-pill ${run.status}`}>{run.status}</span></div>{run.status === 'error' ? <div className="error-box">{run.error}</div> : renderers[run.task_id]?.(run.output)}<details className="raw-json"><summary>Raw JSON</summary><pre className="json-block">{JSON.stringify(run.output, null, 2)}</pre></details></section>;
}
