"use client";

import { useState } from "react";
import type { CognitiveResponse } from "@/lib/elo-cognitive";
import { EloOperationalData } from "@/components/elo-operational-data";

type Props = { onSignOut?: () => void; accessToken: string; displayName?: string | null };

function CognitiveResult({ result }: { result: CognitiveResponse }) {
  return (
    <section className="grid gap-4 xl:grid-cols-[1.5fr_0.8fr]">
      <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><div className="flex items-start justify-between gap-4"><div><h3 className="font-semibold">Resultado da missão</h3><p className="mt-1 text-xs text-slate-400">request {result.request_id.slice(0, 8)} · {Math.round(result.confidence * 100)}% confiança</p></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{result.provenance.validation_status ?? "processada"}</span></div><div className="mt-5 space-y-3 text-sm leading-6">{Object.entries(result.response).map(([key, value]) => <div key={key}><div className="text-xs font-medium uppercase tracking-wide text-slate-400">{key}</div><div className="mt-1 whitespace-pre-wrap">{typeof value === "string" ? value : JSON.stringify(value, null, 2)}</div></div>)}</div>{result.suggestions.length > 0 && <div className="mt-5"><h4 className="text-xs font-semibold uppercase tracking-wide text-slate-400">Próximas ações</h4><div className="mt-2 flex flex-wrap gap-2">{result.suggestions.map((item) => <span key={item.action_id} className="rounded-lg bg-slate-100 px-3 py-2 text-xs font-medium text-slate-700">{item.label}{item.requires_approval ? " · aprovação" : ""}</span>)}</div></div>}</article>
      <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><h3 className="font-semibold">Proveniência e controle</h3><div className="mt-4 space-y-3 text-sm"><div><span className="text-slate-400">Policy</span><div>{result.provenance.policy_decision ?? "não informado"}</div></div><div><span className="text-slate-400">Agentes</span><div>{result.agents_used.map((agent) => agent.agent_id).join(", ") || "nenhum informado"}</div></div><div><span className="text-slate-400">Evidências</span><div>{result.provenance.evidence_refs.length}</div></div><div><span className="text-slate-400">Processamento</span><div>{Math.round(result.processing_time_ms)} ms</div></div></div></article>
    </section>
  );
}

export function EloDashboard({ onSignOut, accessToken, displayName }: Props) {
  const [mission, setMission] = useState("");
  const [notice, setNotice] = useState<string | null>(null);
  const [result, setResult] = useState<CognitiveResponse | null>(null);
  const [busy, setBusy] = useState(false);

  async function runMission() {
    const request = mission.trim();
    if (!request || busy) return;
    setBusy(true); setNotice(null); setResult(null);
    try {
      const response = await fetch("/api/cognitive", {
        method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: `Bearer ${accessToken}` }, cache: "no-store",
        body: JSON.stringify({ message: request, tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner", domain: "planejamento", context: { sector: "Planejamento/PCP", surface: "Workspace", source: "elo-web", related_domains: ["pcp"] } }),
      });
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(typeof payload?.message === "string" ? payload.message : "Não foi possível concluir a análise. Tente novamente.");
      setResult(payload as CognitiveResponse);
      setMission("");
    } catch (error) { setNotice(error instanceof Error ? error.message : "Não foi possível concluir a análise."); }
    finally { setBusy(false); }
  }

  return <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]">
    <header className="border-b border-slate-200 bg-[var(--elo-panel)] px-5 py-4 lg:px-8">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4">
        <div><h1 className="text-xl font-semibold">ELO · Planejamento/PCP</h1><p className="mt-1 text-sm text-slate-600">Demandas, materiais e produção em um único espaço.</p></div>
        <div className="flex items-center gap-4"><span className="hidden text-sm text-slate-600 sm:block">{displayName || "Usuário ELO"}</span><button type="button" onClick={onSignOut} className="rounded-lg border border-slate-300 px-4 py-2 text-sm hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2">Sair</button></div>
      </div>
    </header>
    <div className="mx-auto max-w-7xl space-y-10 px-5 py-8 lg:px-8">
      <section aria-labelledby="consult-title">
        <h2 id="consult-title" className="text-2xl font-semibold">O que você precisa analisar?</h2>
        <p className="mt-2 max-w-prose text-sm leading-6 text-slate-600">Descreva a solicitação ou dúvida. O ELO consulta as fontes disponíveis e aponta evidências, pendências e próximos passos.</p>
        <form className="mt-4" onSubmit={(event) => { event.preventDefault(); void runMission(); }}>
          <label htmlFor="mission" className="block text-sm font-medium">Pedido ao ELO</label>
          <textarea id="mission" value={mission} onChange={(event) => setMission(event.target.value)} maxLength={4000} rows={3} disabled={busy} placeholder="Ex.: consultar materiais de um modelo e identificar o que falta validar." className="mt-2 w-full rounded-xl border border-slate-300 bg-[var(--elo-panel)] p-4 text-sm leading-6 placeholder:text-slate-500 focus-visible:outline-2 focus-visible:outline-offset-2" />
          <div className="mt-3 flex justify-end"><button type="submit" disabled={busy || !mission.trim()} className="rounded-lg bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800 focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-50">{busy ? "Analisando…" : "Consultar ELO"}</button></div>
        </form>
        {notice && <p role="alert" className="mt-3 text-sm text-red-700">{notice}</p>}
      </section>
      {result && <CognitiveResult result={result} />}
      <EloOperationalData accessToken={accessToken} />
    </div>
  </main>;
}
