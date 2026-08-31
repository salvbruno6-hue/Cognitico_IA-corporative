import { useEffect, useState } from 'react';
import { supabase } from './ELOGoogleLogin';

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

      // Keep the callback route free of provider tokens. The Supabase client
      // owns the session and persists/refreshes it according to its auth config.
      window.location.replace('/');
    });

    return () => {
      active = false;
    };
  }, []);

  return <main role="status">{message}</main>;
}
