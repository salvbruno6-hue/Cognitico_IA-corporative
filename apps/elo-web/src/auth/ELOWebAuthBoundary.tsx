"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { type Session } from "@supabase/supabase-js";
import { createClient } from "@/lib/supabase/client";
import { createOAuthFlow } from "@/auth/oauthFlow";
import { EloDashboard } from "@/components/elo-dashboard";
import { callELOAuthorization } from "@/auth/eloAuthorization";

function getSupabaseClient() {
  try { return createClient(); } catch { return null; }
}

function friendlyAuthError(message: string): string {
  const normalized = message.toLowerCase();
  if (normalized.includes("provider is not enabled") || (normalized.includes("unsupported provider") && normalized.includes("not enabled"))) {
    return "O login Google do ELO não está habilitado no Supabase Auth.";
  }
  return message;
}

function GoogleIcon() {
  return <span aria-hidden="true" className="text-base font-bold">G</span>;
}

export function ELOWebAuthBoundary() {
  const [session, setSession] = useState<Session | null>(null);
  const [authorized, setAuthorized] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [signingIn, setSigningIn] = useState(false);
  const [workspaceOpen, setWorkspaceOpen] = useState(false);
  const autoStartConsumed = useRef(false);
  const oauthFlow = useRef<ReturnType<typeof createOAuthFlow> | null>(null);

  useEffect(() => {
    let active = true;
    const supabase = getSupabaseClient();
    if (!supabase) {
      setError("ELO Web não está configurado: variáveis públicas do Supabase não foram definidas no ambiente.");
      setLoading(false);
      return () => { active = false; };
    }

    const { data: authState } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      if (!active) return;
      setSession(nextSession);
      if (!nextSession) {
        setAuthorized(false);
        setWorkspaceOpen(false);
      }
    });

    void supabase.auth.getSession().then(async ({ data, error: sessionError }) => {
      if (!active) return;
      if (sessionError) {
        setError(friendlyAuthError(sessionError.message));
        setLoading(false);
        return;
      }
      if (!data.session) {
        setSession(null);
        setAuthorized(false);
        setWorkspaceOpen(false);
        setLoading(false);
        return;
      }

      setSession(data.session);
      try {
        await callELOAuthorization(data.session.access_token, "establish_session");
        if (!active) return;
        setError(null);
        setAuthorized(true);
        setWorkspaceOpen(false);
      } catch (authorizationError) {
        if (!active) return;
        setAuthorized(false);
        setError(authorizationError instanceof Error ? friendlyAuthError(authorizationError.message) : "Não foi possível autorizar o ELO.");
      } finally {
        if (active) setLoading(false);
      }
    });

    return () => {
      active = false;
      authState.subscription.unsubscribe();
    };
  }, []);

  const beginGoogleOAuth = useCallback(async () => {
    if (signingIn) return;
    setError(null);
    setSigningIn(true);
    const supabase = getSupabaseClient();
    if (!supabase) {
      setError("Cliente de autenticação do ELO não está configurado.");
      setSigningIn(false);
      return;
    }
    try {
      oauthFlow.current ??= createOAuthFlow(supabase.auth);
      await oauthFlow.current.start(window.location.origin);
    } catch (authError) {
      setError(friendlyAuthError(authError instanceof Error ? authError.message : "Falha no login Google."));
    } finally { setSigningIn(false); }
  }, [signingIn]);

  useEffect(() => {
    if (loading || signingIn || autoStartConsumed.current) return;
    const url = new URL(window.location.href);
    if (url.searchParams.get("start") !== "google") return;

    autoStartConsumed.current = true;
    url.searchParams.delete("start");
    window.history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);

    if (!session && !error) void beginGoogleOAuth();
  }, [loading, session, signingIn, error, beginGoogleOAuth]);

  async function signOut() {
    setError(null);
    const supabase = getSupabaseClient();
    if (!supabase) return;
    try {
      if (session) await callELOAuthorization(session.access_token, "revoke_session");
      const { error: signOutError } = await supabase.auth.signOut();
      if (signOutError) throw signOutError;
      setAuthorized(false);
      setWorkspaceOpen(false);
      setSession(null);
      window.location.assign("/");
    } catch (signOutError) {
      setError(signOutError instanceof Error ? friendlyAuthError(signOutError.message) : "Não foi possível encerrar a sessão do ELO.");
    }
  }

  if (loading) {
    return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] text-[var(--elo-ink)]"><div className="text-sm text-slate-500">Inicializando ELO Cognitivo…</div></main>;
  }

  if (!session || !authorized) {
    return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]"><section className="w-full max-w-md rounded-[2rem] border border-slate-200 bg-white p-8 text-center shadow-sm"><div className="mx-auto grid size-14 place-items-center rounded-2xl bg-slate-950 text-xl font-bold text-white">E</div><div className="mt-5 text-[10px] font-bold uppercase tracking-[.22em] text-slate-400">ELO · Inteligência corporativa</div><h1 className="mt-2 text-2xl font-semibold tracking-tight">Acesso ao ELO</h1><p className="mt-3 text-sm leading-6 text-slate-500">Entre com sua conta Google. Depois, o ELO Authorization valida sua identidade e permissões.</p>{error && <div className="mt-4 rounded-xl border border-red-100 bg-red-50 p-3 text-left text-sm text-red-700" role="alert"><div className="font-semibold">Não foi possível continuar</div><div className="mt-1 leading-5">{error}</div></div>}<button type="button" onClick={() => session ? window.location.reload() : void beginGoogleOAuth()} disabled={signingIn} className="mt-6 flex w-full items-center justify-center gap-3 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-800 shadow-sm hover:bg-slate-50 disabled:cursor-wait disabled:opacity-60"><GoogleIcon />{signingIn ? "Abrindo Google…" : session ? "Tentar autorização ELO novamente" : "Continuar com Google"}</button></section></main>;
  }

  if (!workspaceOpen) {
    return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]"><section className="w-full max-w-xl rounded-[2rem] border border-slate-200 bg-white p-8 text-center shadow-sm"><div className="mx-auto grid size-14 place-items-center rounded-2xl bg-slate-950 text-xl font-bold text-white">E</div><div className="mt-5 text-[10px] font-bold uppercase tracking-[.22em] text-slate-400">WORKSPACE OPERACIONAL</div><h1 className="mt-2 text-2xl font-semibold tracking-tight">Acesso autorizado</h1><p className="mt-3 text-sm leading-6 text-slate-500">Autenticação Google, sessão Supabase e autorização ELO concluídas.</p><button type="button" onClick={() => setWorkspaceOpen(true)} className="mt-6 w-full rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-slate-800">Abrir Workspace Operacional</button></section></main>;
  }

  return <EloDashboard displayName={session.user.user_metadata?.full_name ?? session.user.email} accessToken={session.access_token} onSignOut={() => void signOut()} />;
}
