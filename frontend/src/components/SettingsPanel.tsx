import type { ConfigStatus } from '../types';

export function SettingsPanel({ config }: { config: ConfigStatus | null }) {
  return (
    <section className="settings-card">
      <div>
        <span className="eyebrow">Settings</span>
        <h2>配置状态</h2>
      </div>
      <dl>
        <dt>DeepSeek</dt>
        <dd>{config?.deepseek_configured ? 'Configured' : 'Missing API key'}</dd>
        <dt>TMDB</dt>
        <dd>{config?.tmdb_configured ? 'Configured' : 'Missing API key'}</dd>
        <dt>Model</dt>
        <dd>{config?.deepseek_model || '-'}</dd>
      </dl>
    </section>
  );
}
