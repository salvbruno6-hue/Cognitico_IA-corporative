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



def _jq_filter_for_comment_step(step_name: str) -> str:
    script = _shell_step(WORKFLOW, step_name)
    # The workflow's jq program is an actual inlined multiline string.
    opening = '''jq -r --arg sha "$HEAD_SHA" --arg pr "$PR_NUMBER" ' '''
    opening = opening.rstrip()
    assert opening in script, step_name
    start = script.index(opening) + len(opening)
    end = script.index('\' <<<"$comments")"', start)
    return script[start:end]


def _jq_run(filter_source: str, payload: object, *args: str) -> list[str]:
    import json
    import shutil
    import subprocess
    import pytest

    if shutil.which("jq") is None:
        pytest.skip("jq required for workflow provenance behavior tests")
    command = ["jq", "-cr", *args, filter_source]
    result = subprocess.run(
        command, input=json.dumps(payload), text=True,
        capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip().splitlines() if result.stdout.strip() else []


def test_pr_ready_provenance_rejects_human_and_wrong_sha():
    query = _jq_filter_for_comment_step("Verify PR-ready evidence")
    prefix = "ELO execution cycle reached PR-ready state. Commit "
    good = prefix + "aabbcc passed ELO and applicable laboratory gates. " + (
        "ELO_AGENT_LOOP_RUN_ID=1234 ELO_AGENT_LOOP_PR_NUMBER=1177"
    )
    rows = [
        {"author": {"login": "salvbruno6-hue"}, "body": good},
        {"author": {"login": "github-actions[bot]"}, "body": good.replace("aabbcc", "other")},
        {"author": {"login": "github-actions[bot]"}, "body": good.replace("1177", "9999")},
    ]
    args = ("--arg", "sha", "aabbcc", "--arg", "pr", "1177")
    assert _jq_run(query, {"comments": rows}, *args) == []
    rows.append({"author": {"login": "github-actions[bot]"}, "body": good})
    assert _jq_run(query, {"comments": rows}, *args) == ["1234"]


def test_maintenance_provenance_rejects_human_and_stale_sha():
    query = _jq_filter_for_comment_step("Verify applicable ELO gate evidence")
    good = ("ELO Maintenance Coordinator: **APPROVED_FOR_MERGE**. "
            "ELO_MAINTENANCE_RUN_ID=890 ELO_MAINTENANCE_PR_NUMBER=1177 ELO_HEAD_SHA=aabbcc")
    rows = [
        {"author": {"login": "salvbruno6-hue"}, "body": good},
        {"author": {"login": "github-actions[bot]"}, "body": good.replace("aabbcc", "other")},
    ]
    args = ("--arg", "sha", "aabbcc", "--arg", "pr", "1177")
    assert _jq_run(query, {"comments": rows}, *args) == []
    rows.append({"author": {"login": "github-actions[bot]"}, "body": good})
    assert _jq_run(query, {"comments": rows}, *args) == ["890"]


def test_merge_grant_filter_rejects_other_operation_resource_or_session():
    script = _shell_step(WORKFLOW, "Verify elo-merge-authorized in Supabase")
    opening = '''jq -c --arg resource "$required_resource" ' '''
    opening = opening.rstrip()
    assert opening in script
    start = script.index(opening) + len(opening)
    end = script.index('\' <<<"$grants")', start)
    filter_source = script[start:end]
    valid = {
        "grant_id": "good", "operation": "merge", "revoked_at": None,
        "session_id": "session1",
        "metadata": {"issuer_role": "CANONICAL_ADMIN", "resource_id": "pr:1177@aabbcc"}
    }
    others = [
        {**valid, "grant_id": "wrong-operation", "operation": "execute"},
        {**valid, "grant_id": "wrong-pr", "metadata": {
            "issuer_role": "CANONICAL_ADMIN", "resource_id": "pr:999@aabbcc"
        }},
        {**valid, "grant_id": "no-session", "session_id": None},
        {**valid, "grant_id": "wrong-issuer", "metadata": {
            "issuer_role": "USER", "resource_id": "pr:1177@aabbcc"
        }},
        {**valid, "grant_id": "revoked", "revoked_at": "2026-11-10T00:00:00Z"},
    ]
    output = _jq_run(
        filter_source, others + [valid],
        "--arg", "resource", "pr:1177@aabbcc",
    )
    import json
    assert [json.loads(row)["grant_id"] for row in output] == ["good"]



def test_agent_loop_supports_existing_pr_attestation_without_parallel_workflow():
    data = yaml.safe_load(AGENT_WORKFLOW.read_text(encoding="utf-8"))
    triggers = data.get("on") or data.get(True)
    assert "pull_request" in triggers
    assert "labeled" in triggers["pull_request"]["types"]
    dispatch = triggers["workflow_dispatch"]["inputs"]
    assert dispatch["issue_number"]["required"] is False
    assert dispatch["pr_number"]["required"] is False
    assert dispatch["expected_head_sha"]["required"] is False
    assert "attest-existing-pr" in data["jobs"]


def test_existing_pr_attestation_is_read_only_and_secret_minimal():
    data = yaml.safe_load(AGENT_WORKFLOW.read_text(encoding="utf-8"))
    job = data["jobs"]["attest-existing-pr"]
    text = str(job)
    assert "openai/codex-action" not in text
    assert "SUPABASE_SERVICE_ROLE_KEY" not in text
    assert "git commit" not in text
    assert "git push" not in text
    assert "gh pr create" not in text
    assert job["permissions"]["contents"] == "read"
    assert job["permissions"]["pull-requests"] == "write"
    assert job["permissions"]["actions"] == "read"


def test_existing_pr_attestation_freezes_sha_and_reuses_canonical_reconciliation():
    text = AGENT_WORKFLOW.read_text(encoding="utf-8")
    for token in (
        "ATTEST_EXISTING_PR",
        "expected_head_sha",
        "pr:$PR_NUMBER@$head_sha",
        "Verify required GitHub checks",
        "Verify Evolution Gate for immutable head",
        "elo_canonical_reconciliation",
        "reuse_analysis_complete == true",
        "duplicate_or_parallel == false",
        "Revalidate immutable head and reviews",
        "PR head changed before PR-ready publication",
        "ELO_PR_READY_V2=1",
        "ELO_RESOURCE_ID=",
    ):
        assert token in text


def test_create_and_attest_lanes_emit_same_pr_ready_contract():
    text = AGENT_WORKFLOW.read_text(encoding="utf-8")
    assert "ELO_AGENT_LOOP_MODE=CREATE_FROM_ISSUE" in text
    assert "ELO_AGENT_LOOP_MODE=ATTEST_EXISTING_PR" in text
    assert text.count("ELO_PR_READY_V2=1") >= 2
    assert text.count("ELO_AGENT_LOOP_RUN_ID=${GITHUB_RUN_ID}") >= 2
    assert text.count("ELO_AGENT_LOOP_PR_NUMBER=${PR_NUMBER}") >= 2


def test_attestation_shell_steps_are_valid_bash():
    import subprocess
    data = yaml.safe_load(AGENT_WORKFLOW.read_text(encoding="utf-8"))
    steps = [step for step in data["jobs"]["attest-existing-pr"]["steps"] if "run" in step]
    assert steps
    for step in steps:
        result = subprocess.run(
            ["bash", "-n"], input=step["run"], text=True, capture_output=True
        )
        assert result.returncode == 0, (step["name"], result.stderr)
