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
