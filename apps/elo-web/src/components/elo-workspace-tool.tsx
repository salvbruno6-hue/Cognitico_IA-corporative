"use client";

import { useEffect, useState, useRef, type FormEvent } from "react";
import { callWorkspaceTool, type MCPValue, type WorkspaceTool } from "@/lib/elo-workspace-mcp";

const label = (key: string) => key.replaceAll("_", " ");
function DataValue({ value }: { value: unknown }) {
  if (value == null || value === "") return <span className="text-slate-500">Não informado</span>;
  if (Array.isArray(value)) return value.length ? <ul className="space-y-4">{value.map((item, i) => <li key={i} className="border-b border-slate-200 pb-3 last:border-0"><DataValue value={item} /></li>)}</ul> : <span className="text-slate-500">Nenhum registro retornado</span>;
  if (typeof value === "object") return <dl className="space-y-3">{Object.entries(value).map(([key, item]) => <div key={key}><dt className="text-sm font-semibold">{label(key)}</dt><dd className="mt-1 text-sm leading-6"><DataValue value={item} /></dd></div>)}</dl>;
  return <span className="whitespace-pre-wrap break-words">{typeof value === "boolean" ? (value ? "Sim" : "Não") : String(value)}</span>;
}

export function EloWorkspaceTool({ accessToken, tool, title, description, dialogue = false }: { accessToken: string; tool: WorkspaceTool; title: string; description: string; dialogue?: boolean }) {
  const [data, setData] = useState<MCPValue | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [revision, setRevision] = useState(0);
  const [reply, setReply] = useState("");
  const [source, setSource] = useState("");
  const [fields, setFields] = useState<Record<string, string>>({});
  const [sessionId, setSessionId] = useState<string | undefined>();
  const sending = useRef(false);
  const submitController = useRef<AbortController | null>(null);
  useEffect(() => () => submitController.current?.abort(), []);
  useEffect(() => {
    const controller = new AbortController();
    setBusy(true); setError(null); setData(null);
    const baseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
    if (!baseUrl) { setError("Consulta não configurada. Contate o administrador."); setBusy(false); return () => controller.abort(); }
    const args = {};
    void callWorkspaceTool(baseUrl, accessToken, tool, args, controller.signal)
      .then(result => { if (!controller.signal.aborted) { setData(result); if (typeof result.sessao_id === "string") setSessionId(result.sessao_id); } })
      .catch(reason => { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : "A consulta falhou."); })
      .finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [accessToken, tool, revision]);
  const missing = Array.isArray(data?.campos_faltantes) ? data.campos_faltantes.filter((field): field is string => typeof field === "string") : [];
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (sending.current || busy) return;
    const baseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
    if (!baseUrl) { setError("Consulta não configurada. Contate o administrador."); return; }
    const explicitFields: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(fields)) {
      if (!value.trim()) continue;
      explicitFields[key] = key === "quantidade_real" && Number.isFinite(Number(value.replace(",", "."))) ? Number(value.replace(",", ".")) : value;
    }
    sending.current = true; setBusy(true); setError(null);
    const controller = new AbortController(); submitController.current = controller;
    try {
      const result = await callWorkspaceTool(baseUrl, accessToken, tool, { ...(sessionId ? { sessao_id: sessionId } : {}), resposta: reply, fonte_informada: source, dados_fornecidos: explicitFields }, controller.signal);
      if (!controller.signal.aborted) { setData(result); if (typeof result.sessao_id === "string") setSessionId(result.sessao_id); setReply(""); }
    } catch {
      if (!controller.signal.aborted) setError("Não foi possível confirmar o registro. A resposta pode ter sido recebida; evite reenviá-la até verificar o estado do diálogo.");
    } finally { sending.current = false; if (!controller.signal.aborted) setBusy(false); }
  }
  const question = data?.next_question ?? data?.proxima_pergunta;
  const readErrors = data?.erros_leitura && typeof data.erros_leitura === "object" ? Object.values(data.erros_leitura).some(Boolean) : false;
  const primary = data?.comunicado ?? data?.mensagem;
  return <section className="workspace-panel" aria-labelledby={`tool-${tool}`}>
    <div className="flex flex-wrap items-start justify-between gap-4"><div><h2 id={`tool-${tool}`} className="text-xl font-semibold">{title}</h2><p className="mt-2 max-w-prose text-sm leading-6 text-slate-600">{description}</p></div>{!dialogue && <button type="button" disabled={busy} onClick={() => setRevision(current => current + 1)} className="workspace-secondary">Atualizar consulta</button>}</div>
    <div className="mt-5" aria-live="polite">{busy ? <p className="text-sm text-slate-600">Consultando o ELO…</p> : error ? <p role="alert" className="text-sm text-red-700">{error}</p> : data ? <>
      {readErrors && <p role="alert" className="mb-4 text-sm text-red-700">Parte das fontes não pôde ser consultada. Este retorno não comprova ausência de dados.</p>}
      {typeof primary === "string" && <p className="whitespace-pre-wrap text-sm leading-7">{primary}</p>}
      {typeof question === "string" && question && <div className="my-4 rounded-xl bg-slate-100 p-4"><h3 className="font-semibold">Próxima informação necessária</h3><p className="mt-2 text-sm leading-6">{question}</p></div>}
      {Array.isArray(data.requests) && <DataValue value={data.requests} />}
      {Array.isArray(data.pontos_melhorar_inserir) && <DataValue value={data.pontos_melhorar_inserir} />}
      {data.resumo != null && <DataValue value={data.resumo} />}
      {Array.isArray(data.fator_rows) && <DataValue value={data.fator_rows} />}
      {Array.isArray(data.demanda_humana_projetada) && <DataValue value={data.demanda_humana_projetada} />}
      {tool === "elo_status" && <div className="space-y-3 text-sm"><p>Identidade: {String(data.display_name ?? "Não informada")}</p><p>Acesso retornado pelo ELO:</p><DataValue value={data.roles} /></div>}
      <details className="mt-5 text-sm"><summary className="cursor-pointer font-medium">Ver dados e regras retornados</summary><div className="mt-4"><DataValue value={data} /></div></details>
    </> : null}</div>
    {dialogue && <form onSubmit={submit} className="mt-6 space-y-4">
      <label className="block text-sm font-medium">Sua resposta<textarea value={reply} onChange={event => setReply(event.target.value)} maxLength={4000} rows={3} disabled={busy} className="workspace-input mt-2" /></label>
      <label className="block text-sm font-medium">Fonte informada<input value={source} onChange={event => setSource(event.target.value)} disabled={busy} className="workspace-input mt-2" /></label>
      {missing.map(field => <label key={field} className="block text-sm font-medium">{label(field)}<input value={fields[field] ?? ""} onChange={event => setFields(current => ({ ...current, [field]: event.target.value }))} disabled={busy} className="workspace-input mt-2" /></label>)}
      <p className="text-sm leading-6 text-slate-600">A resposta é registrada no diálogo do ELO. A gravação nas tabelas operacionais e a liberação de decisões seguem as permissões e validações correspondentes.</p>
      <button type="submit" disabled={busy || (!reply.trim() && !source.trim() && !Object.values(fields).some(value => value.trim()))} className="workspace-primary">{busy ? "Enviando…" : "Registrar resposta no ELO"}</button>
      
    </form>}
  </section>;
}
