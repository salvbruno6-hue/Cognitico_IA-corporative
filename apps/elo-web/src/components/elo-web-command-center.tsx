"use client";

import { useMemo, useState } from "react";
import type { CognitiveResponse } from "@/lib/elo-cognitive";
import { sectors, type SectorKey } from "@/lib/sectors";

type Props = { accessToken: string; onSignOut?: () => void };
type ErrorPayload = { message?: unknown };

const workspaces: Record<SectorKey, { objective: string; queue: string; signals: string[] }> = {
  planejamento: { objective: "Decidir, orçar e encaminhar demandas", queue: "Solicitações e licitações", signals: ["Demanda", "Análise", "Evidência", "Decisão"] },
  comercial: { objective: "Transformar oportunidades em decisões comerciais", queue: "Leads e propostas", signals: ["Lead", "Oportunidade", "Proposta", "Risco"] },
  financeiro: { objective: "Projetar recursos e proteger o caixa", queue: "Receitas e previsões", signals: ["Caixa", "Receber", "Pagar", "Risco"] },
  rh: { objective: "Apoiar pessoas e decisões organizacionais", queue: "Pessoas e desenvolvimento", signals: ["Pessoas", "Vagas", "Clima", "Desenvolvimento"] },
  operacoes: { objective: "Orquestrar processos e remover gargalos", queue: "Processos e incidentes", signals: ["Processo", "SLA", "Incidente", "Fornecedor"] },
  pcp: { objective: "Conectar capacidade, materiais e produção", queue: "Ordens e capacidade", signals: ["Ordem", "Capacidade", "Material", "Gargalo"] },
  ti: { objective: "Manter sistemas seguros e disponíveis", queue: "Sistemas e riscos", signals: ["Sistema", "Chamado", "Disponibilidade", "Segurança"] },
};

function isErrorPayload(value: unknown): value is ErrorPayload {
  return typeof value === "object" && value !== null && "message" in value;
}

export function EloWebCommandCenter({ accessToken, onSignOut }: Props) {
  const [sectorKey, setSectorKey] = useState<SectorKey>("planejamento");
  const [mission, setMission] = useState("");
  const [result, setResult] = useState<CognitiveResponse | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const workspace = useMemo(() => workspaces[sectorKey], [sectorKey]);
  const sector = useMemo(() => sectors.find((item) => item.key === sectorKey) ?? sectors[0], [sectorKey]);

  async function execute(text = mission) {
    const request = text.trim();
    if (!request || busy) return;
    setBusy(true); setNotice(null); setResult(null);
    try {
      const response = await fetch("/api/cognitive", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: `Bearer ${accessToken}` },
        cache: "no-store",
        body: JSON.stringify({
          message: request,
          tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner",
          domain: sector.key,
          context: { sector: sector.label, surface: "command-center", workspace: workspace.objective, source: "elo-web" },
        }),
      });
      const payload: unknown = await response.json().catch(() => null);
      if (!response.ok) {
        const message = isErrorPayload(payload) && typeof payload.message === "string" ? payload.message : "O ELO não autorizou esta missão.";
        throw new Error(message);
      }
      setResult(payload as CognitiveResponse);
      setMission("");
      setNotice("Missão recebida pelo ELO Cognitivo. A execução permanece dentro do boundary governado.");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Falha ao processar a missão.");
    } finally { setBusy(false); }
  }

  return (
    <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]">
      <div className="flex min-h-screen">
        <aside className="hidden w-64 shrink-0 border-r border-slate-200 bg-slate-950 px-4 py-6 text-white lg:block">
          <div className="flex items-center gap-3 px-2"><div className="grid size-10 place-items-center rounded-2xl border border-white/20 bg-white/10 text-lg font-bold">E</div><div><div className="text-lg font-bold tracking-wide">ELO</div><div className="text-[9px] uppercase tracking-[.22em] text-white/40">Command Center</div></div></div>
          <div className="mt-10 px-2 text-[10px] font-semibold uppercase tracking-[.2em] text-white/35">Domínios</div>
          <nav className="mt-3 space-y-1" aria-label="Domínios ELO">
            {sectors.map((item) => <button key={item.key} type="button" onClick={() => { setSectorKey(item.key); setResult(null); setNotice(null); }} className={`w-full rounded-xl px-3 py-2.5 text-left text-sm transition ${item.key === sectorKey ? "bg-white text-slate-950 font-semibold" : "text-white/65 hover:bg-white/10 hover:text-white"}`}>{item.label}</button>)}
          </nav>
          <div className="mt-8 rounded-2xl border border-white/10 bg-white/[.04] p-4"><div className="text-[10px] uppercase tracking-[.18em] text-white/35">Arquitetura</div><div className="mt-3 space-y-2 text-xs text-white/65"><div>ELO Cognitivo <span className="float-right text-emerald-300">ATIVO</span></div><div>Symbiont <span className="float-right text-sky-300">BOUND</span></div><div>Hermes <span className="float-right text-violet-300">GOVERNADO</span></div><div>Evolution Gate <span className="float-right text-amber-300">PROTEGIDO</span></div></div></div>
          <a href="/terminal" className="mt-4 block rounded-xl border border-white/10 px-3 py-2.5 text-center text-sm text-white/70 hover:bg-white/10 hover:text-white">Abrir Terminal Hermes</a>
        </aside>

        <section className="min-w-0 flex-1">
          <header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200/80 bg-[var(--elo-bg)]/90 px-5 py-4 backdrop-blur lg:px-8">
            <div><div className="text-[10px] font-semibold uppercase tracking-[.2em] text-slate-400">ELO / Command Center</div><h1 className="mt-1 text-xl font-semibold">{sector.label}</h1></div>
            <div className="flex items-center gap-2"><span className="hidden rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 sm:inline-flex">● Cognitivo ativo</span><button type="button" onClick={onSignOut} className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50">Sair</button></div>
          </header>

          <div className="mx-auto max-w-7xl space-y-6 p-5 lg:p-8">
            <section className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm lg:p-8"><div className="absolute right-0 top-0 h-48 w-48 rounded-full bg-slate-100 blur-3xl"/><div className="relative"><div className="flex flex-col justify-between gap-5 md:flex-row md:items-end"><div className="max-w-3xl"><div className="text-xs font-bold uppercase tracking-[.2em]" style={{ color: sector.accent }}>Inteligência corporativa</div><h2 className="mt-2 text-3xl font-semibold tracking-tight lg:text-4xl">{workspace.objective}</h2><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">O ELO transforma intenção em missão, aplica governança e retorna decisão com evidência e proveniência.</p></div><div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-xs"><div className="text-slate-400">Fila operacional</div><div className="mt-1 font-semibold text-slate-800">{workspace.queue}</div></div></div><div className="mt-7 grid gap-3 md:grid-cols-4">{workspace.signals.map((signal, i) => <div key={signal} className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4"><div className="text-[10px] font-bold text-slate-400">0{i + 1}</div><div className="mt-2 text-sm font-semibold">{signal}</div></div>)}</div></div></section>

            <section className="rounded-[2rem] border border-slate-200 bg-slate-950 p-5 text-white shadow-lg lg:p-6"><div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between"><div><div className="text-[10px] font-bold uppercase tracking-[.2em] text-white/35">Mission Control</div><h3 className="mt-1 text-lg font-semibold">O que o ELO deve decidir?</h3></div><div className="text-xs text-white/40">Intenção → Cognitivo → Evidência → Decisão</div></div><form className="mt-5" onSubmit={(e) => { e.preventDefault(); void execute(); }}><textarea value={mission} onChange={(e) => setMission(e.target.value.slice(0, 4000))} disabled={busy} rows={4} placeholder="Descreva a demanda, análise ou decisão que precisa ser processada pelo ELO…" className="w-full resize-none rounded-2xl border border-white/10 bg-white/[.06] px-4 py-4 text-sm leading-6 text-white outline-none placeholder:text-white/30 focus:border-white/30 focus:ring-2 focus:ring-white/10 disabled:opacity-50"/><div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"><span className="text-xs text-white/35">Domínio: {sector.label} · limite 4.000 caracteres</span><button type="submit" disabled={busy || !mission.trim()} className="rounded-xl bg-white px-5 py-2.5 text-sm font-bold text-slate-950 disabled:cursor-not-allowed disabled:opacity-35">{busy ? "Processando…" : "Executar missão →"}</button></div></form></section>

            {notice && <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-600" role="status">{notice}</div>}
            {result && <section className="grid gap-4 xl:grid-cols-[1.5fr_.7fr]"><article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-start justify-between gap-4"><div><div className="text-[10px] font-bold uppercase tracking-[.18em] text-slate-400">Resultado</div><h3 className="mt-1 font-semibold">Resposta do ELO Cognitivo</h3></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{result.provenance.validation_status ?? "processada"}</span></div><div className="mt-5 space-y-4">{Object.entries(result.response).map(([key, value]) => <div key={key} className="rounded-xl bg-slate-50 p-4"><div className="text-[10px] font-bold uppercase tracking-[.16em] text-slate-400">{key}</div><div className="mt-1 whitespace-pre-wrap text-sm leading-6">{typeof value === "string" ? value : JSON.stringify(value, null, 2)}</div></div>)}</div></article><article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="text-[10px] font-bold uppercase tracking-[.18em] text-slate-400">Governança</div><h3 className="mt-1 font-semibold">Proveniência</h3><dl className="mt-5 space-y-4 text-sm"><div><dt className="text-xs text-slate-400">Policy</dt><dd className="mt-1 font-medium">{result.provenance.policy_decision ?? "não informado"}</dd></div><div><dt className="text-xs text-slate-400">Evidências</dt><dd className="mt-1 font-medium">{result.provenance.evidence_refs.length}</dd></div><div><dt className="text-xs text-slate-400">Confiança</dt><dd className="mt-1 font-medium">{Math.round(result.confidence * 100)}%</dd></div><div><dt className="text-xs text-slate-400">Processamento</dt><dd className="mt-1 font-medium">{Math.round(result.processing_time_ms)} ms</dd></div></dl></article></section>}
          </div>
        </section>
      </div>
    </main>
  );
}
