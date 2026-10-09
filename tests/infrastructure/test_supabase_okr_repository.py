from __future__ import annotations

from typing import Any

import pytest

from elo.contracts.okr import KeyResultDirection, TargetApprovalState
from elo.infrastructure.supabase_okr_repository import SupabaseOkrReadRepository


class StubRepository(SupabaseOkrReadRepository):
    def __init__(self, rows_by_table: dict[str, list[dict[str, Any]]]) -> None:
        super().__init__("https://example.supabase.co", "service-role-test-key")
        self.rows_by_table = rows_by_table
        self.calls: list[tuple[str, dict[str, str]]] = []

    def _get_rows(self, table: str, params: dict[str, str]) -> list[dict[str, Any]]:
        self.calls.append((table, params))
        return list(self.rows_by_table.get(table, []))


def _objective_row(**overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "tenant_id": "tenant-a",
        "objective_id": "obj-1",
        "title": "Aumentar previsibilidade operacional",
        "strategy_ref": "strategy-1",
        "owner_ref": "planning",
        "evidence_refs": ["ev-obj-1"],
    }
    row.update(overrides)
    return row


def _kr_row(**overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "tenant_id": "tenant-a",
        "key_result_id": "kr-1",
        "objective_id": "obj-1",
        "title": "Elevar aderência do planejamento",
        "metric_code": "KPI_ADERENCIA",
        "direction": "INCREASE",
        "baseline": "50",
        "target": "80",
        "deadline": "2026-12-31",
        "weight": "1.5",
        "baseline_evidence_refs": ["ev-baseline"],
        "target_evidence_refs": ["ev-target"],
        "target_approval_state": "APPROVED",
        "target_approval_ref": "approval-1",
    }
    row.update(overrides)
    return row


def test_get_objective_is_tenant_filtered_and_maps_contract() -> None:
    repo = StubRepository({"elo_strategic_objectives": [_objective_row()]})

    objective = repo.get_objective(tenant_id="tenant-a", objective_id="obj-1")

    assert objective is not None
    assert objective.tenant_id == "tenant-a"
    assert objective.objective_id == "obj-1"
    assert objective.evidence_refs == ("ev-obj-1",)
    table, params = repo.calls[0]
    assert table == "elo_strategic_objectives"
    assert params["tenant_id"] == "eq.tenant-a"
    assert params["objective_id"] == "eq.obj-1"


def test_get_key_result_maps_existing_kpi_identity_without_defining_kpi() -> None:
    repo = StubRepository({"elo_strategic_key_results": [_kr_row()]})

    key_result = repo.get_key_result(tenant_id="tenant-a", key_result_id="kr-1")

    assert key_result is not None
    assert key_result.metric_code == "KPI_ADERENCIA"
    assert key_result.direction is KeyResultDirection.INCREASE
    assert key_result.target_approval_state is TargetApprovalState.APPROVED
    assert key_result.target_approval_ref == "approval-1"
    assert str(key_result.weight) == "1.5"


def test_list_key_results_rejects_cross_tenant_row_even_with_service_role() -> None:
    repo = StubRepository({"elo_strategic_key_results": [_kr_row(tenant_id="tenant-b")]})

    with pytest.raises(PermissionError, match="tenant boundary"):
        repo.list_key_results(tenant_id="tenant-a", objective_id="obj-1")


def test_list_key_results_rejects_wrong_objective_row() -> None:
    repo = StubRepository({"elo_strategic_key_results": [_kr_row(objective_id="obj-2")]})

    with pytest.raises(PermissionError, match="different Objective"):
        repo.list_key_results(tenant_id="tenant-a", objective_id="obj-1")


def test_measurements_fail_closed_without_approved_binding() -> None:
    repo = StubRepository({})

    assert repo.list_measurements(tenant_id="tenant-a", key_result_id="kr-1") == ()
    assert repo.calls == []


def test_blank_scope_is_rejected_before_any_storage_read() -> None:
    repo = StubRepository({})

    with pytest.raises(ValueError, match="tenant_id is required"):
        repo.get_objective(tenant_id=" ", objective_id="obj-1")

    assert repo.calls == []
