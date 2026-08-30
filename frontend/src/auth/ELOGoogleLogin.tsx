import React, { useEffect, useState } from 'react';
import { createClient, type Session } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string;

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
});

type Props = { children: React.ReactNode };

export function ELOGoogleLogin({ children }: Props) {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    supabase.auth.getSession().then(({ data, error: sessionError }) => {
      if (!active) return;
      if (sessionError) setError(sessionError.message);
      setSession(data.session);
      setLoading(false);
    });

    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession);
      setLoading(false);
    });

    return () => {
      active = false;
      data.subscription.unsubscribe();
    };
  }, []);

  async function signInWithGoogle() {
    setError(null);
    const { error: authError } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    });
    if (authError) setError(authError.message);
  }

  async function signOut() {
    setError(null);
    const { error: signOutError } = await supabase.auth.signOut();
    if (signOutError) setError(signOutError.message);
  }

  if (loading) return <div role="status">Verificando sessão…</div>;
  if (session) {
    return (
      <div data-elo-auth="authenticated">
        <header style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center' }}>
          <span>Conectado ao ELO</span>
          <button type="button" onClick={signOut}>Sair</button>
        </header>
        {children}
        {error && <p role="alert">{error}</p>}
      </div>
    );
  }

  return (
    <main data-elo-auth="login" aria-labelledby="elo-login-title">
      <section>
        <h1 id="elo-login-title">Entrar no ELO</h1>
        <p>Use sua conta Google para acessar o ELO.</p>
        <button type="button" onClick={signInWithGoogle}>
          Continuar com Google
        </button>
        {error && <p role="alert">Não foi possível iniciar o login: {error}</p>}
      </section>
    </main>
  );
}
