"use client";

import { useEffect, useState } from "react";
import { createClient, type Session, type SupabaseClient } from "@supabase/supabase-js";
import { EloWebOperationalPortal } from "@/components/elo-web-operational-portal";
import { callELOAuthorization } from "@/auth/eloAuthorization";

type AuthClient = SupabaseClient<any>;

function getSupabaseClient(): AuthClient | null {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)?.trim();
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } });
}

function GoogleIcon() {
  return <svg aria-hidden="true" viewBox="0 0 24 24" className="size-5"><path fill="#4285F4" d="M21.35 12.23c0-.72-.06-1.25-.2-1.8H12v3.4h5.38a4.6 4.6 0 0 1-2 3.02v2.5h3.24c1.9-1.75 2.73-4.33 2.73-7.12Z"/><path fill="#34A853" d="M12 21.99c2.7 0 4.97-.89 6.62-2.42l-3.24-2.5c-.9.6-2.05.96-3.38.96-2.6 0-4.8-1.76-5.59-4.13H3.06v2.58A10 10 0 0 0 12 21.99Z"/><path fill="#FBBC05" d="M6.41 13.9A5.99 5.99 0 0 1 6.1 12c0-.66.11-1.3.31-1.9V7.52H3.06A10 10 0 0 0 2 12c0 1.62.39 3.14 1.06 4.48l3.35-2.58Z"/><path fill="#EA4335" d="M12 5.97c1.48 0 2.8.51 3.84 1.51l2.88-2.88C16.96 2.9 14.7 2 12 2a10 10 0 0 0-8.94 5.52L6.41 10.1C7.2 7.73 9.4 5.97 12 5.97Z"/></svg>;
}

function friendlyAuthError(message: string): string {
  const normalized = message.toLowerCase();
  if (normalized.includes("unsupported provider") && normalized.includes("not enabled")) {
    return "O login Google ainda não está habilitado no provedor de autenticação do ELO. A configuração precisa ser concluída no Supabase Auth antes de uma nova tentativa.";
  }
  if (normalized.includes("provider is not enabled")) {
    return "O provedor Google do ELO está desabilitado no Supabase Auth.";
  }
  return message;
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
    if (!supabase) {
      setError("ELO Web não está configurado: variáveis públicas do Supabase não foram definidas no ambiente.");
      setLoading(false);
      return () => { active = false; };
    }

    void supabase.auth.getSession().then(async ({ data, error: sessionError }) => {
      if (!active) return;
      if (sessionError) {
        setError(friendlyAuthError(sessionError.message));
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
        if (active) {
          setError(null);
          setAuthorized(true);
        }
      } catch (authorizationError) {
        if (active) setError(authorizationError instanceof Error ? friendlyAuthError(authorizationError.message) : "Não foi possível autorizar o ELO.");
      } finally {
        if (active) setLoading(false);
      }
    });

    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      if (!active) return;
      setSession(nextSession);
      if (!nextSession) setAuthorized(false);
    });

    return () => {
      active = false;
      data.subscription.unsubscribe();
    };
  }, []);

  async function signInWithGoogle() {
    setError(null);
    setSigningIn(true);
    const supabase = getSupabaseClient();
    if (!supabase) {
      setError("Cliente de autenticação do ELO não está configurado.");
      setSigningIn(false);
      return;
    }

    const { error: authError } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    });

    if (authError) {
      setError(friendlyAuthError(authError.message));
      setSigningIn(false);
    }
  }

  async function signOut() {
    setError(null);
    const supabase = getSupabaseClient();
    if (!supabase) {
      setError("Cliente de autenticação do ELO não está configurado.");
      return;
    }
    try {
      if (session) await callELOAuthorization(session.access_token, "revoke_session");
    } catch (revokeError) {
      setError(revokeError instanceof Error ? friendlyAuthError(revokeError.message) : "Não foi possível revogar a sessão do ELO.");
      return;
    }
    const { error: signOutError } = await supabase.auth.signOut();
    if (signOutError) {
      setError(friendlyAuthError(signOutError.message));
      return;
    }
    setAuthorized(false);
    setSession(null);
    window.location.assign("/");
  }

  if (loading) {
    return <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] text-[var(--elo-ink)]"><div className="text-sm text-slate-500">Inicializando ELO Cognitivo…</div></main>;
  }

  if (!session || !authorized) {
    return (
      <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]">
        <section className="w-full max-w-md rounded-[2rem] border border-slate-200 bg-white p-8 text-center shadow-sm">
          <div className="mx-auto grid size-14 place-items-center rounded-2xl bg-slate-950 text-xl font-bold text-white">E</div>
          <div className="mt-5 text-[10px] font-bold uppercase tracking-[.22em] text-slate-400">ELO · Inteligência corporativa</div>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight">Acesso ao ELO</h1>
          <p className="mt-3 text-sm leading-6 text-slate-500">Entre com sua conta Google. O Google confirma sua identidade e, depois, o ELO Authorization verifica se esse e-mail possui acesso cadastrado.</p>

          {error && (
            <div className="mt-4 rounded-xl border border-red-100 bg-red-50 p-3 text-left text-sm text-red-700" role="alert">
              <div className="font-semibold">Não foi possível continuar</div>
              <div className="mt-1 leading-5">{error}</div>
            </div>
          )}

          <button type="button" onClick={() => void signInWithGoogle()} disabled={signingIn} className="mt-6 flex w-full items-center justify-center gap-3 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-800 shadow-sm hover:bg-slate-50 disabled:cursor-wait disabled:opacity-60">
            <GoogleIcon />
            {signingIn ? "Abrindo Google…" : "Continuar com Google"}
          </button>

          <div className="mt-5 grid gap-2 text-left text-[11px] leading-5 text-slate-400">
            <div><span className="font-semibold text-slate-500">1.</span> Google autentica a conta e o e-mail.</div>
            <div><span className="font-semibold text-slate-500">2.</span> Supabase mantém a sessão autenticada.</div>
            <div><span className="font-semibold text-slate-500">3.</span> ELO Authorization valida identidade e permissões.</div>
            <div><span className="font-semibold text-slate-500">4.</span> Usuários autorizados seguem para o Portal Operacional.</div>
          </div>
        </section>
      </main>
    );
  }

  return <EloWebOperationalPortal accessToken={session.access_token} displayName={session.user.user_metadata?.full_name ?? session.user.user_metadata?.name} email={session.user.email} onSignOut={() => void signOut()} />;
}
