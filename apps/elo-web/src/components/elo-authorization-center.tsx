"use client";

import { useRef, useState } from "react";
import { callELOAuthorization } from "@/auth/eloAuthorization";
import { CANONICAL_REPOSITORY, mergeGrantResource } from "@/lib/authorization-resource";

type Check = { status: "idle" | "loading" | "verified" | "denied"; message: string; identity?: string; session?: string };

export function EloAuthorizationCenter({ accessToken }: { accessToken: string }) {
  const [check, setCheck] = useState<Check>({ status: "idle", message: "A verificação de permissões é realizada pelo ELO Authorization." });
  const [pr, setPr] = useState("");
  const [sha, setSha] = useState("");
  const requestVersion = useRef(0);
  async function verify() {
    const version = ++requestVersion.current;
    const resourceId = mergeGrantResource(pr, sha);
    if (!resourceId) {
      setCheck({ status: "denied", message: "Informe número da PR e SHA completo (40 caracteres) para consulta de grant específico." });
      return;
    }
    setCheck({ status: "loading", message: "Consultando a autoridade canônica..." });
    try {
      const result = await callELOAuthorization(accessToken, "check_authorization_state", { authorization_state: "elo-merge-authorized", operation: "merge", repository: CANONICAL_REPOSITORY, resource_id: resourceId });
      if (version !== requestVersion.current) return;
      setCheck({ status: "verified", message: `Grant de merge válido para PR #${pr} no SHA informado, conforme elo-authz. Outros gates ainda são obrigatórios.`, identity: result.identity_id, session: result.session_id });
    } catch {
      if (version !== requestVersion.current) return;
      setCheck({ status: "denied", message: "Grant não comprovado para PR/SHA informado ou consulta indisponível. Nenhuma operação privilegiada está disponível." });
    }
  }
  return <section aria-labelledby="elo-authz-title" className="space-y-5">
    <header className="rounded-3xl border border-slate-200 bg-[var(--elo-panel)] p-6 shadow-sm">
      <div className="text-xs font-bold uppercase tracking-[.2em] text-indigo-500">ELO · Governança</div>
      <h2 id="elo-authz-title" className="mt-2 text-3xl font-semibold">Central de Autorizações</h2>
      <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">Identidade, solicitações e decisões sob controle do ELO Authorization. Autenticação Google não equivale a permissão de execução, commit ou merge.</p>
    </header>
    <div className="grid gap-4 sm:grid-cols-3">
      {["Aguardando decisão", "Autorizadas", "Negadas ou bloqueadas"].map(label => <article key={label} className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5"><p className="text-xs font-medium text-slate-500">{label}</p><div className="mt-3 text-xl font-semibold" aria-label="Contagem indisponível">—</div><p className="mt-2 text-xs text-slate-500">Fonte de solicitações ainda não conectada</p></article>)}
    </div>
    <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-6">
      <h3 className="font-semibold">Verificação de identidade e política</h3>
      <p className="mt-2 text-sm text-slate-500">Consulta de grant de merge vinculada a PR e SHA completos. Não emite grants nem modifica permissões.</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2"><label className="text-sm">Número da PR<input aria-label="Número da PR" value={pr} onChange={e => { requestVersion.current++; setPr(e.target.value); setCheck({ status: "idle", message: "Consulta necessária para os dados atuais." }); }} inputMode="numeric" placeholder="1237" className="mt-1 w-full rounded-lg border border-slate-300 bg-transparent p-2" /></label><label className="text-sm">SHA completo da PR<input aria-label="SHA completo" value={sha} onChange={e => { requestVersion.current++; setSha(e.target.value); setCheck({ status: "idle", message: "Consulta necessária para os dados atuais." }); }} placeholder="40 caracteres hexadecimais" className="mt-1 w-full rounded-lg border border-slate-300 bg-transparent p-2 font-mono text-xs" /></label></div>
      <button type="button" onClick={() => void verify()} disabled={check.status === "loading"} className="mt-4 rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">Consultar grant de merge</button>
      <p role="status" aria-live="polite" className="mt-4 text-sm text-slate-600">{check.message}</p>
    </article>
    <article className="rounded-2xl border border-amber-200 bg-[var(--elo-panel)] p-6">
      <h3 className="font-semibold">Solicitações e notificações</h3>
      <p className="mt-2 text-sm text-slate-500">Nenhuma fila é exibida até que a fonte canônica de solicitações e as regras de acesso sejam validadas. Não confundir ausência de dados com ausência de pendências.</p>
      <p className="mt-3 text-xs font-medium text-amber-700">Aprovar e rejeitar indisponíveis até integração governada, testes e Evolution Gate.</p>
    </article>
  </section>;
}
