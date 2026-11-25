"""Teste estrutural do workflow de reconciliação."""
from __future__ import annotations

from pathlib import Path

import json
import runpy

import pytest
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


def test_runtime_requires_env_vars_and_thin_script_delegates():
    script = SCRIPT.read_text(encoding="utf-8")
    runtime = Path("src/elo/infrastructure/live_state_reconciliation.py").read_text(encoding="utf-8")
    assert "run_reconciliation_cli as main" in script
    assert "sys.exit(main())" in script
    assert "SUPABASE_URL" in runtime
    assert "SUPABASE_SERVICE_ROLE_KEY" in runtime


def test_workflow_propagates_reconciliation_failure():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "continue-on-error: true" not in text
    assert "set -o pipefail" in text
    assert "PyYAML==6.0.2" in text


@pytest.mark.parametrize(
    ("status", "expected_exit"),
    [
        ("PASS", 0),
        ("DRIFT", 3),
        ("UNKNOWN", 3),
        ("BLOCKED", 3),
        ("UNEXPECTED", 3),
        (None, 3),
    ],
)
def test_reconciliation_cli_only_succeeds_on_pass(
    monkeypatch, capsys, status, expected_exit
):
    from elo.infrastructure.live_state_reconciliation import LiveStateReconciliation
    from elo.infrastructure.supabase_rls_reader import SupabaseRLSStateReader

    monkeypatch.setenv("SUPABASE_URL", "https://example.invalid")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "dummy-local-test")
    monkeypatch.setattr(
        SupabaseRLSStateReader, "__init__", lambda self, url, key: None
    )

    class FakeReport:
        def to_dict(self):
            return {"scope": "rls", "overall": status, "tables": []}

    monkeypatch.setattr(
        LiveStateReconciliation, "reconcile", lambda self, reader: FakeReport()
    )
    run = runpy.run_path(str(SCRIPT))["main"]

    assert run() == expected_exit
    data = json.loads(capsys.readouterr().out)
    assert data["overall"] == status


def test_reconciliation_cli_missing_credentials_fails_closed(monkeypatch, capsys):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    run = runpy.run_path(str(SCRIPT))["main"]
    assert run() == 1
    assert "ERRO" in capsys.readouterr().err


def test_reconciliation_cli_runtime_error_fails_closed(monkeypatch, capsys):
    from elo.infrastructure.supabase_rls_reader import SupabaseRLSStateReader
    from elo.infrastructure.live_state_reconciliation import LiveStateReconciliation

    monkeypatch.setenv("SUPABASE_URL", "https://example.invalid")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "dummy")
    monkeypatch.setattr(SupabaseRLSStateReader, "__init__", lambda self, url, key: None)

    def failing_reconcile(self, reader):
        raise RuntimeError("controlled failure")

    monkeypatch.setattr(LiveStateReconciliation, "reconcile", failing_reconcile)
    run = runpy.run_path(str(SCRIPT))["main"]
    assert run() == 2
    assert "controlled failure" in capsys.readouterr().err
