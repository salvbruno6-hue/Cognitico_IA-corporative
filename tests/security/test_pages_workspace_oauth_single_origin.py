"""GitHub Pages must be an entry, not a second operational OAuth session."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = (ROOT / "frontend/src/auth/ELOGoogleLogin.tsx").read_text(encoding="utf-8")
WEB = (ROOT / "apps/elo-web/src/auth/ELOWebAuthBoundary.tsx").read_text(encoding="utf-8")
CALLBACK = (ROOT / "apps/elo-web/src/app/auth/callback/page.tsx").read_text(encoding="utf-8")


def test_pages_login_delegates_to_web_origin():
    component = PAGES.split("export function ELOGoogleLogin(", 1)[1]
    assert 'window.location.assign(`${getOperationalWorkspaceUrl()}/?start=google`)' in component
    assert "signInWithOAuth" not in component
    assert "establishELOAuthorizationSession" not in component
    assert "session.access_token" not in component
    assert "localStorage" not in component


def test_web_is_operational_auth_owner():
    assert 'createOAuthFlow(supabase.auth)' in WEB
    assert 'callELOAuthorization(data.session.access_token, "establish_session")' in WEB
    assert 'setWorkspaceOpen(true)' in WEB
    assert 'flow.complete(window.location.href' in CALLBACK


def test_pages_consent_callback_is_preserved():
    assert "export async function establishELOAuthorizationSession" in PAGES
    assert "export const supabase" in PAGES
