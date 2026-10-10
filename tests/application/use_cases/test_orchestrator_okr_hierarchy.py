from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace

from elo.application.queries.okr import OkrQueryService
from elo.application.queries.okr_metric import OkrMetricResolver
from elo.application.use_cases.okr_capability import StrategicOkrCapability, build_okr_capability_probe
from elo.application.use_cases.orchestrator import GovernedOrchestrator
from elo.cognitive.reasoning.capability_selection import CapabilityRequirement, CapabilitySelector
from elo.cognitive.symbiont_capability_governance import (
    CapabilityVisibilityRecord,
    CapabilityVisibilityState,
    GlobalCapabilityVisibility,
)
from elo.contracts.okr import KeyResult, KeyResultDirection, Measurement, Objective
from elo.core.capability_registry import CapabilityRegistry


class Repo:
    def __init__(self):
        self.objective = Objective(
            tenant_id="tenant-a",
            objective_id="OBJ-1",
            title="Improve delivery reliability",
            key_result_ids=("KR-1",),
        )
        self.kr = KeyResult(
            tenant_id="tenant-a",
            key_result_id="KR-1",
            objective_id="OBJ-1",
            title="Reduce lead time",
            metric_code="KPI-LEAD-TIME",
            direction=KeyResultDirection.DECREASE,
        )
        self.measurement = Measurement(
            tenant_id="tenant-a",
            measurement_id="M-1",
            key_result_id="KR-1",
            metric_code="KPI-LEAD-TIME",
            value=Decimal("12"),
            measured_at=datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc),
            evidence_refs=("ev:current",),
            source_ref="mt_snapshots_kpi:M-1",
        )

    def get_objective(self, *, tenant_id, objective_id):
        return self.objective if objective_id == "OBJ-1" else None

    def get_key_result(self, *, tenant_id, key_result_id):
        return self.kr if key_result_id == "KR-1" else None

    def list_key_results(self, *, tenant_id, objective_id):
        return (self.kr,) if objective_id == "OBJ-1" else ()

    def list_measurements(self, *, tenant_id, key_result_id):
        return (self.measurement,) if key_result_id == "KR-1" else ()


class KpiRegistry:
    def get_definition(self, *, metric_code):
        return {
            "codigo_kpi": metric_code,
            "nome": "Lead Time",
            "unidade": "dias",
            "formula": "data_fim-data_inicio",
            "ativo": True,
        }


def test_governed_orchestrator_remains_above_strategic_okr_capability():
    registry = CapabilityRegistry((build_okr_capability_probe(health_check=lambda: True),))
    selector = CapabilitySelector(registry)
    selected = selector.select(
        CapabilityRequirement(
            capability="objective_context",
            preferred_kinds=("domain",),
            min_score=0.3,
        )
    )
    assert selected.capability_name == "strategic_okr"

    visibility = GlobalCapabilityVisibility(
        records=(
            CapabilityVisibilityRecord(
                capability_id="strategic_okr",
                registry_visible=True,
                available=True,
                implementation_visible=True,
                owner="strategic-objective-domain",
                runtime_status="OBSERVED",
                evolution_status="CANDIDATE",
                evidence_refs=("ev:capability",),
                state=CapabilityVisibilityState.REGISTERED_VISIBLE,
            ),
        )
    )
    orchestrator = GovernedOrchestrator()
    orientation = orchestrator.advise_capability(visibility, "strategic_okr")

    assert orientation.action == "USE_CANONICAL"
    assert orientation.owner == "strategic-objective-domain"
    assert orientation.authorized is False

    capability = StrategicOkrCapability(
        queries=OkrQueryService(Repo()),
        metrics=OkrMetricResolver(KpiRegistry()),
    )
    result = capability.consult_objective(
        request=SimpleNamespace(tenant_id="tenant-a", correlation_id="corr-1"),
        objective_id="OBJ-1",
    )

    assert result is not None
    _, response = result
    assert response.capability == "strategic_okr"
    assert response.stage == "ANALYZE"
    assert "Status: INDETERMINADO" in response.response


def test_okr_capability_does_not_gain_execution_authority_from_orchestrator_visibility():
    visibility = GlobalCapabilityVisibility(
        records=(
            CapabilityVisibilityRecord(
                capability_id="strategic_okr",
                registry_visible=True,
                available=True,
                implementation_visible=True,
                owner="strategic-objective-domain",
                runtime_status="OBSERVED",
                evolution_status="CANDIDATE",
                evidence_refs=("ev:capability",),
                state=CapabilityVisibilityState.REGISTERED_VISIBLE,
            ),
        )
    )
    orientation = GovernedOrchestrator().advise_capability(
        visibility,
        "strategic_okr",
        authorized_actions=frozenset(),
    )

    assert orientation.action == "USE_CANONICAL"
    assert orientation.authorized is False
