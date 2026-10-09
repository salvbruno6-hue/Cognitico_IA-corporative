from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace

from elo.application.queries.okr import OkrQueryService
from elo.application.queries.okr_metric import OkrMetricResolver
from elo.application.use_cases.okr_capability import (
    StrategicOkrCapability,
    build_okr_capability_probe,
)
from elo.cognitive.reasoning.capability_selection import CapabilityRequirement, CapabilitySelector
from elo.contracts.okr import (
    KeyResult,
    KeyResultDirection,
    Measurement,
    Objective,
    TargetApprovalState,
)
from elo.core.capability_registry import CapabilityRegistry


class FakeOkrRepository:
    def __init__(self, objective, kr, measurement):
        self.objective = objective
        self.kr = kr
        self.measurement = measurement

    def get_objective(self, *, tenant_id: str, objective_id: str):
        return self.objective if objective_id == self.objective.objective_id else None

    def get_key_result(self, *, tenant_id: str, key_result_id: str):
        return self.kr if key_result_id == self.kr.key_result_id else None

    def list_key_results(self, *, tenant_id: str, objective_id: str):
        return (self.kr,) if objective_id == self.objective.objective_id else ()

    def list_measurements(self, *, tenant_id: str, key_result_id: str):
        return (self.measurement,) if key_result_id == self.kr.key_result_id else ()


class FakeFormalKpiRegistry:
    def get_definition(self, *, metric_code: str):
        if metric_code != "KPI-LEAD-TIME":
            return None
        return {
            "codigo_kpi": "KPI-LEAD-TIME",
            "nome": "Lead Time",
            "unidade": "dias",
            "formula": "data_fim-data_inicio",
            "ativo": True,
        }


def _fixture():
    objective = Objective(
        tenant_id="tenant-a",
        objective_id="OBJ-1",
        title="Improve delivery reliability",
        key_result_ids=("KR-1",),
        evidence_refs=("ev:objective",),
    )
    kr = KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce lead time",
        metric_code="KPI-LEAD-TIME",
        direction=KeyResultDirection.DECREASE,
        baseline=Decimal("15"),
        target=Decimal("10"),
        baseline_evidence_refs=("ev:baseline",),
        target_evidence_refs=("ev:target",),
        target_approval_state=TargetApprovalState.APPROVED,
        target_approval_ref="approval:human:1",
    )
    measurement = Measurement(
        tenant_id="tenant-a",
        measurement_id="M-1",
        key_result_id="KR-1",
        metric_code="KPI-LEAD-TIME",
        value=Decimal("12"),
        measured_at=datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc),
        evidence_refs=("ev:current",),
        source_ref="mt_snapshots_kpi:M-1",
    )
    return objective, kr, measurement


def test_existing_capability_registry_can_select_strategic_okr():
    registry = CapabilityRegistry((build_okr_capability_probe(health_check=lambda: True),))
    selector = CapabilitySelector(registry)

    selected = selector.select(
        CapabilityRequirement(
            capability="objective_context",
            preferred_kinds=("domain",),
            min_score=0.3,
        )
    )

    assert selected.status == "SELECTED"
    assert selected.capability_name == "strategic_okr"
    assert selected.capability_kind == "domain"


def test_strategic_okr_capability_serves_orchestrator_with_evaluated_read_model():
    objective, kr, measurement = _fixture()
    capability = StrategicOkrCapability(
        queries=OkrQueryService(FakeOkrRepository(objective, kr, measurement)),
        metrics=OkrMetricResolver(FakeFormalKpiRegistry()),
    )

    result = capability.consult_objective(
        request=SimpleNamespace(tenant_id="tenant-a", correlation_id="corr-1"),
        objective_id="OBJ-1",
    )

    assert result is not None
    snapshot, response = result
    assert snapshot.objective_id == "OBJ-1"
    assert snapshot.evaluations["KR-1"].progress_pct == Decimal("60")
    assert snapshot.objective_health == "INDETERMINADO"
    assert response.capability == "strategic_okr"
    assert "Status: INDETERMINADO" in response.response


def test_capability_returns_none_for_unknown_objective_without_inventing_state():
    objective, kr, measurement = _fixture()
    capability = StrategicOkrCapability(
        queries=OkrQueryService(FakeOkrRepository(objective, kr, measurement)),
        metrics=OkrMetricResolver(FakeFormalKpiRegistry()),
    )

    result = capability.consult_objective(
        request=SimpleNamespace(tenant_id="tenant-a", correlation_id="corr-1"),
        objective_id="OBJ-404",
    )

    assert result is None
