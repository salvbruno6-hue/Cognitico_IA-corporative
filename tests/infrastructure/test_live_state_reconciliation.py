"""Testes do harness de reconciliação live."""
from __future__ import annotations

from pathlib import Path

import pytest

from elo.infrastructure.live_state_reconciliation import (
    LiveStateReconciliation,
    ReconciliationStatus,
    RLSLiveState,
)


class MockReader:
    """Reader controlado para testes."""

    def __init__(self, states: dict[str, RLSLiveState]):
        self._states = states

    def read(self, table: str) -> RLSLiveState:
        if table not in self._states:
            return RLSLiveState(
                table=table,
                rls_enabled=None,
                read_error=f"table not found: {table}",
            )
        return self._states[table]


@pytest.fixture
def expected_yaml(tmp_path):
    content = """
schema_version: "1.0"
domain: supabase-live-state
scope: rls
tables:
  - name: table_ok
    expected_rls: true
    policies:
      - policy_a
  - name: table_drift
    expected_rls: true
    policies: []
  - name: table_unknown
    expected_rls: true
    policies: []
"""
    p = tmp_path / "expected.yaml"
    p.write_text(content, encoding="utf-8")
    return p


def test_all_pass(expected_yaml):
    reader = MockReader({
        "table_ok": RLSLiveState(
            "table_ok", True, ("policy_a",),
        ),
        "table_drift": RLSLiveState(
            "table_drift", True, (),
        ),
        "table_unknown": RLSLiveState(
            "table_unknown", True, (),
        ),
    })
    harness = LiveStateReconciliation(
        expected_state_path=expected_yaml
    )
    report = harness.reconcile(reader)
    assert report.overall == ReconciliationStatus.PASS


def test_drift_detected(expected_yaml):
    reader = MockReader({
        "table_ok": RLSLiveState(
            "table_ok", True, ("policy_a",),
        ),
        "table_drift": RLSLiveState(
            "table_drift", False, (),
        ),
        "table_unknown": RLSLiveState(
            "table_unknown", True, (),
        ),
    })
    harness = LiveStateReconciliation(
        expected_state_path=expected_yaml
    )
    report = harness.reconcile(reader)
    assert report.overall == ReconciliationStatus.DRIFT
    drift = next(
        t for t in report.tables if t.table == "table_drift"
    )
    assert drift.status == ReconciliationStatus.DRIFT
    assert "RLS mismatch" in " ".join(drift.reasons)


def test_missing_policy_is_drift(expected_yaml):
    reader = MockReader({
        "table_ok": RLSLiveState(
            "table_ok", True, (),  # esperado policy_a
        ),
        "table_drift": RLSLiveState(
            "table_drift", True, (),
        ),
        "table_unknown": RLSLiveState(
            "table_unknown", True, (),
        ),
    })
    harness = LiveStateReconciliation(
        expected_state_path=expected_yaml
    )
    report = harness.reconcile(reader)
    ok = next(t for t in report.tables if t.table == "table_ok")
    assert ok.status == ReconciliationStatus.DRIFT
    assert any("missing policies" in r for r in ok.reasons)


def test_unknown_live_state(expected_yaml):
    reader = MockReader({
        "table_ok": RLSLiveState(
            "table_ok", True, ("policy_a",),
        ),
        "table_drift": RLSLiveState(
            "table_drift", True, (),
        ),
        "table_unknown": RLSLiveState(
            "table_unknown", None, (),
        ),
    })
    harness = LiveStateReconciliation(
        expected_state_path=expected_yaml
    )
    report = harness.reconcile(reader)
    unknown = next(
        t for t in report.tables if t.table == "table_unknown"
    )
    assert unknown.status == ReconciliationStatus.UNKNOWN
    assert report.overall == ReconciliationStatus.UNKNOWN


def test_blocked_on_reader_error(expected_yaml):
    reader = MockReader({
        "table_ok": RLSLiveState(
            "table_ok", True, ("policy_a",),
        ),
        "table_drift": RLSLiveState(
            "table_drift", True, (),
        ),
    })
    harness = LiveStateReconciliation(
        expected_state_path=expected_yaml
    )
    report = harness.reconcile(reader)
    assert report.overall == ReconciliationStatus.BLOCKED
    blocked = next(
        t for t in report.tables if t.table == "table_unknown"
    )
    assert blocked.status == ReconciliationStatus.BLOCKED


def test_report_is_serializable(expected_yaml):
    reader = MockReader({
        "table_ok": RLSLiveState(
            "table_ok", True, ("policy_a",),
        ),
        "table_drift": RLSLiveState(
            "table_drift", True, (),
        ),
        "table_unknown": RLSLiveState(
            "table_unknown", True, (),
        ),
    })
    harness = LiveStateReconciliation(
        expected_state_path=expected_yaml
    )
    report = harness.reconcile(reader)
    serialized = report.to_dict()
    assert serialized["scope"] == "rls"
    assert "tables" in serialized


def test_harness_reads_real_expected_yaml():
    """Verifica que o YAML real em main carrega."""
    real = Path(
        "09-governance/contracts/expected_state/supabase_rls.yaml"
    )
    if not real.exists():
        pytest.skip("expected_state YAML ainda não existe")
    harness = LiveStateReconciliation(expected_state_path=real)
    data = harness.load_expected()
    assert data["scope"] == "rls"
    names = [t["name"] for t in data["tables"]]
    assert "lista_mae" in names
    assert "fornecedor_cotacoes" in names
    assert "lista_mae_alteracoes" in names
