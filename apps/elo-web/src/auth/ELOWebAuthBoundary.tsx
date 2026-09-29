"use client";

import { useEffect, useRef, useState } from "react";
import { createClient, type Session, type SupabaseClient } from "@supabase/supabase-js";
import { callELOAuthorization } from "@/auth/eloAuthorization";

type AuthClient = SupabaseClient<any>;

let supabaseClient: AuthClient | null = null;

function getSupabaseClient(): AuthClient | null {
  if (supabaseClient) return supabaseClient;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)?.trim();
  if (!url || !key) return null;

  supabaseClient = createClient(url, key, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true,
    },
  });

  return supabaseClient;
}

function friendlyAuthError(message: string): string {
  const normalized = message.toLowerCase();

  if (normalized.includes("unsupported provider") && normalized.includes("not enabled")) {
    return "O login Google ainda não está habilitado no provedor de autenticação do ELO.";
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
  const [establishing, setEstablishing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [signingIn, setSigningIn] = useState(false);\n  const mountedRef = useRef(true);

  async function establishELOSession(nextSession: Session): Promise<boolean> {
    setEstablishing(true);
    setError(null);

    try {
      await callELOAuthorization(nextSession.access_token, "establish_session");
      setAuthorized(true);
      return true;
    } catch (authorizationError) {
      setAuthorized(false);
      setError(
        authorizationError instanceof Error
          ? friendlyAuthError(authorizationError.message)
          : "Não foi possível estabelecer a sessão do ELO.",
      );
      return false;
    } finally {
      setEstablishing(false);
    }
  }

  useEffect(() => {
    let active = true;
    const supabase = getSupabaseClient();

    if (!supabase) {
      setError("ELO Web não está configurado: variáveis públicas do Supabase não foram definidas.");
      setLoading(false);
      return () => {
        active = false;
      };
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

      await establishELOSession(data.session);
      if (active) setLoading(false);
    });

    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      if (!active) return;

      setSession(nextSession);

      if (!nextSession) {
        setAuthorized(false);
        setEstablishing(false);
      }
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
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
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
      if (session) {
        await callELOAuthorization(session.access_token, "revoke_session");
      }
    } catch (revokeError) {
      setError(
        revokeError instanceof Error
          ? friendlyAuthError(revokeError.message)
          : "Não foi possível revogar a sessão do ELO.",
      );
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

  if (loading || establishing) {
    return (
      <main className="grid min-h-screen place-items-center bg-slate-950 p-6 text-white">
        <div className="text-center">
          <div className="mx-auto grid size-14 place-items-center rounded-2xl bg-white text-xl font-bold text-slate-950">E</div>
          <div className="mt-5 text-sm font-semibold">
            {loading ? "Inicializando ELO…" : "Estabelecendo sessão do ELO…"}
          </div>
          <div className="mt-2 text-xs text-white/45">Google → Supabase → ELO Authorization</div>
        </div>
      </main>
    );
  }

  if (!session || !authorized) {
    const authenticated = Boolean(session);

    return (
      <main className="grid min-h-screen place-items-center bg-slate-950 p-6 text-white">
        <section className="w-full max-w-md rounded-3xl border border-white/10 bg-white/[.04] p-8 text-center">
          <div className="mx-auto grid size-14 place-items-center rounded-2xl bg-white text-xl font-bold text-slate-950">E</div>
          <div className="mt-5 text-[10px] font-bold uppercase tracking-[.22em] text-white/40">ELO · teste de acesso</div>
          <h1 className="mt-2 text-2xl font-semibold">
            {authenticated ? "Google autenticado" : "Acesso ao ELO"}
          </h1>
          <p className="mt-3 text-sm leading-6 text-white/55">
            {authenticated
              ? "A identidade foi autenticada. Falta estabelecer a sessão operacional do ELO."
              : "Entre com Google para iniciar o teste da fronteira de autenticação."}
          </p>

          {error && (
            <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/10 p-3 text-left text-sm text-red-200" role="alert">
              <div className="font-semibold">Não foi possível continuar</div>
              <div className="mt-1 leading-5">{error}</div>
            </div>
          )}

          {authenticated ? (
            <button
              type="button"
              onClick={() => session && void establishELOSession(session)}
              disabled={establishing}
              className="mt-6 w-full rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 disabled:opacity-50"
            >
              {establishing ? "Estabelecendo sessão…" : "Estabelecer sessão do ELO"}
            </button>
          ) : (
            <button
              type="button"
              onClick={() => void signInWithGoogle()}
              disabled={signingIn}
              className="mt-6 w-full rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 disabled:opacity-50"
            >
              {signingIn ? "Abrindo Google…" : "Continuar com Google"}
            </button>
          )}

          <div className="mt-6 text-left text-[11px] leading-5 text-white/35">
            1. Google autentica a identidade.<br />
            2. Supabase mantém a sessão.<br />
            3. ELO Authorization estabelece a sessão ELO.<br />
            4. Nenhum grant é emitido pelo navegador.
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-950 p-6 text-white">
      <section className="w-full max-w-lg rounded-3xl border border-emerald-400/20 bg-white/[.04] p-8">
        <div className="text-[10px] font-bold uppercase tracking-[.22em] text-emerald-300/70">ELO · teste de acesso</div>
        <h1 className="mt-3 text-3xl font-semibold">Sessão ELO estabelecida</h1>
        <p className="mt-3 text-sm leading-6 text-white/55">
          A autenticação Google, a sessão Supabase e o <code>establish_session</code> do ELO Authorization concluíram o fluxo mínimo.
        </p>
        <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-4 text-sm">
          <div><span className="text-white/40">Identidade:</span> {session.user.email ?? "não informado"}</div>
          <div className="mt-2"><span className="text-white/40">Estado:</span> autorizado para a sessão ELO</div>
          <div className="mt-2"><span className="text-white/40">Próximo teste:</span> validar operações governadas separadamente</div>
        </div>
        <button
          type="button"
          onClick={() => void signOut()}
          className="mt-6 rounded-xl border border-white/10 px-4 py-2.5 text-sm font-semibold text-white/75 hover:bg-white/5"
        >
          Encerrar sessão
        </button>
      </section>
    </main>
  );
}
