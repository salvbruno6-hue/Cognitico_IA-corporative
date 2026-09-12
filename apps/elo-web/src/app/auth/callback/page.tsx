"use client";

import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

export default function AuthCallbackPage() {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
    const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)?.trim();

    if (!url || !key) {
      setError("ELO Web não está configurado: variáveis públicas do Supabase não foram definidas no ambiente.");
      return;
    }

    const supabase = createClient(url, key, {
      auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
    });

    void supabase.auth.getSession().then(({ error: sessionError }) => {
      if (sessionError) {
        setError(sessionError.message);
        return;
      }
      window.location.replace("/");
    });
  }, []);

  return (
    <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]">
      <section className="w-full max-w-lg rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-8 text-center shadow-sm">
        {error ? (
          <>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-red-500">ELO · Falha de autenticação</p>
            <p className="mt-4 text-sm text-red-700">{error}</p>
            <a href="/" className="mt-6 inline-flex rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">
              Voltar ao ELO
            </a>
          </>
        ) : (
          <>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">ELO · Autenticação</p>
            <h1 className="mt-3 text-2xl font-semibold tracking-tight">Validando sua sessão…</h1>
            <p className="mt-3 text-sm text-slate-500">Concluindo o acesso seguro do ELO.</p>
          </>
        )}
      </section>
    </main>
  );
}
