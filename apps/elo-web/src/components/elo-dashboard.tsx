"use client";

import { useEffect, useRef, useState } from "react";
import type { CognitiveResponse } from "@/lib/elo-cognitive";
import { workspaceAreas, isEvidenceBacked } from "@/lib/workspace";
import { EloOperationalData } from "@/components/elo-operational-data";
import { EloWorkspaceTool } from "@/components/elo-workspace-tool";
import { DEFAULT_ELO_SETTINGS, loadELOSettings, persistELOSettings } from "@/lib/elo-settings";

type Props = { onSignOut?: () => void; accessToken: string; displayName?: string | null; initialArea?: string };

export function EloDashboard({ onSignOut, accessToken, displayName, initialArea = "orquestrador" }: Props) {
  const [active, setActive] = useState(initialArea);
  const area = workspaceAreas.find(item => item.key === active) ?? workspaceAreas[0];
  const [mission, setMission] = useState("");
  const [notice, setNotice] = useState<string | null>(null);
  const [result, setResult] = useState<CognitiveResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [theme, setTheme] = useState("dark");
  const [sound, setSound] = useState(false);
  const missionController = useRef<AbortController | null>(null);
  useEffect(() => { const saved = loadELOSettings(); setTheme(saved.theme); setSound(saved.soundEnabled); }, []);
  useEffect(() => () => missionController.current?.abort(), []);
  function switchArea(key: string) { missionController.current?.abort(); setBusy(false); setActive(key); setNotice(null); setResult(null); setMission(""); }
  async function runMission() {
    const request = mission.trim(); if (!request || busy) return;
    const controller = new AbortController(); missionController.current = controller;
    setBusy(true); setNotice(null); setResult(null);
    try {
      const response = await fetch("/api/cognitive", {
        method: "POST", signal: controller.signal, headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: `Bearer ${accessToken}` }, cache: "no-store",
        body: JSON.stringify({ message: request, tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner", domain: "planejamento", context: { sector: "Planejamento/PCP", surface: area.label, source: "elo-web" } }),
      });
      const payload = await response.json().catch(() => null);
      if (!response.ok || !payload?.response || !payload?.provenance) throw new Error("Não foi possível concluir o pedido. Tente novamente.");
      if (!controller.signal.aborted) {
        if (!isEvidenceBacked(payload)) setNotice("O serviço respondeu sem fontes ou evidências consultadas. Esta resposta não comprova uma análise. Use as consultas disponíveis abaixo para verificar os dados do ELO.");
        else setResult(payload as CognitiveResponse);
      }
    } catch (error) { if (!controller.signal.aborted) setNotice(error instanceof Error ? error.message : "Não foi possível concluir o pedido."); }
    finally { if (!controller.signal.aborted) setBusy(false); }
  }
  function preferences(nextTheme: string, nextSound: boolean) {
    setTheme(nextTheme); setSound(nextSound);
    const saved = loadELOSettings(); persistELOSettings({ ...DEFAULT_ELO_SETTINGS, ...saved, theme: nextTheme === "light" ? "light" : "dark", soundEnabled: nextSound });
  }
  const toolProps = { accessToken };
  return <main className="elo-workspace min-h-screen" data-workspace-theme={theme}>
    <a href="#workspace-content" className="workspace-skip">Ir para o conteúdo</a>
    <header className="workspace-header"><div className="flex min-w-0 items-center gap-4"><div className="workspace-logo" aria-hidden="true">E</div><div><h1 className="text-xl font-semibold">ELO Orquestrador</h1><p className="mt-1 text-sm text-slate-600">Workspace Operacional · Multiteiner</p></div></div><div className="flex items-center gap-4"><span className="hidden text-sm text-slate-600 sm:block">{displayName || "Usuário ELO"}</span><button type="button" onClick={onSignOut} className="workspace-secondary">Sair</button></div></header>
    <nav aria-label="Áreas do workspace" className="workspace-nav">{workspaceAreas.map(item => <button key={item.key} type="button" onClick={() => switchArea(item.key)} aria-current={area.key === item.key ? "page" : undefined} className={area.key === item.key ? "is-active" : ""}>{item.label}</button>)}</nav>
    <div id="workspace-content" className="workspace-content" tabIndex={-1}>
      <div className="mb-8"><h2 className="text-3xl font-semibold tracking-tight">{area.label}</h2><p className="mt-3 max-w-prose text-sm leading-6 text-slate-600">{area.description}</p></div>
      {(active === "orquestrador" || active === "pcp") && <>
        <section className="workspace-panel"><h2 className="text-xl font-semibold">Pedido ao ELO</h2><p className="mt-2 text-sm leading-6 text-slate-600">Descreva o que precisa verificar. Uma resposta só será exibida como análise quando trouxer referências de evidência.</p><form className="mt-4" onSubmit={event => { event.preventDefault(); void runMission(); }}><label htmlFor="mission" className="block text-sm font-medium">Sua solicitação</label><textarea id="mission" value={mission} onChange={event => setMission(event.target.value)} maxLength={4000} rows={3} disabled={busy} placeholder="Descreva a demanda, dúvida ou decisão…" className="workspace-input mt-2" /><div className="mt-3 flex justify-end"><button type="submit" disabled={busy || !mission.trim()} className="workspace-primary">{busy ? "Consultando…" : "Enviar pedido ao ELO"}</button></div></form>{notice && <p role="status" className="mt-4 text-sm leading-6">{notice}</p>}{result && <div className="mt-5"><h3 className="font-semibold">Resposta com referências de evidência</h3><div className="mt-3 whitespace-pre-wrap text-sm leading-6">{typeof result.response.content === "string" ? result.response.content : JSON.stringify(result.response, null, 2)}</div><details className="mt-4"><summary className="text-sm">Ver fontes e proveniência</summary><pre className="mt-3 overflow-auto whitespace-pre-wrap text-xs">{JSON.stringify({ sources: result.sources, provenance: result.provenance }, null, 2)}</pre></details></div>}</section>
        <div className="workspace-grid"><EloWorkspaceTool {...toolProps} tool="elo_pcp_dados_pendentes" title="Pendências e recomendações" description="Dado necessário, fonte autorizada, motivo e próxima pergunta." /><EloWorkspaceTool {...toolProps} tool="elo_pcp_comunicacao_melhoria" title="Orientações de melhoria" description="Pontos faltantes e orientações produzidos pelo mecanismo de comunicação existente." /></div>
        <EloWorkspaceTool {...toolProps} tool="elo_pcp_decisao_externa_status" title="Decisão externa" description="Resumo, impactos e informações que ainda precisam ser validadas." />
      </>}
      {(active === "dashboard" || active === "pcp") && <EloWorkspaceTool {...toolProps} tool="elo_pcp_demanda_crossing_status" title="Cruzamento de demanda" description="Histórico comparável, fatores e projeções devolvidos pelo ELO. A consulta não executa uma simulação." />}
      {active === "notificacoes" && <EloWorkspaceTool {...toolProps} tool="elo_pcp_dados_pendentes" title="Pontos de atenção" description="Pendências reais consultadas no ELO. Ausência nesta fila não comprova ausência de outros alertas." />}
      {active === "chat" && <EloWorkspaceTool {...toolProps} tool="elo_pcp_orquestrador_dialogo" dialogue title="Diálogo com o ELO" description="Complete os dados solicitados pelo mecanismo de diálogo existente de Planejamento/PCP." />}
      {(active === "catalogo" || active === "pcp") && <section className="workspace-panel"><EloOperationalData accessToken={accessToken} compact={active === "pcp"} /></section>}
      {active === "configuracoes" && <>
        <section className="workspace-panel"><h2 className="text-xl font-semibold">Preferências</h2><div className="mt-5 flex flex-wrap gap-6"><label className="text-sm font-medium">Aparência<select value={theme} onChange={event => preferences(event.target.value, sound)} className="workspace-input mt-2"><option value="dark">Escura</option><option value="light">Clara</option></select></label><label className="flex items-center gap-3 text-sm"><input type="checkbox" checked={sound} onChange={event => preferences(theme, event.target.checked)} />Preferência de som</label></div><p className="mt-4 text-sm text-slate-600">Preferências salvas neste navegador. Não alteram permissões nem dados da empresa.</p></section>
        <EloWorkspaceTool {...toolProps} tool="elo_status" title="Meu acesso" description="Identidade e papéis retornados pela autorização existente do ELO." />
      </>}
      {area.sections.length > 0 && <section className="workspace-panel"><h2 className="text-xl font-semibold">{["orquestrador", "catalogo", "pcp", "chat", "notificacoes", "configuracoes", "dashboard"].includes(active) ? "Integrações a completar" : "Acompanhamento da área"}</h2><div className="mt-5 divide-y divide-slate-200">{area.sections.map(section => <article key={section.label} className="py-5 first:pt-0 last:pb-0"><div className="flex flex-wrap items-center justify-between gap-2"><h3 className="font-semibold">{section.label}</h3><span className="text-xs text-slate-600">Integração pendente</span></div><p className="mt-2 max-w-prose text-sm leading-6 text-slate-600">{section.gap}</p>{section.sources.length > 0 && <details className="mt-3 text-sm"><summary className="cursor-pointer">Ver fontes identificadas</summary><ul className="mt-2 space-y-1 text-xs text-slate-600">{section.sources.map(source => <li key={source}>{source}</li>)}</ul></details>}</article>)}</div></section>}
      <footer className="mt-8 text-sm text-slate-600">Planejamento e PCP formam uma única área. Os dados e operações seguem as permissões da sua sessão.</footer>
    </div>
  </main>;
}
