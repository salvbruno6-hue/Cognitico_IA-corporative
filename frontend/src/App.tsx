import { useEffect, useState } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { ELOAuthCallback } from './auth/ELOAuthCallback';
import { ELOGoogleLogin } from './auth/ELOGoogleLogin';
import { playELOSound, setELOSoundEnabled, setELOSoundVolume } from './eloSound';

type Area = 'memoria' | 'processamento' | 'decisao' | 'historico' | 'configuracoes' | 'ajuda' | null;

type AreaInfo = { title: string; label: string; text: string; metrics: string[] };

const areas: Record<Exclude<Area, null>, AreaInfo> = {
  memoria: { title: 'Memória', label: 'Conhecimento', text: 'Base de conhecimento corporativo do ELO: informações, referências, registros e aprendizados consolidados.', metrics: ['Datasets Ativos · 25', 'Políticas Ativas · 10', 'Metas Ativas · 23', 'Recuperação Rápida · 12 ms'] },
  processamento: { title: 'Processamento', label: 'Arbitragem', text: 'Camada de processamento: agentes analisam, cruzam dados e executam a arbitragem das informações.', metrics: ['Agentes em Uso · 8', 'Status Operacional · Ativo', 'Ambiente · Cloud', 'Última Execução · 2 min'] },
  decisao: { title: 'Decisão', label: 'Governança', text: 'Camada de governança: decisões são validadas, auditadas e registradas para garantir rastreabilidade.', metrics: ['Políticas Ativas · 12', 'Audit-Ready · 100%', 'Auditorias Ativas · 12', 'Status · Conforme'] },
  historico: { title: 'Histórico', label: 'Rastreabilidade', text: 'Linha do tempo das atividades e decisões registradas pelo ELO.', metrics: ['Eventos · 24', 'Últimas 24h · 24', 'Registros Íntegros · 100%'] },
  configuracoes: { title: 'Configurações', label: 'Parâmetros', text: 'Preferências de interface, notificações e parâmetros operacionais do ambiente.', metrics: ['Som · Configurável', 'Notificações · Configuráveis', 'Ambiente · Produção'] },
  ajuda: { title: 'Ajuda', label: 'Suporte', text: 'Orientações sobre navegação, memória, processamento, decisão e governança do ELO.', metrics: ['Status · Operacional', 'Documentação · Disponível'] },
};

function action(kind: 'click' | 'success' | 'close' = 'click') { playELOSound(kind); }

function ELOCore() {
  const [activeArea, setActiveArea] = useState<Area>(null);
  const [notifications, setNotifications] = useState(true);
  const [alerts, setAlerts] = useState(true);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [volume, setVolume] = useState(70);

  const open = (area: Exclude<Area, null>) => { action(); setActiveArea(area); };
  const close = () => { action('close'); setActiveArea(null); };

  useEffect(() => {
    setELOSoundEnabled(soundEnabled);
    setELOSoundVolume(volume / 100);
  }, [soundEnabled, volume]);

  useEffect(() => {
    if (!activeArea) return;
    const onKeyDown = (event: KeyboardEvent) => { if (event.key === 'Escape') close(); };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [activeArea]);

  return (
    <main className="elo-dashboard" data-elo-core="authenticated">
      <aside className="elo-sidebar" aria-label="Navegação principal">
        <button className="elo-sidebar-brand" type="button" onClick={() => { action(); setActiveArea(null); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>
          <span className="elo-mark">∞</span><strong>ELO</strong><small>Cognitive_IA-corporative</small>
        </button>
        <nav>
          <button className="is-active" type="button" onClick={() => { action(); setActiveArea(null); }} aria-current="page">⌂ <span>Núcleo ELO</span></button>
          <button type="button" onClick={() => open('memoria')}>◉ <span>Memória</span></button>
          <button type="button" onClick={() => open('processamento')}>◌ <span>Processamento</span></button>
          <button type="button" onClick={() => open('decisao')}>♎ <span>Decisão</span></button>
          <hr />
          <button type="button" onClick={() => open('historico')}>◷ <span>Histórico</span></button>
          <button type="button" onClick={() => open('configuracoes')}>⚙ <span>Configurações</span></button>
          <button type="button" onClick={() => open('ajuda')}>? <span>Ajuda</span></button>
        </nav>
        <button className="elo-sidebar-sound" type="button" onClick={() => { const next = !soundEnabled; setSoundEnabled(next); setELOSoundEnabled(next); if (next) playELOSound('success'); }} aria-pressed={soundEnabled} aria-label="Alternar som">
          {soundEnabled ? '◖' : '○'} <span>Som {soundEnabled ? 'ativado' : 'desativado'}</span>
        </button>
      </aside>

      <section className="elo-main">
        <div className="elo-dashboard-top">
          <span className="elo-connected"><i /> CONECTADO AO ELO</span>
          <div className="elo-dashboard-actions">
            <button type="button" onClick={() => open('configuracoes')} aria-label="Abrir configurações">⚙</button>
            <button type="button" onClick={() => { action(); setNotifications(v => !v); }} aria-pressed={notifications} aria-label="Alternar notificações">{notifications ? '♢' : '○'}</button>
          </div>
        </div>

        <section className="elo-hero">
          <div className="elo-hero-logo"><span className="elo-mark elo-mark--hero">∞</span><span><b>ELO</b><small>Cognitive_IA-corporative | Orchestration System</small></span></div>
          <div className="elo-hero-copy"><span>● CONECTADO AO ELO</span><h1>NÚCLEO ELO</h1><p>Sessão autenticada. A camada de inteligência corporativa e orquestração está disponível.</p></div>
        </section>

        <div className="elo-card-grid">
          {(['memoria', 'processamento', 'decisao'] as const).map((key) => {
            const area = areas[key];
            return <article className={`elo-module elo-module--${key}`} key={key}>
              <span className="elo-module-kicker">{area.title.toUpperCase()}</span><span className="elo-module-icon">{key === 'memoria' ? '◉' : key === 'processamento' ? '◌' : '♎'}</span>
              <h2>{area.label}</h2><p>{area.text}</p>
              <div className="elo-metrics">{area.metrics.map(metric => <span key={metric}>{metric}</span>)}</div>
              <button type="button" onClick={() => open(key)}>Acessar {area.title} <b>→</b></button>
            </article>;
          })}
        </div>

        <section className="elo-system-strip" aria-label="Status do sistema">
          <div><b>⌁ ATIVIDADE RECENTE</b><span>24 eventos nas últimas 24h</span></div>
          <div><b>✓ STATUS DO SISTEMA</b><span>Todos os sistemas operacionais</span></div>
          <div><b>↻ ÚLTIMA SINCRONIZAÇÃO</b><span>31/08/2026 23:24</span></div>
        </section>

        <section className="elo-controls" aria-label="Som e notificações">
          <div><b>Som e Notificações</b><span>Controles de interação do ELO</span></div>
          <label><span>Notificações do sistema</span><input type="checkbox" checked={notifications} onChange={(e) => { action(); setNotifications(e.target.checked); }} /></label>
          <label><span>Alertas de eventos</span><input type="checkbox" checked={alerts} onChange={(e) => { action(); setAlerts(e.target.checked); }} /></label>
          <label><span>Volume</span><input type="range" min="0" max="100" value={volume} onChange={(e) => { setVolume(Number(e.target.value)); }} aria-label="Volume do som" /></label>
        </section>

        {activeArea && <div className="elo-modal-backdrop" role="presentation" onClick={close}>
          <section className="elo-modal" role="dialog" aria-modal="true" aria-labelledby="elo-modal-title" onClick={(e) => e.stopPropagation()}>
            <span className="elo-eyebrow">{areas[activeArea].label.toUpperCase()}</span><h2 id="elo-modal-title">{areas[activeArea].title}</h2><p>{areas[activeArea].text}</p>
            <div className="elo-modal-metrics">{areas[activeArea].metrics.map(metric => <span key={metric}>{metric}</span>)}</div>
            <button type="button" onClick={close}>Fechar</button>
          </section>
        </div>}
      </section>
    </main>
  );
}

function Login() { return <ELOGoogleLogin><ELOCore /></ELOGoogleLogin>; }

export default function App() {
  return <Routes><Route path="/" element={<Login />} /><Route path="/login" element={<Login />} /><Route path="/auth/callback" element={<ELOAuthCallback />} /><Route path="/app/*" element={<Login />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>;
}
