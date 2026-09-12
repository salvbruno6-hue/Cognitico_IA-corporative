"use client";

import { useEffect, useState } from "react";
import { createClient, type Session } from "@supabase/supabase-js";
import { GovernedHermesTerminal } from "@/components/governed-hermes-terminal";
import { callELOAuthorization } from "@/auth/eloAuthorization";
import { getCanonicalSupabaseConfig } from "@/lib/supabase/config";

function getSupabaseClient() {
  try {
    const { url, key } = getCanonicalSupabaseConfig();
    return createClient(url, key, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } });
  } catch {
    return null;
  }
}

export default function HermesTerminalPage() {
  const [session, setSession] = useState<Session | null>(null);
  const [authorized, setAuthorized] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const supabase = getSupabaseClient();
    if (!supabase) {
      setError("ELO Web está apontando para um projeto Supabase diferente do projeto canônico.");
      setLoading(false);
      return () => { active = false; };
    }

    void supabase.auth.getSession().then(async ({ data, error: sessionError }) => {
      if (!active) return;
      if (sessionError) {
        setError(sessionError.message);
        setLoading(false);
        return;
      }
      setSession(data.session);
      if (!data.session) {
        setLoading(false);
        return;
      }
      try {
        await callELOAuthorization(data.session.access_token, "establish_session");
        if (active) setAuthorized(true);
      } catch (authorizationError) {
        if (active) setError(authorizationError instanceof Error ? authorizationError.message : "Não foi possível autorizar o terminal ELO.");
      } finally {
        if (active) setLoading(false);
      }
    });

    return () => { active = false; };
  }, []);

  if (loading) return <main className="grid min-h-screen place-items-center bg-slate-950 text-slate-200">Verificando sessão ELO…</main>;

  if (!session || !authorized) {
    return (
      <main className="grid min-h-screen place-items-center bg-slate-950 p-6 text-slate-100">
        <section className="w-full max-w-lg rounded-2xl border border-white/10 bg-white/[0.04] p-8 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">ELO · Terminal Governado</p>
          <h1 className="mt-3 text-2xl font-semibold">Acesso protegido</h1>
          <p className="mt-3 text-sm leading-6 text-slate-400">O terminal Hermes reutiliza a mesma identidade Google/Supabase e a mesma sessão de autorização do ELO. Abra o ELO principal e autentique-se antes de usar o terminal.</p>
          {error && <p className="mt-4 rounded-xl bg-rose-500/10 p-3 text-sm text-rose-300" role="alert">{error}</p>}
          <a href="/" className="mt-6 inline-flex rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950">Abrir ELO</a>
        </section>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 p-4 text-slate-100 sm:p-6 lg:p-10">
      <div className="mx-auto max-w-7xl">
        <div className="mb-5 flex items-center justify-between gap-4">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">ELO / Cognitivo / Symbiont / Hermes</div>
            <h1 className="mt-1 text-2xl font-semibold">Terminal de entrada governado</h1>
          </div>
          <a href="/" className="rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-300 hover:bg-white/5">Voltar ao ELO</a>
        </div>
        <GovernedHermesTerminal accessToken={session.access_token} />
      </div>
    </main>
  );
}
