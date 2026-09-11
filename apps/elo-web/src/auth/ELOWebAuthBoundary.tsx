"use client";

import { useEffect, useState } from "react";
import { createClient, type Session, type SupabaseClient } from "@supabase/supabase-js";
import { EloDashboard } from "@/components/elo-dashboard";

function getSupabaseClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)?.trim();
  if (!url || !key) return null;
  return createClient(url, key, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
  });
}

async function establishELOAuthorizationSession(supabase: SupabaseClient<any>) {
  const { error: identityError } = await supabase.rpc("elo_bind_authenticated_identity");
  if (identityError) throw identityError;

  const { data: sessionId, error: sessionError } = await supabase.rpc("elo_establish_authenticated_session");
  if (sessionError) throw sessionError;
  if (!sessionId) throw new Error("ELO authorization session was not established.");
  return sessionId as string;
}

async function revokeELOAuthorizationSession(supabase: SupabaseClient<any>) {
  const { error } = await supabase.rpc("elo_revoke_authenticated_session");
  if (error) throw error;
}

function getELOLoginUrl() {
  return process.env.NEXT_PUBLIC_ELO_LOGIN_URL?.trim() || "/";
}

export function ELOWebAuthBoundary() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const supabase = getSupabaseClient();

    if (!supabase) {
      setError("ELO Web não está configurado: variáveis públicas do Supabase não foram definidas no ambiente.");
      setLoading(false);
      return () => {
        active = false;
      };
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
        setAuthorized(false);
        setLoading(false);
        return;
      }

      try {
        await establishELOAuthorizationSession(supabase);
        if (active) setAuthorized(true);
      } catch (authorizationError) {
        if (active) {
          setAuthorized(false);
          setError(
            authorizationError instanceof Error
              ? authorizationError.message
              : "Não foi possível estabelecer a sessão de autorização do ELO.",
          );
        }
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

  async function signOut() {
    setError(null);
    const supabase = getSupabaseClient();
    if (!supabase) {
      setError("Cliente de autenticação do ELO não está configurado.");
      return;
    }

    try {
      if (session) await revokeELOAuthorizationSession(supabase);
    } catch (revokeError) {
      setError(
        revokeError instanceof Error
          ? revokeError.message
          : "Não foi possível revogar a sessão do ELO.",
      );
      return;
    }

    const { error: signOutError } = await supabase.auth.signOut();
    if (signOutError) {
      setError(signOutError.message);
      return;
    }

    setAuthorized(false);
    setSession(null);
    window.location.assign(getELOLoginUrl());
  }

  if (loading) {
    return (
      <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] text-[var(--elo-ink)]">
        Verificando sessão…
      </main>
    );
  }

  if (!session || !authorized) {
    return (
      <main className="grid min-h-screen place-items-center bg-[var(--elo-bg)] p-6 text-[var(--elo-ink)]">
        <section className="w-full max-w-lg rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-8 text-center shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">ELO · Acesso protegido</p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight">Entre pela página oficial do ELO</h1>
          <p className="mt-3 text-sm leading-6 text-slate-500">
            O ELO Web reutiliza a identidade Google/Supabase e a sessão de autorização já estabelecidas pelo ELO.
            Não existe cadastro ou login paralelo nesta aplicação.
          </p>
          {error && (
            <p className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-700" role="alert">
              {error}
            </p>
          )}
          <a
            href={getELOLoginUrl()}
            className="mt-6 inline-flex rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white"
          >
            Continuar para o login do ELO
          </a>
        </section>
      </main>
    );
  }

  return <EloDashboard accessToken={session.access_token} onSignOut={() => void signOut()} />;
}
