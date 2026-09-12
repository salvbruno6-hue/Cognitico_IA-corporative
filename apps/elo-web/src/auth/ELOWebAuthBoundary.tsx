"use client";

import { useEffect, useState } from "react";
import { createClient, type Session, type SupabaseClient } from "@supabase/supabase-js";
import { EloWebCommandCenter } from "@/components/elo-web-command-center";

type AuthClient = SupabaseClient<any>;
type BridgeResponse = { ok?: boolean; reason?: string; message?: string };

function getSupabaseClient(): AuthClient | null {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)?.trim();
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } });
}

function bridgeError(payload: unknown, fallback: string) {
  if (typeof payload === "object" && payload !== null && "reason" in payload && typeof (payload as BridgeResponse).reason === "string") {
    return (payload as BridgeResponse).reason;
  }
  if (typeof payload === "object" && payload !== null && "message" in payload && typeof (payload as BridgeResponse).message === "string") {
    return (payload as BridgeResponse).message;
  }
  return fallback;
}

async function callSessionBridge(supabase: AuthClient, operation: "establish" | "revoke") {
  const requestId = crypto.randomUUID();
  const { data, error } = await supabase.functions.invoke<BridgeResponse>("elo-session-bridge", {
    headers: { "x-elo-request-id": requestId },
    body: { operation },
  });
  if (error) throw new Error(error.message || `Falha no ELO Session Bridge (${operation}).`);
  if (!data?.ok) throw new Error(bridgeError(data, `ELO Session Bridge negou a operação ${operation}.`));
  return data;
}

async function establishAuthorization(supabase: AuthClient) {
  await callSessionBridge(supabase, "establish");
}

async function revokeAuthorization(supabase: AuthClient) {
  await callSessionBridge(supabase, "revoke");
}

export function ELOWebAuthBoundary() {
  const [session, setSession] = useState<Session | null>(null);
  const [authorized, setAuthorized] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [signingIn, setSigningIn] = useState(false);

  useEffect(() => {
    let active = true;
    const supabase = getSupabaseClient();
    if (!supabase) { setError("ELO Web não está configurado: variáveis públicas do Supabase não foram definidas no ambiente."); setLoading(false); return () => { active = false; }; }

    void supabase.auth.getSession().then(async ({ data, error: sessionError }) => {
      if (!active) return;
      if (sessionError) { setError(sessionError.message); setLoading(false); return; }
      setSession(data.session);
      if (!data.session) { setLoading(false); return; }
      try { await establishAuthorization(supabase); if (active) setAuthorized(true); }
      catch (authorizationError) { if (active) setError(authorizationError instanceof Error ? authorizationError.message : "Não foi possível autorizar o ELO."); }
      finally { if (active) setLoading(false); }
    });

    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => { if (!active) return; setSession(nextSession); if (!nextSession) setAuthorized(false); });
    return () => { active = false; data.subscription.unsubscribe(); };
  }, []);

  async function signInWithGoogle() {
    setError(null); setSigningIn(true);
    const supabase = getSupabaseClient();
    if (!supabase) { setError("Cliente de autenticação do ELO não está configurado."); setSigningIn(false); return; }
    const { error: authError } = await supabase.auth.signInWithOAuth({ provider: "google", options: { redirectTo: `${window.location.origin}/auth/callback` } });
    if (authError) { setError(authError.message); setSigningIn(false); }
  }

  async function signOut() {
    setError(null);
    const supabase = getSupabaseClient();
    if (!supabase) { setError("Cliente de autenticação do ELO não está configurado."); return; }
    try { if (session) await revokeAuthorization(supabase); }
    catch (revokeError) { setError(revokeError instanceof Error ? revokeError.message : "Não foi possível revogar a sessão do ELO."); return; }
    const { error: signOutError } = await supabase.auth.signOut();
    if (signOutError) { setError(signOutError.message); return; }
    setAuthorized(false); setSession(null); window.location.assign("/");
  }

  if (loading) return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] text-[var(--elo-ink)]"><div className="text-sm text-slate-500">Inicializando ELO Cognitivo…</div></main>;

  if (!session || !authorized) return (
    <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]">
      <section className="w-full max-w-md rounded-[2rem] border border-slate-200 bg-white p-8 text-center shadow-sm">
        <div className="mx-auto grid size-14 place-items-center rounded-2xl bg-slate-950 text-xl font-bold text-white">E</div>
        <div className="mt-5 text-[10px] font-bold uppercase tracking-[.22em] text-slate-400">ELO · Inteligência corporativa</div>
        <h1 className="mt-2 text-2xl font-semibold tracking-tight">Acesso protegido</h1>
        <p className="mt-3 text-sm leading-6 text-slate-500">Use a identidade Google/Supabase do ELO. Não existe autenticação paralela nesta aplicação.</p>
        {error && <p className="mt-4 rounded-xl bg-red-50 p-3 text-left text-sm text-red-700" role="alert">{error}</p>}
        <button type="button" onClick={() => void signInWithGoogle()} disabled={signingIn} className="mt-6 w-full rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white disabled:cursor-wait disabled:opacity-60">{signingIn ? "Abrindo Google…" : "Continuar com Google"}</button>
      </section>
    </main>
  );

  return <EloWebCommandCenter accessToken={session.access_token} onSignOut={() => void signOut()} />;
}
