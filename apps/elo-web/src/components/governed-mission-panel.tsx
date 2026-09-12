"use client";

import { useState } from "react";
import type { CognitiveResponse } from "@/lib/elo-cognitive";

type Props = { accessToken: string; sector: string; domain: string; workspace: string; activeSurface: string; onResult: (result: CognitiveResponse) => void; onNotice: (notice: string | null) => void; onBusyChange: (busy: boolean) => void };

export function GovernedMissionPanel({ accessToken, sector, domain, workspace, activeSurface, onResult, onNotice, onBusyChange }: Props) {
  const [mission, setMission] = useState("");
  const [runtimeProbe, setRuntimeProbe] = useState(false);

  async function submit(message: string, probe = false) {
    const request = message.trim();
    if (!request) return;
    onBusyChange(true); onNotice(null);
    try {
      const context: Record<string, unknown> = { sector, surface: activeSurface, workspace, source: "elo-web" };
      if (probe) context.hermes_mission = { mission_class: "runtime_probe", authorized_capabilities: ["hermes:runtime_probe"], method: "runtime_probe", constraints: { read_only: true, bounded: true, no_canonical_mutation: true }, evidence_requirements: ["execution", "outcome"] };
      const response = await fetch("/api/cognitive", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: `Bearer ${accessToken}` }, cache: "no-store", body: JSON.stringify({ message: request, tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner", domain, context }) });
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(typeof payload?.message === "string" ? payload.message : "O ELO não conseguiu processar a missão.");
      onResult(payload as CognitiveResponse); setMission(""); setRuntimeProbe(false);
      onNotice(probe ? "Probe Hermes enviada pelo fluxo cognitivo governado. Nenhum arquivo canônico foi autorizado para alteração." : "Missão processada pelo ELO Cognitivo.");
    } catch (error) { onNotice(error instanceof Error ? error.message : "Não foi possível processar a missão."); }
    finally { onBusyChange(false); }
  }

  return <section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm">
    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between"><div><div className="flex items-center gap-2"><h3 className="font-semibold">Missão ELO</h3><span className="rounded-full border border-slate-200 px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-slate-500">Governada</span></div><p className="mt-1 text-xs leading-5 text-slate-400">A intenção entra pelo Cognitivo. Hermes somente recebe missões explicitamente autorizadas.</p></div><button type="button" onClick={() => setRuntimeProbe((value) => !value)} className={`rounded-xl border px-3 py-2 text-xs font-semibold ${runtimeProbe ? "border-slate-900 bg-slate-900 text-white" : "border-slate-200 text-slate-600"}`}>{runtimeProbe ? "Probe Hermes selecionado" : "Testar Hermes"}</button></div>
    {runtimeProbe && <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4 text-xs text-slate-600"><div className="font-semibold">runtime_probe</div><div className="mt-1">Somente leitura · capacidade pré-autorizada · Evidence/Outcome obrigatórios · sem mutação canônica.</div><button type="button" onClick={() => void submit("Executar probe governado do runtime Hermes e retornar Evidence/Outcome.", true)} className="mt-3 rounded-lg bg-slate-900 px-3 py-2 font-semibold text-white">Executar probe</button></div>}
    <div className="mt-4 flex gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2"><input value={mission} onChange={(event) => setMission(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") void submit(mission); }} placeholder={`Solicite algo para ${sector.toLowerCase()}…`} className="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none"/><button type="button" onClick={() => void submit(mission)} className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white">Enviar</button></div>
    <div className="mt-4 grid grid-cols-1 gap-2 text-xs text-slate-500 sm:grid-cols-3"><div className="rounded-lg bg-slate-50 p-3">Browser → API Cognitive</div><div className="rounded-lg bg-slate-50 p-3">Symbiont → Hermes</div><div className="rounded-lg bg-slate-50 p-3">Evidence → Evolution Gate</div></div>
  </section>;
}
