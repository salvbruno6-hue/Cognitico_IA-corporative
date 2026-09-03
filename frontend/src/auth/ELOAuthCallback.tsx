import { useEffect, useState } from 'react';
import { supabase } from './ELOGoogleLogin';

const ELO_BASE_PATH = import.meta.env.BASE_URL;
const OAUTH_RETURN_KEY = 'elo.oauth.return_to';

function getSafeReturnPath() {
  const stored = sessionStorage.getItem(OAUTH_RETURN_KEY);
  sessionStorage.removeItem(OAUTH_RETURN_KEY);
  if (!stored) return ELO_BASE_PATH;

  try {
    const url = new URL(stored, window.location.origin);
    if (url.origin !== window.location.origin) return ELO_BASE_PATH;
    if (!url.pathname.startsWith(`${ELO_BASE_PATH.replace(/\/$/, '')}/oauth/consent`)) return ELO_BASE_PATH;
    return `${url.pathname}${url.search}${url.hash}`;
  } catch {
    return ELO_BASE_PATH;
  }
}

/**
 * Route component for /auth/callback.
 * Supabase processes the OAuth response and restores the persisted session.
 */
export function ELOAuthCallback() {
  const [message, setMessage] = useState('Finalizando autenticação…');

  useEffect(() => {
    let active = true;

    supabase.auth.getSession().then(({ data, error }) => {
      if (!active) return;
      if (error) {
        setMessage(`Não foi possível finalizar o login: ${error.message}`);
        return;
      }
      if (!data.session) {
        setMessage('Sessão não encontrada. Retorne ao login e tente novamente.');
        return;
      }

      window.location.replace(getSafeReturnPath());
    });

    return () => {
      active = false;
    };
  }, []);

  return <main role="status">{message}</main>;
}
