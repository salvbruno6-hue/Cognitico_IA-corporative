import React, { useEffect, useMemo, useState } from 'react';

type SuggestedAction = {
  action_id?: string;
  label: string;
  action_type?: string;
  payload?: Record<string, unknown>;
  requires_approval?: boolean;
};

type SourceReference = {
  source_id: string;
  source_type: string;
  title?: string | null;
  uri?: string | null;
  metadata?: Record<string, unknown>;
};

type CognitiveResponse = {
  response_id: string;
  request_id: string;
  session_id: string;
  domain?: string | null;
  response: Record<string, unknown>;
  sources: SourceReference[];
  agents_used: Array<{ agent_id: string; role?: string | null; provider?: string | null; model?: string | null }>;
  confidence: number;
  provenance: Record<string, unknown>;
  suggestions: SuggestedAction[];
  processing_time_ms: number;
  timestamp: string;
};

type ChatMessage = {
  role: 'user' | 'assistant' | 'system';
  content: string;
  metadata?: Record<string, unknown>;
};

type SessionState = {
  session_id?: string;
  tenant_id?: string;
  domain?: string;
  user_id?: string;
};

const API_BASE = '/api/v1/interface';

const defaultSession: SessionState = {
  tenant_id: 'default',
  domain: 'inteligencia_demanda',
  user_id: 'anonymous',
};

function formatResponse(response: CognitiveResponse): string {
  const payload = response.response;
  const text =
    typeof payload.content === 'string'
      ? payload.content
      : typeof payload.summary === 'string'
        ? payload.summary
        : JSON.stringify(payload, null, 2);

  const suggestions = response.suggestions
    .map((item) => `• ${item.label}${item.requires_approval ? ' (aprovação)' : ''}`)
    .join('\n');

  const sources = response.sources
    .map((item) => `• ${item.title ?? item.source_id} [${item.source_type}]`)
    .join('\n');

  const confidence = Math.round(response.confidence * 100);

  return [
    text,
    '',
    `Confiança: ${confidence}%`,
    response.domain ? `Domínio: ${response.domain}` : null,
    sources ? `\nFontes:\n${sources}` : null,
    suggestions ? `\nSugestões:\n${suggestions}` : null,
  ]
    .filter(Boolean)
    .join('\n');
}

export const ELOChat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'system',
      content: 'Interface cognitiva do ELO pronta para receber demandas por domínio.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [session, setSession] = useState<SessionState>(defaultSession);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const stored = window.localStorage.getItem('elo-interface-session');
    if (!stored) return;
    try {
      const parsed = JSON.parse(stored) as SessionState;
      setSession((current) => ({ ...current, ...parsed }));
    } catch {
      window.localStorage.removeItem('elo-interface-session');
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem('elo-interface-session', JSON.stringify(session));
  }, [session]);

  const title = useMemo(() => {
    const domain = session.domain ?? 'inteligencia_demanda';
    return `ELO • ${domain}`;
  }, [session.domain]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const nextMessages: ChatMessage[] = [
      ...messages,
      { role: 'user', content: trimmed },
    ];
    setMessages(nextMessages);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const payload = {
        message: trimmed,
        session_id: session.session_id,
        user_id: session.user_id,
        tenant_id: session.tenant_id,
        domain: session.domain,
        context: {
          channel: 'web',
          source: 'frontend',
        },
      };

      const response = await fetch(`${API_BASE}/cognitive`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = (await response.json()) as CognitiveResponse;
      setSession((current) => ({
        ...current,
        session_id: data.session_id,
        domain: data.domain ?? current.domain,
      }));

      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: formatResponse(data),
          metadata: {
            confidence: data.confidence,
            response_id: data.response_id,
            request_id: data.request_id,
          },
        },
      ]);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Falha ao consultar o ELO';
      setError(message);
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: `Erro: ${message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'grid', gap: 16, maxWidth: 960, margin: '0 auto', padding: 24 }}>
      <header>
        <h2>{title}</h2>
        <p>
          Sessão: {session.session_id ?? 'nova'} • Tenant: {session.tenant_id ?? 'default'}
        </p>
      </header>

      <section style={{ display: 'grid', gap: 12, minHeight: 420, border: '1px solid #ddd', padding: 16, borderRadius: 12 }}>
        {messages.map((message, index) => (
          <article
            key={`${message.role}-${index}`}
            style={{
              padding: 12,
              borderRadius: 10,
              background: message.role === 'user' ? '#eef6ff' : message.role === 'assistant' ? '#f7f7f7' : '#fafafa',
              whiteSpace: 'pre-wrap',
            }}
          >
            <strong>{message.role.toUpperCase()}</strong>
            <div>{message.content}</div>
          </article>
        ))}
      </section>

      <section style={{ display: 'grid', gap: 8 }}>
        <label>
          Domínio
          <input
            value={session.domain ?? ''}
            onChange={(event) => setSession((current) => ({ ...current, domain: event.target.value }))}
            placeholder="inteligencia_demanda"
            style={{ width: '100%', padding: 10, marginTop: 4 }}
          />
        </label>

        <label>
          Mensagem
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Digite sua pergunta ou solicitação"
            rows={5}
            style={{ width: '100%', padding: 10, marginTop: 4 }}
          />
        </label>

        <button onClick={handleSend} disabled={loading} style={{ padding: '10px 16px' }}>
          {loading ? 'Processando...' : 'Enviar ao ELO'}
        </button>

        {error ? <p style={{ color: 'crimson' }}>{error}</p> : null}
      </section>
    </div>
  );
};

export default ELOChat;
