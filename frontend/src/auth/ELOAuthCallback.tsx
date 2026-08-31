import { useEffect, useState } from 'react';
import { supabase } from './ELOGoogleLogin';

const ELO_BASE_PATH = import.meta.env.BASE_URL;

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

      window.location.replace(ELO_BASE_PATH);
    });

    return () => {
      active = false;
    };
  }, []);

  return <main role="status">{message}</main>;
}
