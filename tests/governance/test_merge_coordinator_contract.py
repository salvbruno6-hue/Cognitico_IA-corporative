"""Teste estrutural do Merge Coordinator.

Não executa o workflow — apenas valida invariantes
declarados no YAML e no contrato.
"""
from __future__ import annotations

from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/elo-merge-coordinator.yml")
CONTRACT = Path("docs/governance/ELO_MERGE_COORDINATOR.md")


def test_workflow_exists():
    assert WORKFLOW.exists()


def test_contract_exists():
    assert CONTRACT.exists()


def test_workflow_triggers_on_workflow_run():
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    triggers = data.get("on") or data.get(True)
    assert "workflow_run" in triggers
    wf_run = triggers["workflow_run"]
    assert "ELO Agent Loop" in wf_run["workflows"]
    assert "ELO Evolution Gate" in wf_run["workflows"]


def test_workflow_does_not_use_admin():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "--admin" not in text
    assert "push --force" not in text
    assert "push -f" not in text


def test_workflow_checks_authz_grant():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "elo-merge-authorized" in text
    assert "elo_authorization_grants" in text
    assert "revoked_at=is.null" in text


def test_workflow_uses_squash():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "gh pr merge" in text
    assert "--squash" in text


def test_workflow_does_not_close_issues_automatically():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "gh issue close" not in text


def test_contract_declares_no_authority_creation():
    text = CONTRACT.read_text(encoding="utf-8")
    # O contrato usa: "Ele NÃO: - Cria autorização - Fabrica decisão"
    assert "Cria autorização" in text or "cria autorização" in text
    assert "Fabrica decisão" in text or "fabrica decisão" in text



AGENT_WORKFLOW = Path(".github/workflows/elo-agent-loop.yml")
MAINTENANCE_WORKFLOW = Path(".github/workflows/elo-maintenance-coordinator.yml")


def _shell_step(workflow: Path, name: str) -> str:
    data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    scripts = [
        item["run"] for job in data["jobs"].values()
        for item in job.get("steps", [])
        if item.get("name") == name and "run" in item
    ]
    assert len(scripts) == 1, (workflow, name)
    return scripts[0]


def test_pr_ready_requires_bot_run_current_pr_and_sha():
    producer = AGENT_WORKFLOW.read_text(encoding="utf-8")
    consumer = _shell_step(WORKFLOW, "Verify PR-ready evidence")
    assert "ELO_AGENT_LOOP_RUN_ID=${GITHUB_RUN_ID}" in producer
    assert "ELO_AGENT_LOOP_PR_NUMBER=${PR_NUMBER}" in producer
    for token in (
        '.author.login == "github-actions[bot]"',
        'startswith("ELO execution cycle reached PR-ready state. Commit " + $sha',
        'contains("ELO_AGENT_LOOP_PR_NUMBER=" + $pr)',
        'capture("ELO_AGENT_LOOP_RUN_ID=(?<id>[0-9]+)")',
        '.name == "ELO Agent Loop"',
        '.conclusion == "success"',
        '.repository.full_name == $repo',
    ):
        assert token in consumer


def test_maintenance_requires_bot_run_current_pr_and_sha():
    producer = MAINTENANCE_WORKFLOW.read_text(encoding="utf-8")
    consumer = _shell_step(WORKFLOW, "Verify applicable ELO gate evidence")
    for token in (
        "ELO_MAINTENANCE_RUN_ID=${GITHUB_RUN_ID}",
        "ELO_MAINTENANCE_PR_NUMBER=${PR_NUMBER}",
        "ELO_HEAD_SHA=${PR_HEAD_SHA}",
    ):
        assert token in producer
    for token in (
        '.author.login == "github-actions[bot]"',
        'startswith("ELO Maintenance Coordinator: **APPROVED_FOR_MERGE**.")',
        'contains("ELO_MAINTENANCE_PR_NUMBER=" + $pr)',
        'contains("ELO_HEAD_SHA=" + $sha)',
        'capture("ELO_MAINTENANCE_RUN_ID=(?<id>[0-9]+)")',
        '.name == "ELO Maintenance Coordinator"',
        '.conclusion == "success"',
    ):
        assert token in consumer


def test_merge_grant_requires_exact_operation_resource_and_live_session():
    script = _shell_step(WORKFLOW, "Verify elo-merge-authorized in Supabase")
    for token in (
        "required_resource=\"pr:${PR_NUMBER}@${HEAD_SHA}\"",
        "&operation=eq.merge&",
        ".metadata.resource_id == $resource",
        '.metadata.issuer_role == "CANONICAL_ADMIN"',
        ".session_id != null",
        "identity_id == $identity",
        "session_now_epoch < session_expires_epoch",
        "elo_operator_github_bindings",
        "elo_identity_roles",
        "elo_identity_sessions",
    ):
        assert token in script


def test_merge_rechecks_same_sha_immediately_before_merge():
    script = _shell_step(WORKFLOW, "Execute governed squash merge")
    assert ".headRefOid == $sha" in script
    assert "gh pr merge" in script
    assert "--admin" not in script


def test_provenance_workflow_steps_are_valid_bash():
    import subprocess

    for workflow, name in (
        (WORKFLOW, "Verify PR-ready evidence"),
        (WORKFLOW, "Verify applicable ELO gate evidence"),
        (WORKFLOW, "Verify elo-merge-authorized in Supabase"),
        (WORKFLOW, "Execute governed squash merge"),
        (AGENT_WORKFLOW, "Register PR awaiting authorized merge"),
        (MAINTENANCE_WORKFLOW, "Publish governed audit decision"),
    ):
        script = _shell_step(workflow, name)
        result = subprocess.run(
            ["bash", "-n"], input=script, text=True, capture_output=True
        )
        assert result.returncode == 0, (str(workflow), name, result.stderr)
