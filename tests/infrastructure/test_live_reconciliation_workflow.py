"""Teste estrutural do workflow de reconciliação."""
from __future__ import annotations

from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/elo-live-reconciliation.yml")
SCRIPT = Path("scripts/run_live_reconciliation.py")


def test_script_exists():
    assert SCRIPT.exists()


def test_workflow_exists():
    assert WORKFLOW.exists()


def test_workflow_has_dispatch_and_schedule():
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    triggers = data.get("on") or data.get(True)
    assert "workflow_dispatch" in triggers
    assert "schedule" in triggers


def test_workflow_is_read_only():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "contents: read" in text
    assert "contents: write" not in text


def test_workflow_does_not_execute_ddl():
    text = WORKFLOW.read_text(encoding="utf-8")
    for forbidden in [
        "ALTER TABLE",
        "CREATE POLICY",
        "DROP POLICY",
        "supabase db push",
        "supabase migration up",
    ]:
        assert forbidden not in text


def test_script_requires_env_vars():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "SUPABASE_URL" in text
    assert "SUPABASE_SERVICE_ROLE_KEY" in text
