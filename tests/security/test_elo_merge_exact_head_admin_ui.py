"""Fail-closed UI contract checks: merge authority remains the canonical ELO #1177."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PANEL = (ROOT / "apps/elo-web/src/components/elo-admin-grant-panel.tsx").read_text(encoding="utf-8")
DASHBOARD = (ROOT / "apps/elo-web/src/components/elo-dashboard.tsx").read_text(encoding="utf-8")


def test_admin_form_uses_existing_session_and_exact_pr_sha_resource():
    assert 'callELOAuthorization(accessToken, "issue_authorization_grant"' in PANEL
    assert 'authorization_state: "elo-merge-authorized"' in PANEL
    assert 'operation: "merge"' in PANEL
    assert 'resource_id: `pr:${pr}@${sha.toLowerCase()}`' in PANEL
    assert 'operation: `merge_pr:' not in PANEL
    assert 'resource_id: sha.toLowerCase()' not in PANEL
    assert 'expires_in_seconds: duration' in PANEL
    assert 'ELOAdminGrantPanel accessToken={accessToken}' in DASHBOARD
    assert 'activeNav === "Governança"' in DASHBOARD


def test_invalid_inputs_and_unconfirmed_review_cannot_request_grant():
    assert 'const SHA_PATTERN = /^[0-9a-f]{40}$/i;' in PANEL
    assert 'bindingId.trim().length > 0' in PANEL
    assert '/^[1-9][0-9]*$/.test(pr)' in PANEL
    assert 'SHA_PATTERN.test(sha)' in PANEL
    assert 'duration >= 60 && duration <= 3600 && confirmed' in PANEL
    assert 'if (!valid || busy) return;' in PANEL
    assert 'Revisei os gates e confirmei aprovação independente' in PANEL


def test_form_does_not_merge_or_persist_sensitive_credentials():
    assert 'gh pr merge' not in PANEL
    assert 'localStorage' not in PANEL
    assert 'service_role' not in PANEL
    assert 'create_operator_binding' not in PANEL
    assert 'callELOAuthorization(accessToken, "issue_authorization_grant"' in PANEL
