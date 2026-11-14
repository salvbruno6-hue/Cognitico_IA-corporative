"""Fail-closed structural checks for scoped ELO merge authorization and admin UI."""
import json
import shlex
import subprocess

import pytest
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


@pytest.mark.parametrize(
    "review_sha,reviewer,state,decision,expected",
    [
        ("a" * 40, "independent", "APPROVED", "APPROVED", True),
        ("b" * 40, "independent", "APPROVED", "APPROVED", False),
        (None, "independent", "APPROVED", "APPROVED", False),
        ("a" * 40, "pr-author", "APPROVED", "APPROVED", False),
        ("a" * 40, None, "APPROVED", "APPROVED", False),
        ("a" * 40, "independent", "COMMENTED", "APPROVED", False),
        ("a" * 40, "independent", "APPROVED", "REVIEW_REQUIRED", False),
    ],
)
def test_independent_review_gate_evaluates_exact_head(
    review_sha, reviewer, state, decision, expected
):
    # Execute the actual workflow predicate, rather than mirroring its logic.
    line = next(line for line in WORKFLOW.splitlines()
                if "jq -e" in line and '.reviewDecision == "APPROVED"' in line)
    command = shlex.split(line.strip().replace("${{ steps.pr.outputs.sha }}", "a" * 40))
    command = command[:command.index("/tmp/pr.json")]
    review = {"state": state, "author": {"login": reviewer}}
    if review_sha is not None:
        review["commit"] = {"oid": review_sha}
    payload = {"reviewDecision": decision, "author": {"login": "pr-author"},
               "reviews": [review]}
    result = subprocess.run(command, input=json.dumps(payload), text=True,
                            capture_output=True, check=False)
    assert result.returncode in (0, 1), result.stderr
    assert (result.returncode == 0) is expected
