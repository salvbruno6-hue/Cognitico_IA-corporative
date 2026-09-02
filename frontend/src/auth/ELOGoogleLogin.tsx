import React, { useEffect, useState } from 'react';
import { createClient, type Session } from '@supabase/supabase-js';
import { playELOSound, startELOAmbient } from '../eloSound';
import './login.css';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('ELO Auth: VITE_SUPABASE_URL e VITE_SUPABASE_ANON_KEY são obrigatórias.');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
});

type Props = { children: React.ReactNode };

function GoogleIcon() {
  return (
    <svg className="elo-google-icon" viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.2 6.1 29.4 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5Z" />
      <path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 16 18.9 12 24 12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.2 6.1 29.4 4 24 4c-7.7 0-14.3 4.3-17.7 10.7Z" />
      <path fill="#4CAF50" d="M24 44c5.2 0 10-2 13.6-5.2l-6.3-5.3C29.4 35 26.8 36 24 36c-5.2 0-9.7-3.3-11.3-8l-6.5 5C9.6 39.4 16.2 44 24 44Z" />
      <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-1.1 3.1-3.7 5.5-7 6.6l.1.1 6.3 5.3C34.3 40.6 44 34 44 24c0-1.3-.1-2.4-.4-3.5Z" />
    </svg>
  );
}

function ELOLogo() {
  return <div className="elo-login-logo" aria-label="ELO"><span className="elo-login-wordmark" aria-hidden="true">EL</span><span className="elo-login-orbit" aria-hidden="true"><i /><b /></span></div>;
}

function getPublicOrigin() {
  const configuredOrigin = import.meta.env.VITE_ELO_PUBLIC_URL as string | undefined;
  return (configuredOrigin || window.location.origin).replace(/\/$/, '');
}

export function ELOGoogleLogin({ children }: Props) {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [setup, setSetup] = useState(false);

  useEffect(() => {
    let active = true;
    void supabase.auth.getSession().then(({ data, error: sessionError }) => {
      if (!active) return;
      if (sessionError) setError(sessionError.message);
      setSession(data.session);
      setLoading(false);
    });
    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      if (!active) return;
      setSession(nextSession);
      setLoading(false);
    });
    return () => { active = false; data.subscription.unsubscribe(); };
  }, []);

  async function signInWithGoogle() {
    setError(null);
    startELOAmbient();
    playELOSound('click');
    const base = import.meta.env.BASE_URL || '/';
    const callbackPath = `${base.replace(/\/$/, '')}/auth/callback`;
    const redirectTo = new URL(callbackPath, `${getPublicOrigin()}/`).toString();
    const { error: authError } = await supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo } });
    if (authError) setError(authError.message);
  }

  async function signOut() {
    setError(null);
    const { error: signOutError } = await supabase.auth.signOut();
    if (signOutError) setError(signOutError.message);
  }

  function continueToChatGPT() {
    playELOSound('success');
    window.open('https://chatgpt.com/', '_blank', 'noopener,noreferrer');
  }

  if (loading) return <div role="status" className="elo-loading">Verificando sessão…</div>;

  if (session && !setup) {
    return (
      <main data-elo-auth="setup" className="elo-setup-page">
        <section className="elo-login-panel elo-setup-panel">
          <div className="elo-login-content">
            <ELOLogo />
            <span className="elo-setup-kicker">CONFIGURAÇÃO INICIAL</span>
            <h1>Preparar acesso ao ELO</h1>
            <p className="elo-setup-lead">Sua identidade administrativa já foi autenticada. Agora escolha como deseja entrar na camada conversacional do ELO.</p>
            <div className="elo-setup-status" aria-label="Status da configuração">
              <div><span className="elo-status-dot" /> <strong>Google</strong><small>Identidade autenticada</small></div>
              <div><span className="elo-status-dot" /> <strong>Supabase</strong><small>Sessão ELO ativa</small></div>
              <div><span className="elo-status-pending" /> <strong>ChatGPT</strong><small>Conexão ainda não autorizada</small></div>
            </div>
            <button className="elo-google-button elo-chatgpt-button" type="button" onClick={continueToChatGPT}>Continuar para o ChatGPT</button>
            <p className="elo-setup-note">A abertura do ChatGPT não concede, por si só, acesso ao ELO. A autorização entre ChatGPT e ELO será concluída por uma integração OAuth/MCP compatível.</p>
            <button className="elo-setup-secondary" type="button" onClick={() => setSetup(true)}>Entrar no Núcleo ELO agora</button>
            <button className="elo-setup-signout" type="button" onClick={signOut}>Sair da sessão administrativa</button>
          </div>
        </section>
      </main>
    );
  }

  if (session && setup) {
    return <div data-elo-auth="authenticated">{children}<button type="button" onClick={signOut}>Sair</button>{error && <p role="alert">{error}</p>}</div>;
  }

  return (
    <main data-elo-auth="login" aria-labelledby="elo-login-title">
      <section className="elo-login-panel"><div className="elo-login-content">
        <ELOLogo /><h1 id="elo-login-title">Entrar no ELO</h1>
        <button className="elo-google-button" type="button" onClick={signInWithGoogle} onKeyDown={(event) => { if (event.key === 'Enter' || event.key === ' ') startELOAmbient(); }}><GoogleIcon /><span>Continuar com Google</span></button>
        <p className="elo-login-description">Use sua conta Google para acessar o ELO.</p>
        {error && <p className="elo-login-error" role="alert">Não foi possível iniciar o login: {error}</p>}
      </div></section>
    </main>
  );
}
