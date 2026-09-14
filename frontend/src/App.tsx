import { useEffect, useState } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { ELOAuthCallback } from './auth/ELOAuthCallback';
import { ELOGoogleLogin } from './auth/ELOGoogleLogin';
import { ELOOAuthConsent } from './auth/ELOOAuthConsent';
import { playELOSound, setELOSoundEnabled, setELOSoundVolume } from './eloSound';

type Area = 'memoria' | 'processamento' | 'decisao' | 'historico' | 'configuracoes' | 'ajuda' | null;
type AreaInfo = { title: string; label: string; text: string; state: string; icon: string };
const areas: Record<Exclude<Area, null>, AreaInfo> = {
  memoria: { title: 'Memória', label: 'Conhecimento', text: 'Conhecimento corporativo, referências e aprendizados consolidados pelo ELO.', state: 'Aguardando evidência', icon: '◉' },
  processamento: { title: 'Processamento', label: 'Arbitragem', text: 'Análise e orquestração de informações por capacidades governadas.', state: 'Pronto para missão', icon: '◌' },
  decisao: { title: 'Decisão', label: 'Governança', text: 'Políticas, autoridade, evidências e rastreabilidade das decisões do ELO.', state: 'Governança ativa', icon: '♎' },
  historico: { title: 'Histórico', label: 'Rastreabilidade', text: 'Linha do tempo de eventos, resultados e evidências disponíveis à sessão.', state: 'Consulta controlada', icon: '◷' },
  configuracoes: { title: 'Configurações', label: 'Parâmetros', text: 'Preferências locais de interação. Autoridade e segredos permanecem fora do navegador.', state: 'Estado local', icon: '⚙' },
  ajuda: { title: 'Ajuda', label: 'Suporte', text: 'Orientações para navegar pelas superfícies de missão, workspace, evidência e governança.', state: 'Disponível', icon: '?' },
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
  useEffect(() => { setELOSoundEnabled(soundEnabled); setELOSoundVolume(volume / 100); }, [soundEnabled, volume]);
  useEffect(() => { if (!activeArea) return; const onKeyDown = (event: KeyboardEvent) => { if (event.key === 'Escape') close(); }; window.addEventListener('keydown', onKeyDown); return () => window.removeEventListener('keydown', onKeyDown); }, [activeArea]);
  return (
    <main className="elo-dashboard" data-elo-core="authenticated">
      <aside className="elo-sidebar" aria-label="Navegação principal">
        <button className="elo-sidebar-brand" type="button" onClick={() => { action(); setActiveArea(null); window.scrollTo({ top: 0, behavior: 'smooth' }); }}><span className="elo-mark">∞</span><strong>ELO</strong><small>Cognitive_IA-corporative</small></button>
        <nav aria-label="Áreas do ELO">
          <button className="is-active" type="button" onClick={() => { action(); setActiveArea(null); }} aria-current="page">⌂ <span>Núcleo</span></button>
          <button type="button" onClick={() => open('memoria')}>◉ <span>Memória</span></button>
          <button type="button" onClick={() => open('processamento')}>◌ <span>Processamento</span></button>
          <button type="button" onClick={() => open('decisao')}>♎ <span>Governança</span></button>
          <hr />
          <button type="button" onClick={() => open('historico')}>◷ <span>Histórico</span></button>
          <button type="button" onClick={() => open('configuracoes')}>⚙ <span>Configurações</span></button>
          <button type="button" onClick={() => open('ajuda')}>? <span>Ajuda</span></button>
        </nav>
        <button className="elo-sidebar-sound" type="button" onClick={() => { const next = !soundEnabled; setSoundEnabled(next); setELOSoundEnabled(next); if (next) playELOSound('success'); }} aria-pressed={soundEnabled} aria-label="Alternar som">{soundEnabled ? '◖' : '○'} <span>Som {soundEnabled ? 'ativado' : 'desativado'}</span></button>
      </aside>
      <section className="elo-main">
        <header className="elo-dashboard-top"><div><span className="elo-connected"><i /> SESSÃO ELO ATIVA</span><p className="elo-top-context">Inteligência corporativa · camada de experiência</p></div><div className="elo-dashboard-actions"><button type="button" onClick={() => open('configuracoes')} aria-label="Abrir configurações">⚙</button><button type="button" onClick={() => { action(); setNotifications(v => !v); }} aria-pressed={notifications} aria-label="Alternar notificações">{notifications ? '♢' : '○'}</button></div></header>

        <section className="elo-hero" aria-labelledby="elo-hero-title">
          <div className="elo-hero-logo"><span className="elo-mark elo-mark--hero">∞</span><span><b>ELO</b><small>Cognitive_IA-corporative · Orchestration System</small></span></div>
          <div className="elo-hero-copy"><span>EXPERIÊNCIA GOVERNADA</span><h1 id="elo-hero-title">NÚCLEO ELO</h1><p>Transforme uma intenção em missão, acompanhe o workspace, consulte evidências e preserve a governança no fluxo.</p><div className="elo-hero-state"><i /> Interface pronta · dados operacionais somente quando fornecidos pela camada ELO</div></div>
        </section>

        <section className="elo-mission-surface" aria-labelledby="mission-title">
          <div className="elo-section-heading"><div><span>MISSÃO</span><h2 id="mission-title">O que você precisa realizar?</h2></div><span className="elo-boundary-badge">Browser → ELO → Hermes</span></div>
          <div className="elo-mission-grid"><div className="elo-mission-input" role="group" aria-label="Entrada de missão"><span>INTENÇÃO DO USUÁRIO</span><p>Descreva uma necessidade para que o ELO possa governar a próxima etapa.</p><button type="button" onClick={() => open('processamento')}>Abrir workspace <b>→</b></button></div><div className="elo-mission-steps"><span><b>01</b> Intenção</span><span><b>02</b> Governança</span><span><b>03</b> Execução Hermes</span><span><b>04</b> Evidência e resultado</span></div></div>
        </section>

        <section aria-labelledby="workspace-title"><div className="elo-section-heading elo-section-heading--workspace"><div><span>WORKSPACE</span><h2 id="workspace-title">Camadas do núcleo</h2></div><span className="elo-section-note">Composição por capacidade · sem autoridade paralela</span></div>
          <div className="elo-card-grid">{(['memoria', 'processamento', 'decisao'] as const).map((key) => { const area = areas[key]; return <article className={`elo-module elo-module--${key}`} key={key}><span className="elo-module-kicker">{area.title.toUpperCase()}</span><span className="elo-module-icon" aria-hidden="true">{area.icon}</span><h3>{area.label}</h3><p>{area.text}</p><div className="elo-state-chip"><i /> {area.state}</div><button type="button" onClick={() => open(key)}>Abrir {area.title} <b>→</b></button></article>; })}</div>
        </section>

        <section className="elo-evidence-governance" aria-label="Evidência e governança">
          <article className="elo-evidence-panel"><span>EVIDÊNCIA</span><h2>Resultados precisam de contexto</h2><p>O frontend apresenta status, evidência e resultado recebidos do ELO. Não inventa telemetria nem transforma estado visual em autoridade.</p><div className="elo-evidence-row"><span>Proveniência</span><b>Aguardando dados</b></div><div className="elo-evidence-row"><span>Resultado</span><b>Não executado</b></div></article>
          <article className="elo-governance-panel"><span>GOVERNANÇA</span><h2>Autoridade permanece no ELO</h2><ul><li>Autorização e políticas fora do navegador</li><li>Hermes como runtime de execução</li><li>Segredos e credenciais nunca no bundle</li><li>Aprendizado somente por fluxo governado</li></ul></article>
        </section>

        <section className="elo-system-strip" aria-label="Estado da interface"><div><b>ESTADO</b><span>Pronta para interação</span></div><div><b>ACESSIBILIDADE</b><span>Foco por teclado e estados explícitos</span></div><div><b>DEPLOY TARGET</b><span>GitHub Pages · camada estática</span></div></section>
        <section className="elo-controls" aria-label="Som e notificações"><div><b>Preferências locais</b><span>Som e notificações são estados de interação do navegador.</span></div><label><span>Notificações</span><input type="checkbox" checked={notifications} onChange={(e) => { action(); setNotifications(e.target.checked); }} /></label><label><span>Alertas</span><input type="checkbox" checked={alerts} onChange={(e) => { action(); setAlerts(e.target.checked); }} /></label><label><span>Volume</span><input type="range" min="0" max="100" value={volume} onChange={(e) => setVolume(Number(e.target.value))} aria-label="Volume do som" /></label></section>
        {activeArea && <div className="elo-modal-backdrop" role="presentation" onClick={close}><section className="elo-modal" role="dialog" aria-modal="true" aria-labelledby="elo-modal-title" onClick={(e) => e.stopPropagation()}><span className="elo-eyebrow">{areas[activeArea].label.toUpperCase()}</span><h2 id="elo-modal-title">{areas[activeArea].title}</h2><p>{areas[activeArea].text}</p><div className="elo-modal-metrics"><span>Estado</span><b>{areas[activeArea].state}</b><span>Autoridade</span><b>ELO</b><span>Execução</span><b>Hermes quando governado</b></div><button type="button" onClick={close}>Fechar</button></section></div>}
      </section>
    </main>
  );
}
function Login() { return <ELOGoogleLogin><ELOCore /></ELOGoogleLogin>; }
export default function App() {
  return <Routes><Route path="/" element={<Login />} /><Route path="/login" element={<Login />} /><Route path="/auth/callback" element={<ELOAuthCallback />} /><Route path="/oauth/consent" element={<ELOOAuthConsent />} /><Route path="/app/*" element={<Login />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>;
}
