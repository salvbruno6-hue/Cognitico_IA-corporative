from __future__ import annotations

from decimal import Decimal
from typing import Any

from elo.application.commands.okr_write import SnapshotBindingWrite
from elo.contracts.okr import KeyResult, KeyResultDirection, Objective, TargetApprovalState
from elo.infrastructure.supabase_okr_writer import SupabaseOkrWriteRepository


class StubWriter(SupabaseOkrWriteRepository):
    def __init__(self) -> None:
        super().__init__("https://example.supabase.co", "service-role-test-key")
        self.posts: list[tuple[str, dict[str, Any], str]] = []

    def _post(self, table: str, payload: dict[str, Any], *, on_conflict: str) -> None:
        self.posts.append((table, payload, on_conflict))


def test_objective_writer_targets_only_approved_owner() -> None:
    repo = StubWriter()
    objective = Objective(
        tenant_id="tenant-a",
        objective_id="obj-1",
        title="Aumentar previsibilidade",
        evidence_refs=("ev-objective",),
    )

    repo.upsert_objective(objective, authorization_ref="elo-authz:req-1")

    table, payload, conflict = repo.posts[0]
    assert table == "elo_strategic_objectives"
    assert conflict == "tenant_id,objective_id"
    assert payload["tenant_id"] == "tenant-a"
    assert payload["evidence_refs"] == ["ev-objective"]


def test_key_result_writer_reuses_metric_identity_without_touching_kpi_owner() -> None:
    repo = StubWriter()
    key_result = KeyResult(
        tenant_id="tenant-a",
        key_result_id="kr-1",
        objective_id="obj-1",
        title="Elevar aderência",
        metric_code="KPI_ADERENCIA",
        direction=KeyResultDirection.INCREASE,
        baseline=Decimal("50"),
        target=Decimal("80"),
        baseline_evidence_refs=("ev-baseline",),
        target_evidence_refs=("ev-target",),
        target_approval_state=TargetApprovalState.APPROVED,
        target_approval_ref="approval-1",
    )

    repo.upsert_key_result(key_result, authorization_ref="elo-authz:req-2")

    table, payload, conflict = repo.posts[0]
    assert table == "elo_strategic_key_results"
    assert conflict == "tenant_id,key_result_id"
    assert payload["metric_code"] == "KPI_ADERENCIA"
    assert all(post[0] not in {"mt_definicoes_kpi", "mt_snapshots_kpi"} for post in repo.posts)


def test_binding_writer_only_writes_attribution_owner() -> None:
    repo = StubWriter()
    binding = SnapshotBindingWrite(
        tenant_id="tenant-a",
        key_result_id="kr-1",
        snapshot_id="11111111-1111-1111-1111-111111111111",
        evidence_refs=("ev-binding",),
    )

    repo.bind_snapshot(binding, authorization_ref="elo-authz:req-3")

    table, payload, conflict = repo.posts[0]
    assert table == "elo_strategic_kr_snapshot_bindings"
    assert conflict == "tenant_id,key_result_id,snapshot_id"
    assert payload == {
        "tenant_id": "tenant-a",
        "key_result_id": "kr-1",
        "snapshot_id": "11111111-1111-1111-1111-111111111111",
        "evidence_refs": ["ev-binding"],
    }


def test_adapter_rejects_blank_authorization_reference_before_transport() -> None:
    repo = StubWriter()
    objective = Objective(
        tenant_id="tenant-a",
        objective_id="obj-1",
        title="Aumentar previsibilidade",
        evidence_refs=("ev-objective",),
    )

    try:
        repo.upsert_objective(objective, authorization_ref=" ")
    except ValueError as exc:
        assert "authorization_ref" in str(exc)
    else:
        raise AssertionError("blank authorization_ref must fail")

    assert repo.posts == []
