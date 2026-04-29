import type { ConfigStatus, RunRecord, TaskMeta } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options?.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(String(payload.detail || response.statusText));
  }
  return response.json() as Promise<T>;
}

export function getHealth(): Promise<{ status: string; config: ConfigStatus }> {
  return request('/api/health');
}

export function getTasks(): Promise<{ tasks: TaskMeta[] }> {
  return request('/api/tasks');
}

export function runTask(taskId: string, payload: Record<string, unknown>): Promise<RunRecord> {
  return request(`/api/tasks/${taskId}/runs`, { method: 'POST', body: JSON.stringify(payload) });
}

export function getRuns(taskId?: string): Promise<{ runs: RunRecord[] }> {
  const query = taskId ? `?task_id=${encodeURIComponent(taskId)}` : '';
  return request(`/api/runs${query}`);
}
