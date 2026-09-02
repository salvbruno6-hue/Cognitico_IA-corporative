import { useEffect, useState } from 'react';
import { supabase } from './ELOGoogleLogin';
import './login.css';

export function ELOOAuthConsent() {
  const [authorizationId, setAuthorizationId] = useState('');
  const [details, setDetails] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const id = new URLSearchParams(window.location.search).get('authorization_id') ?? '';
    setAuthorizationId(id);

    if (!id) {
      setLoading(false);
      setError('Solicitação OAuth inválida: authorization_id ausente.');
      return;
    }

    void (async () => {
      const { data: sessionData } = await supabase.auth.getSession();
      if (!active) return;

      if (!sessionData.session) {
        const redirectTo = window.location.href;
        const { error: authError } = await supabase.auth.signInWithOAuth({
          provider: 'google',
          options: { redirectTo },
        });
        if (authError && active) setError(authError.message);
        if (active) setLoading(false);
        return;
      }

      const { data, error: detailsError } = await supabase.auth.oauth.getAuthorizationDetails(id);
      if (!active) return;
      if (detailsError) setError(detailsError.message);
      else setDetails(data);
      setLoading(false);
    })();

    return () => { active = false; };
  }, []);

  async function decide(approve: boolean) {
    if (!authorizationId) return;
    setBusy(true);
    setError(null);
    const result = approve
      ? await supabase.auth.oauth.approveAuthorization(authorizationId)
      : await supabase.auth.oauth.denyAuthorization(authorizationId);
    if (result.error) {
      setError(result.error.message);
      setBusy(false);
      return;
    }
    if (result.data?.redirect_url) window.location.replace(result.data.redirect_url);
  }

  if (loading) return <main role="status" className="elo-loading">Preparando autorização segura…</main>;

  return (
    <main data-elo-auth="oauth-consent" className="elo-setup-page">
      <section className="elo-login-panel elo-setup-panel">
        <div className="elo-login-content">
          <div className="elo-login-logo" aria-label="ELO"><span className="elo-login-wordmark" aria-hidden="true">EL</span><span className="elo-login-orbit" aria-hidden="true"><i /><b /></span></div>
          <span className="elo-setup-kicker">AUTORIZAÇÃO ELO</span>
          <h1>Autorizar acesso</h1>
          {details ? (
            <>
              <p className="elo-setup-lead">Uma aplicação está solicitando acesso ao ELO por OAuth 2.1.</p>
              <div className="elo-setup-status" aria-label="Detalhes da autorização">
                <div><span className="elo-status-dot" /><strong>Aplicação</strong><small>{details.client?.name ?? details.client_name ?? 'Cliente OAuth'}</small></div>
                <div><span className="elo-status-dot" /><strong>Usuário</strong><small>{details.user?.email ?? 'Sessão administrativa autenticada'}</small></div>
                <div><span className="elo-status-dot" /><strong>Escopos</strong><small>{details.scope ?? 'Acesso solicitado pelo cliente'}</small></div>
              </div>
              <p className="elo-setup-note">A aprovação libera somente os escopos apresentados acima. O MCP do ELO permanece somente leitura nesta primeira fase.</p>
              <div className="elo-consent-actions">
                <button className="elo-google-button elo-chatgpt-button" type="button" disabled={busy} onClick={() => decide(true)}>Autorizar acesso</button>
                <button className="elo-setup-secondary" type="button" disabled={busy} onClick={() => decide(false)}>Negar</button>
              </div>
            </>
          ) : (
            <p className="elo-login-error" role="alert">{error ?? 'Não foi possível carregar a solicitação de autorização.'}</p>
          )}
          {error && details && <p className="elo-login-error" role="alert">{error}</p>}
        </div>
      </section>
    </main>
  );
}
