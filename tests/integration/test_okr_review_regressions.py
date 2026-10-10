from datetime import datetime, timezone
from decimal import Decimal

from elo.application.queries.okr import KeyResultContext, ObjectiveContext
from elo.application.queries.okr_metric import FormalKpiLink, KeyResultMetricState
from elo.application.use_cases.okr_capability import OkrCapabilitySnapshot, StrategicOkrCapability
from elo.cognitive._core import CognitiveCore
from elo.cognitive.response.intelligent_orchestration_response import IntelligentOrchestrationResponse
from elo.contracts.okr import KeyResult, KeyResultDirection, Measurement, Objective, TargetApprovalState
from elo.core.okr_evaluation import OkrEvaluationService
from elo.interface.contracts import CognitiveRequest


class _Queries:
    def __init__(self, objective: Objective, key_result: KeyResult, measurement: Measurement) -> None:
        self.objective = objective
        self.key_result = key_result
        self.measurement = measurement

    def objective_context(self, *, tenant_id: str, objective_id: str):
        assert tenant_id == self.objective.tenant_id
        if objective_id != self.objective.objective_id:
            return None
        return ObjectiveContext(objective=self.objective, key_results=(self.key_result,))

    def key_result_context(self, *, tenant_id: str, key_result_id: str):
        assert tenant_id == self.key_result.tenant_id
        if key_result_id != self.key_result.key_result_id:
            return None
        return KeyResultContext(key_result=self.key_result, measurements=(self.measurement,))


class _Metrics:
    def __init__(self, key_result: KeyResult, measurement: Measurement) -> None:
        self.key_result = key_result
        self.measurement = measurement

    def resolve(self, context: KeyResultContext) -> KeyResultMetricState:
        return KeyResultMetricState(
            key_result_id=self.key_result.key_result_id,
            metric_state="KPI_FORMAL_COM_MEDICAO",
            kpi=FormalKpiLink(
                metric_code=self.key_result.metric_code,
                name="Indicador",
                unit="%",
                formula="observado",
            ),
            current=self.measurement.value,
            current_measurement_id=self.measurement.measurement_id,
            current_evidence_refs=self.measurement.evidence_refs,
        )


class _RuntimeCapability:
    def consult_objective(self, *, request, objective_id: str):
        assert objective_id == "OBJ-1"
        assert request.tenant_id == "MULTITEINER"
        return (
            OkrCapabilitySnapshot(
                objective_id="OBJ-1",
                metric_states={},
                evaluations={},
                objective_health="INDETERMINADO",
            ),
            IntelligentOrchestrationResponse(
                status="CONSULTED",
                stage="ANALYZE",
                headline="OKR",
                response="consulta OKR governada",
                capability="strategic_okr",
                provider=None,
                model=None,
                execution_id=None,
                correlation_id=request.correlation_id,
                evidence_state="INSUFFICIENT",
                next_action="obter evidência",
                evidence_refs=(),
            ),
        )


def _domain_objects():
    objective = Objective(
        tenant_id="MULTITEINER",
        objective_id="OBJ-1",
        title="Objetivo",
        evidence_refs=("ev-objective-missing",),
    )
    key_result = KeyResult(
        tenant_id="MULTITEINER",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="KR",
        metric_code="KPI-1",
        direction=KeyResultDirection.INCREASE,
        baseline=Decimal("10"),
        target=Decimal("20"),
        target_approval_state=TargetApprovalState.APPROVED,
        target_approval_ref="approval:1",
        baseline_evidence_refs=("ev-baseline-missing",),
        target_evidence_refs=("ev-target-missing",),
    )
    measurement = Measurement(
        tenant_id="MULTITEINER",
        measurement_id="M-1",
        key_result_id="KR-1",
        metric_code="KPI-1",
        value=Decimal("15"),
        measured_at=datetime(2026, 10, 9, tzinfo=timezone.utc),
        evidence_refs=("ev-current-missing",),
        source_ref="snapshot:1",
    )
    return objective, key_result, measurement


def test_cognitive_core_routes_explicit_okr_objective_through_production_registry() -> None:
    core = CognitiveCore(strategic_okr_capability=_RuntimeCapability())
    result = core.process(
        CognitiveRequest(
            tenant_id="MULTITEINER",
            user_id="operator-1",
            message="Como está o objetivo?",
            domain="strategic",
            context={"okr_objective_id": "OBJ-1"},
        )
    )

    assert result["response"]["type"] == "strategic_okr"
    assert result["okr"]["capability"] == "strategic_okr"
    assert result["provenance"]["provider"] == "governed_orchestrator:strategic_okr"


def test_unresolved_evidence_refs_never_become_observed() -> None:
    objective, key_result, measurement = _domain_objects()
    capability = StrategicOkrCapability(
        queries=_Queries(objective, key_result, measurement),
        metrics=_Metrics(key_result, measurement),
        evidence=None,
    )
    request = type(
        "Request",
        (),
        {"tenant_id": "MULTITEINER", "correlation_id": "corr-1"},
    )()

    snapshot, response = capability.consult_objective(request=request, objective_id="OBJ-1")

    assert response.evidence_state == "INSUFFICIENT"
    assert response.evidence_refs == ()
    assert snapshot.evaluations["KR-1"].confidence == "SEM_DADO"
    assert "EVIDENCIA_NAO_COMPROVADA" in snapshot.evaluations["KR-1"].limitations


def test_increase_target_below_baseline_is_not_calculable() -> None:
    assert OkrEvaluationService._progress(
        direction=KeyResultDirection.INCREASE,
        baseline=Decimal("100"),
        target=Decimal("50"),
        current=Decimal("75"),
    ) is None


def test_decrease_target_above_baseline_is_not_calculable() -> None:
    assert OkrEvaluationService._progress(
        direction=KeyResultDirection.DECREASE,
        baseline=Decimal("50"),
        target=Decimal("100"),
        current=Decimal("75"),
    ) is None
