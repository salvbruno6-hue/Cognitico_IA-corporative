"""Fail-closed structural checks for scoped ELO merge authorization and admin UI."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = (ROOT / ".github/workflows/elo-merge-coordinator.yml").read_text(encoding="utf-8")
PANEL = (ROOT / "apps/elo-web/src/components/elo-admin-grant-panel.tsx").read_text(encoding="utf-8")
DASHBOARD = (ROOT / "apps/elo-web/src/components/elo-dashboard.tsx").read_text(encoding="utf-8")


def test_merge_requires_exact_pr_and_head_sha():
    assert '.operation == ("merge_pr:" + $pr + ":" + $sha)' in WORKFLOW
    assert '.metadata.resource_id == $sha' in WORKFLOW
    assert '--arg pr "$PR_NUMBER" --arg sha "$HEAD_SHA"' in WORKFLOW
    assert '--match-head-commit "${{ steps.pr.outputs.sha }}"' in WORKFLOW


def test_merge_requires_independent_review():
    assert '.reviewDecision == "APPROVED"' in WORKFLOW
    assert '.author.login != $author' in WORKFLOW
    assert '.state == "APPROVED"' in WORKFLOW


def test_admin_form_uses_existing_session_and_authority():
    assert 'callELOAuthorization(accessToken, "issue_authorization_grant"' in PANEL
    assert 'authorization_state: "elo-merge-authorized"' in PANEL
    assert 'operation: `merge_pr:${pr}:${sha.toLowerCase()}`' in PANEL
    assert 'resource_id: sha.toLowerCase()' in PANEL
    assert 'expires_in_seconds: duration' in PANEL
    assert 'ELOAdminGrantPanel accessToken={accessToken}' in DASHBOARD
    assert 'activeNav === "Governança"' in DASHBOARD


def test_form_cannot_merge_or_store_tokens():
    assert "gh pr merge" not in PANEL
    assert "localStorage" not in PANEL
    assert "service_role" not in PANEL
    assert "create_operator_binding" not in PANEL
