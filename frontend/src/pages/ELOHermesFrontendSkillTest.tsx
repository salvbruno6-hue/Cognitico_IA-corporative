import { useState } from 'react';

const blocks = [
  ['Mission Surface', 'Intent → governed mission → status → outcome'],
  ['Workspace', 'Reusable sector-ready composition without duplicating the shell'],
  ['Evidence', 'Provenance and result visibility without inventing enterprise facts'],
  ['Governance', 'ELO remains authority; Hermes remains execution boundary'],
  ['States', 'Loading, empty, validation, success and error are explicit'],
  ['Responsive Shell', 'Keyboard-safe controls and mobile-safe composition'],
] as const;

export function ELOHermesFrontendSkillTest() {
  const [status, setStatus] = useState<'idle' | 'validating' | 'ready'>('idle');

  const runMission = () => {
    setStatus('validating');
    window.setTimeout(() => setStatus('ready'), 450);
  };

  return (
    <main className="hermes-skill-lab" aria-labelledby="hermes-skill-title">
      <header className="hermes-skill-header">
        <a href="/Cognitico_IA-corporative/" className="hermes-skill-brand" aria-label="Voltar ao ELO">
          <span className="elo-mark" aria-hidden="true">∞</span>
          <span><strong>ELO</strong><small>Inteligência Corporativa</small></span>
        </a>
        <span className="hermes-skill-badge">HERMES SKILL LAB · REAL</span>
      </header>

      <section className="hermes-skill-hero">
        <div>
          <p className="hermes-kicker">elo-frontend-engineering</p>
          <h1 id="hermes-skill-title">Frontend como sistema, não como página.</h1>
          <p className="hermes-lede">
            Validação da skill Hermes aplicada ao frontend publicado do ELO: composição, tokens,
            blocos, estados, acessibilidade e fronteira de execução governada.
          </p>
          <button type="button" className="hermes-primary-action" onClick={runMission} disabled={status === 'validating'}>
            {status === 'validating' ? 'Validando missão…' : 'Executar missão de teste'}
          </button>
        </div>
        <aside className="hermes-mission-card" aria-live="polite">
          <span>MISSION SURFACE</span>
          <strong>{status === 'idle' ? 'Pronta para validação' : status === 'validating' ? 'Contrato em validação' : 'Validação concluída'}</strong>
          <p>Teste local determinístico. Nenhuma credencial ou dado empresarial é enviado pelo browser.</p>
          <dl>
            <div><dt>Autoridade</dt><dd>ELO</dd></div>
            <div><dt>Execução</dt><dd>Hermes</dd></div>
            <div><dt>Evidência</dt><dd>{status === 'ready' ? 'Disponível' : 'Aguardando'}</dd></div>
          </dl>
        </aside>
      </section>

      <section className="hermes-skill-section" aria-labelledby="blocks-title">
        <div className="hermes-section-heading"><p className="hermes-kicker">COMPOSABLE BLOCKS</p><h2 id="blocks-title">Capacidades exercitadas</h2></div>
        <div className="hermes-block-grid">
          {blocks.map(([title, description]) => <article key={title} className="hermes-block"><span aria-hidden="true">◇</span><h3>{title}</h3><p>{description}</p></article>)}
        </div>
      </section>

      <section className="hermes-skill-section hermes-two-column">
        <div>
          <p className="hermes-kicker">SEMANTIC DESIGN TOKENS</p>
          <h2>Paleta e hierarquia</h2>
          <div className="hermes-token-list" aria-label="Tokens de interface">
            <div><i className="token token-surface" /><span>surface</span><code>--surface</code></div>
            <div><i className="token token-signal" /><span>signal</span><code>--signal</code></div>
            <div><i className="token token-success" /><span>success</span><code>--success</code></div>
            <div><i className="token token-attention" /><span>attention</span><code>--attention</code></div>
          </div>
        </div>
        <div>
          <p className="hermes-kicker">GOVERNED BACKEND BOUNDARY</p>
          <h2>Browser → ELO → Hermes</h2>
          <ol className="hermes-boundary">
            <li><b>Browser</b><span>apresenta, navega e inicia a interação</span></li>
            <li><b>ELO</b><span>valida autorização, contrato, contexto e governança</span></li>
            <li><b>Hermes</b><span>executa a capacidade aprovada e devolve resultado/evidência</span></li>
          </ol>
        </div>
      </section>

      <section className="hermes-skill-section hermes-verification" aria-labelledby="verification-title">
        <div><p className="hermes-kicker">VERIFICATION</p><h2 id="verification-title">Critérios de aprovação</h2></div>
        <ul>
          <li>UI responsiva e semanticamente estruturada</li>
          <li>foco de teclado e nomes acessíveis</li>
          <li>tokens semânticos, sem cores de setor espalhadas</li>
          <li>estados explícitos de interação</li>
          <li>nenhum segredo ou autoridade Hermes no bundle</li>
          <li>linhagem registrada para a skill externa aplicada</li>
        </ul>
      </section>

      <footer className="hermes-skill-footer">
        Laboratório isolado · não representa dados corporativos reais · não altera a autoridade canônica do ELO.
      </footer>
    </main>
  );
}
