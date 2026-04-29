export type TaskMeta = {
  id: string;
  label: string;
  description: string;
  result_type: string;
};

export type RunRecord = {
  id: string;
  task_id: string;
  status: 'success' | 'error';
  input: Record<string, unknown>;
  output: Record<string, unknown>;
  error: string | null;
  model: string;
  duration_ms: number;
  created_at: string;
};

export type ConfigStatus = {
  deepseek_configured: boolean;
  tmdb_configured: boolean;
  deepseek_base_url: string;
  deepseek_model: string;
  tmdb_base_url: string;
};
