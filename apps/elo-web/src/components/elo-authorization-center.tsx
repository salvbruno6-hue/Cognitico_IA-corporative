"use client";

import { useState } from "react";
import { callELOAuthorization } from "@/auth/eloAuthorization";

type Check = { status: "idle" | "loading" | "verified" | "denied"; message: string; identity?: string; session?: string };

export function EloAuthorizationCenter({ accessToken }: { accessToken: string }) {
  const [check, setCheck] = useState<Check>({ status: "idle", message: "A verificação de permissões é realizada pelo ELO Authorization." });
  async function verify() {
    setCheck({ status: "loading", message: "Consultando a autoridade canônica..." });
    try {
      const result = await callELOAuthorization(accessToken, "check_authorization_state");
      setCheck({ status: "verified", message: "Consulta respondida pela autoridade ELO. A sessão não constitui autorização para merge.", identity: result.identity_id, session: result.session_id });
    } catch {
      setCheck({ status: "denied", message: "Não foi possível comprovar a autorização. Nenhuma operação privilegiada está disponível." });
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
      <p className="mt-2 text-sm text-slate-500">Consulta somente leitura ao endpoint existente. Não emite grants e não modifica permissões.</p>
      <button type="button" onClick={() => void verify()} disabled={check.status === "loading"} className="mt-4 rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">Verificar autorização ELO</button>
      <p role="status" aria-live="polite" className="mt-4 text-sm text-slate-600">{check.message}</p>
    </article>
    <article className="rounded-2xl border border-amber-200 bg-[var(--elo-panel)] p-6">
      <h3 className="font-semibold">Solicitações e notificações</h3>
      <p className="mt-2 text-sm text-slate-500">Nenhuma fila é exibida até que a fonte canônica de solicitações e as regras de acesso sejam validadas. Não confundir ausência de dados com ausência de pendências.</p>
      <p className="mt-3 text-xs font-medium text-amber-700">Aprovar e rejeitar indisponíveis até integração governada, testes e Evolution Gate.</p>
    </article>
  </section>;
}
