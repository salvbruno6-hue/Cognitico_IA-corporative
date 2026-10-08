"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { createOAuthFlow } from "@/auth/oauthFlow";

let flow: ReturnType<typeof createOAuthFlow> | undefined;

export default function AuthCallbackPage() {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    try {
      flow ??= createOAuthFlow(createClient().auth);
      void flow.complete(window.location.href, () => {
        window.history.replaceState({}, "", window.location.pathname);
      }).then(() => {
        if (active) window.location.replace("/");
      }).catch(callbackError => {
        if (active) setError(callbackError instanceof Error ? callbackError.message : "Falha no retorno Google.");
      });
    } catch (configurationError) {
      setError(configurationError instanceof Error ? configurationError.message : "Cliente Supabase indisponível.");
    }

    return () => { active = false; };
  }, []);

  return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]"><section className="w-full max-w-lg rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-8 text-center shadow-sm">{error ? <><p className="text-xs font-semibold uppercase tracking-[0.18em] text-red-500">ELO · Falha de autenticação</p><p className="mt-4 text-sm text-red-700">{error}</p><a href="/" className="mt-6 inline-flex rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">Voltar ao ELO</a></> : <><p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">ELO · Autenticação</p><h1 className="mt-3 text-2xl font-semibold tracking-tight">Validando sua sessão…</h1><p className="mt-3 text-sm text-slate-500">Concluindo o acesso seguro do ELO.</p></>}</section></main>;
}
