"use client";

import { useEffect, useState } from "react";
import { createClient, type Session } from "@supabase/supabase-js";
import { EloDashboard } from "@/components/elo-dashboard";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;

if (!supabaseUrl || !supabaseAnonKey) throw new Error("ELO Web Auth: configure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY (or NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY).");

export const supabase = createClient(supabaseUrl, supabaseAnonKey, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } });

async function establishELOAuthorizationSession() {
  const { error: identityError } = await supabase.rpc("elo_bind_authenticated_identity");
  if (identityError) throw identityError;
  const { data: sessionId, error: sessionError } = await supabase.rpc("elo_establish_authenticated_session");
  if (sessionError) throw sessionError;
  if (!sessionId) throw new Error("ELO authorization session was not established.");
  return sessionId as string;
}

async function revokeELOAuthorizationSession() {
  const { error } = await supabase.rpc("elo_revoke_authenticated_session");
  if (error) throw error;
}

function getELOLoginUrl() { return process.env.NEXT_PUBLIC_ELO_LOGIN_URL?.trim() || "/"; }

export function ELOWebAuthBoundary() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    void supabase.auth.getSession().then(async ({ data, error: sessionError }) => {
      if (!active) return;
      if (sessionError) { setError(sessionError.message); setLoading(false); return; }
      setSession(data.session);
      if (!data.session) { setAuthorized(false); setLoading(false); return; }
      try { await establishELOAuthorizationSession(); if (active) setAuthorized(true); }
      catch (authorizationError) { if (active) { setAuthorized(false); setError(authorizationError instanceof Error ? authorizationError.message : "Não foi possível estabelecer a sessão de autorização do ELO."); } }
      finally { if (active) setLoading(false); }
    });
    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => { if (!active) return; setSession(nextSession); if (!nextSession) setAuthorized(false); });
    return () => { active = false; data.subscription.unsubscribe(); };
  }, []);

  async function signOut() {
    setError(null);
    try { if (session) await revokeELOAuthorizationSession(); }
    catch (revokeError) { setError(revokeError instanceof Error ? revokeError.message : "Não foi possível revogar a sessão do ELO."); return; }
    const { error: signOutError } = await supabase.auth.signOut();
    if (signOutError) { setError(signOutError.message); return; }
    setAuthorized(false); setSession(null); window.location.assign(getELOLoginUrl());
  }

  if (loading) return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] text-[var(--elo-ink)]">Verificando sessão…</main>;
  if (!session || !authorized) return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]"><section className="w-full max-w-lg rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-8 text-center shadow-sm"><p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">ELO · Acesso protegido</p><h1 className="mt-3 text-3xl font-semibold tracking-tight">Entre pela página oficial do ELO</h1><p className="mt-3 text-sm leading-6 text-slate-500">O ELO Web reutiliza a identidade Google/Supabase e a sessão de autorização já estabelecidas pelo ELO. Não existe cadastro ou login paralelo nesta aplicação.</p>{error && <p className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-700" role="alert">{error}</p>}<a href={getELOLoginUrl()} className="mt-6 inline-flex rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">Continuar para o login do ELO</a></section></main>;
  return <EloDashboard onSignOut={() => void signOut()} />;
}
