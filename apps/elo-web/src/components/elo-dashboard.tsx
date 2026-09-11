"use client";

import { useEffect, useMemo, useState } from "react";
import { sectors, type SectorKey } from "@/lib/sectors";
import { DEFAULT_ELO_SETTINGS, loadELOSettings, persistELOSettings, type ELOSettings } from "@/lib/elo-settings";
import { EloSettingsPanel } from "@/components/elo-settings-panel";
import type { CognitiveResponse } from "@/lib/elo-cognitive";

type Props = { onSignOut?: () => void; accessToken: string };
const navItems = ["Início", "Missões", "Projetos", "Análises", "Conectores", "Governança"];
const sectorActionHelp: Record<SectorKey, string[]> = {
  planejamento: ["Nova solicitação", "Analisar orçamento", "Consultar ELO", "Abrir relatório"],
  comercial: ["Qualificar lead", "Gerar proposta", "Analisar conversão", "Identificar risco"],
  financeiro: ["Gerar relatório", "Analisar despesas", "Prever fluxo", "Ver inadimplência"],
  rh: ["Abrir vaga", "Analisar clima", "Plano de desenvolvimento", "Relatório de desempenho"],
  operacoes: ["Iniciar processo", "Verificar gargalos", "Gerar relatório", "Acompanhar fornecedor"],
  pcp: ["Programar produção", "Ver Gantt", "Analisar estoque", "Detectar gargalo"],
  ti: ["Abrir chamado", "Ver status", "Analisar vulnerabilidades", "Gerar relatório"],
};
const sectorDescriptions: Record<SectorKey, string> = {
  planejamento: "Entrada de demandas, análise, orçamento e encaminhamento governado.",
  comercial: "Oportunidades, propostas e riscos comerciais.", financeiro: "Leitura financeira e apoio a decisões de recursos.", rh: "Pessoas, desenvolvimento e indicadores organizacionais.", operacoes: "Coordenação operacional, incidentes e desempenho.", pcp: "Capacidade, programação, materiais e gargalos de produção.", ti: "Sistemas, suporte, disponibilidade e segurança.",
};

function CognitiveResult({ result }: { result: CognitiveResponse }) {
  return <section className="grid gap-4 xl:grid-cols-[1.5fr_0.8fr]">
    <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4"><div><h3 className="font-semibold">Resposta cognitiva</h3><p className="mt-1 text-xs text-slate-400">request {result.request_id.slice(0, 8)} · {Math.round(result.confidence * 100)}% de confiança</p></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{result.provenance.validation_status ?? "processada"}</span></div>
      <div className="mt-5 space-y-3 text-sm leading-6">{Object.entries(result.response).map(([key, value]) => <div key={key}><dt className="text-xs font-medium uppercase tracking-wide text-slate-400">{key}</dt><dd className="mt-1 whitespace-pre-wrap">{typeof value === "string" ? value : JSON.stringify(value, null, 2)}</dd></div>)}</div>
      {result.suggestions.length > 0 && <div className="mt-5"><h4 className="text-xs font-semibold uppercase tracking-wide text-slate-400">Próximas ações sugeridas</h4><div className="mt-2 flex flex-wrap gap-2">{result.suggestions.map((item) => <span key={item.action_id} className="rounded-lg bg-slate-100 px-3 py-2 text-xs font-medium text-slate-700">{item.label}{item.requires_approval ? " · aprovação" : ""}</span>)}</div></div>}
    </article>
    <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><h3 className="font-semibold">Proveniência</h3><div className="mt-4 space-y-3 text-sm"><div><span className="text-slate-400">Policy</span><div>{result.provenance.policy_decision ?? "não informado"}</div></div><div><span className="text-slate-400">Agentes</span><div>{result.agents_used.map((agent) => agent.agent_id).join(", ") || "nenhum informado"}</div></div><div><span className="text-slate-400">Evidências</span><div>{result.provenance.evidence_refs.length}</div></div><div><span className="text-slate-400">Processamento</span><div>{Math.round(result.processing_time_ms)} ms</div></div></div></article>
  </section>;
}

export function EloDashboard({ onSignOut, accessToken }: Props) {
  const [sectorKey, setSectorKey] = useState<SectorKey>("planejamento");
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settings, setSettings] = useState<ELOSettings>(DEFAULT_ELO_SETTINGS);
  const [activeNav, setActiveNav] = useState("Início");
  const [mission, setMission] = useState("");
  const [notice, setNotice] = useState<string | null>(null);
  const [result, setResult] = useState<CognitiveResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const sector = useMemo(() => sectors.find((item) => item.key === sectorKey) ?? sectors[0], [sectorKey]);
  const actions = sectorActionHelp[sectorKey];

  useEffect(() => { setSettings(loadELOSettings()); }, []);
  useEffect(() => { document.documentElement.dataset.theme = settings.theme; document.documentElement.style.colorScheme = settings.theme; }, [settings.theme]);
  function handleSettingsChange(next: ELOSettings) { setSettings(next); persistELOSettings(next); }
  function playFeedbackTone() { if (!settings.soundEnabled || typeof window === "undefined") return; try { const AudioContextClass = window.AudioContext ?? (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext; if (!AudioContextClass) return; const context = new AudioContextClass(); const oscillator = context.createOscillator(); const gain = context.createGain(); oscillator.frequency.value = 660; gain.gain.value = 0.025; oscillator.connect(gain); gain.connect(context.destination); oscillator.start(); oscillator.stop(context.currentTime + 0.06); void context.close(); } catch { /* optional feedback */ } }

  async function runMission(requestText: string) {
    const request = requestText.trim();
    if (!request || busy) return;
    setBusy(true); setNotice(null); setResult(null);
    try {
      const response = await fetch("/api/cognitive", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: `Bearer ${accessToken}` }, cache: "no-store", body: JSON.stringify({ message: request, tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner", principal_id: undefined, domain: sector.key, context: { sector: sector.label, surface: activeNav, source: "elo-web" } }) });
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(typeof payload?.message === "string" ? payload.message : "Não foi possível processar a missão pelo ELO Cognitivo.");
      setResult(payload as CognitiveResponse); setNotice("Missão processada pelo ELO Cognitivo. A interface mostra resposta, proveniência e evidências devolvidas pelo contrato."); setMission(""); playFeedbackTone();
    } catch (error) { setNotice(error instanceof Error ? error.message : "Não foi possível processar a missão."); }
    finally { setBusy(false); }
  }

  return <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]"><div className="flex min-h-screen flex-col lg:flex-row">
    <aside className="w-full border-b border-white/10 bg-[var(--elo-sidebar)] p-4 text-white lg:min-h-screen lg:w-72 lg:border-b-0 lg:border-r"><div className="mb-8 flex items-center gap-3 px-2"><div className="grid size-10 place-items-center rounded-full border border-white/40 text-lg font-semibold">C</div><div><div className="text-xl font-semibold tracking-wide">ELO</div><div className="text-[10px] uppercase tracking-[0.24em] text-white/50">Inteligência corporativa</div></div></div><nav aria-label="Navegação principal" className="space-y-1">{navItems.map((item) => <button key={item} type="button" onClick={() => setActiveNav(item)} className={`w-full rounded-xl px-4 py-3 text-left text-sm transition ${activeNav === item ? "bg-white/10 font-medium text-white" : "text-white/70 hover:bg-white/10 hover:text-white"}`}>{item === "Início" ? "⌂" : "•"} {item}</button>)}</nav><div className="mt-8 border-t border-white/10 pt-5"><div className="mb-2 px-2 text-xs font-medium uppercase tracking-wider text-white/40">Setor atual</div><div className="space-y-2">{sectors.map((item) => <button key={item.key} type="button" onClick={() => { setSectorKey(item.key); setActiveNav("Início"); setNotice(null); setResult(null); }} aria-current={sectorKey === item.key ? "page" : undefined} className={`w-full rounded-xl border px-3 py-2.5 text-left text-sm transition ${sectorKey === item.key ? "border-white/20 bg-white/15 text-white" : "border-white/5 bg-white/5 text-white/65 hover:bg-white/10 hover:text-white"}`}>{item.label}</button>)}</div></div><button type="button" onClick={() => setSettingsOpen(true)} className="mt-5 flex w-full items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white/80 hover:bg-white/10 hover:text-white"><span>⚙ Configurações</span><span className="text-xs text-white/40">Interface · Canais</span></button></aside>
    <section className="flex min-w-0 flex-1 flex-col"><header className="flex items-center justify-between gap-4 border-b border-slate-200 bg-[var(--elo-panel)]/90 px-5 py-4 backdrop-blur lg:px-8"><div><div className="text-xs text-slate-400">ELO / {activeNav}</div><h1 className="text-2xl font-semibold tracking-tight">{sector.label}</h1></div><div className="flex items-center gap-2"><button type="button" onClick={() => setSettingsOpen(true)} className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50" aria-label="Configurações">⚙</button><button type="button" onClick={onSignOut} className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm">Sair</button><div className="hidden text-sm text-slate-500 sm:block">Bruno</div><div className="grid size-9 place-items-center rounded-full bg-slate-200 text-sm font-semibold text-slate-700">B</div></div></header>
      <div className="flex-1 space-y-6 p-5 lg:p-8">{notice && <div className="rounded-xl border border-slate-200 bg-[var(--elo-panel)] px-4 py-3 text-sm text-slate-600" role="status">{notice}</div>}
        <div className="grid gap-4 xl:grid-cols-[1.4fr_1fr]"><section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-6 shadow-sm"><p className="mb-2 text-sm font-medium" style={{ color: sector.accent }}>ELO • {sector.label}</p><h2 className="max-w-2xl text-3xl font-semibold tracking-tight">{sector.subtitle}</h2><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">{sectorDescriptions[sectorKey]}</p><div className="mt-6 flex flex-wrap gap-3"><button type="button" disabled={busy} onClick={() => void runMission("Criar uma missão governada para este setor")} className="rounded-xl px-4 py-3 text-sm font-semibold text-white shadow-sm disabled:opacity-60" style={{ backgroundColor: sector.accent }}>{busy ? "Processando…" : "Criar missão"}</button><button type="button" disabled={busy} onClick={() => void runMission("Analise os dados relevantes disponíveis para este setor e indique evidências e próximos passos")} className="rounded-xl border border-slate-200 bg-transparent px-4 py-3 text-sm font-semibold text-slate-700 disabled:opacity-60">Analisar dados</button></div></section>
          <section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><label htmlFor="mission" className="mb-2 block text-sm font-medium text-slate-700">Pergunte ou solicite algo</label><div className="flex gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2"><input id="mission" value={mission} onChange={(event) => setMission(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") void runMission(mission); }} placeholder={`Ex.: analise a carteira de ${sector.label.toLowerCase()}`} disabled={busy} className="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none"/><button type="button" onClick={() => void runMission(mission)} disabled={busy} className="rounded-lg px-4 py-2 text-sm font-semibold text-white disabled:opacity-60" style={{ backgroundColor: sector.accent }}>➤</button></div><div className="mt-4 grid grid-cols-2 gap-2 text-xs text-slate-500"><div className="rounded-lg bg-slate-50 p-3">Governança ativa</div><div className="rounded-lg bg-slate-50 p-3">Cognitivo → Simbionte → Hermes</div></div></section></div>
        {result && <CognitiveResult result={result} />}
        <section aria-label="Indicadores principais" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{sector.metrics.map((metric) => <article key={metric.label} className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><p className="text-xs font-medium text-slate-500">{metric.label}</p><div className="mt-2 flex items-end justify-between gap-2"><strong className="text-2xl tracking-tight">{metric.value}</strong><span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">Sem dado</span></div></article>)}</section>
        <section className="grid gap-4 xl:grid-cols-[1.5fr_0.8fr]"><article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><div className="mb-5 flex items-center justify-between"><div><h3 className="font-semibold">Telemetria cognitiva</h3><p className="text-xs text-slate-400">Sem dados governados ativos, o ELO não fabrica métricas.</p></div><span className="rounded-lg bg-slate-50 px-3 py-2 text-xs text-slate-500">Aguardando</span></div><div className="grid min-h-36 place-items-center rounded-xl border border-dashed border-slate-200 text-sm text-slate-400">Conecte a fonte cognitiva para visualizar indicadores reais</div></article><article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><h3 className="font-semibold">Ações do setor</h3><p className="mt-1 text-xs text-slate-400">A ação é enviada ao ELO Cognitivo; Hermes só executa uma missão autorizada pelo boundary.</p><div className="mt-4 space-y-2">{actions.map((action) => <button key={action} type="button" disabled={busy} onClick={() => void runMission(action)} className="flex w-full items-center justify-between rounded-xl border border-slate-200 px-3 py-3 text-left text-sm transition hover:bg-slate-50 disabled:opacity-60"><span>{action}</span><span className="text-slate-400">→</span></button>)}</div></article></section>
        <footer className="flex flex-col gap-2 border-t border-slate-200 pt-5 text-xs text-slate-400 sm:flex-row sm:items-center sm:justify-between"><span>ELO • Inteligência para um futuro melhor.</span><span>GPT → Cognitivo → Simbionte → Hermes → Evidência → Governança</span></footer>
      </div>
    </section>
  </div>
  <EloSettingsPanel open={settingsOpen} onClose={() => setSettingsOpen(false)} onChange={handleSettingsChange} />
  </main>;
}
