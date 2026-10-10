from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from elo.application.queries.okr import ObjectiveContext
from elo.application.queries.okr_metric import FormalKpiLink, KeyResultMetricState
from elo.cognitive.response.intelligent_orchestration_response import OrchestrationResponseComposer
from elo.contracts.okr import KeyResult, KeyResultDirection, Objective, TargetApprovalState
from elo.core.okr_evaluation import KeyResultEvaluation, ObjectiveEvaluation, ValueTrend


def _kr():
    return KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce lead time",
        metric_code="KPI-LEAD-TIME",
        direction=KeyResultDirection.DECREASE,
        baseline=Decimal("15"),
        target=Decimal("10"),
        deadline=date(2026, 12, 31),
        baseline_evidence_refs=("ev:baseline",),
        target_evidence_refs=("ev:target",),
        target_approval_state=TargetApprovalState.APPROVED,
        target_approval_ref="approval:human:1",
    )


def test_compose_okr_uses_existing_composer_and_preserves_independent_dimensions():
    objective = Objective(
        tenant_id="tenant-a",
        objective_id="OBJ-1",
        title="Improve delivery reliability",
        key_result_ids=("KR-1",),
        evidence_refs=("ev:objective",),
    )
    kr = _kr()
    metric_state = KeyResultMetricState(
        key_result_id="KR-1",
        metric_state="KPI_FORMAL_COM_MEDICAO",
        kpi=FormalKpiLink(
            metric_code="KPI-LEAD-TIME",
            name="Lead Time",
            unit="dias",
            formula="data_fim-data_inicio",
        ),
        current=Decimal("12"),
        current_measurement_id="M-2",
        current_evidence_refs=("ev:current",),
    )
    evaluation = KeyResultEvaluation(
        key_result_id="KR-1",
        baseline=Decimal("15"),
        target=Decimal("10"),
        current=Decimal("12"),
        progress_pct=Decimal("60"),
        trend=ValueTrend.DOWN,
        forecast=None,
        deviation=Decimal("2"),
        status="INDETERMINADO",
        confidence="OBSERVED",
        evidence_refs=("ev:baseline", "ev:target", "ev:current"),
    )
    objective_eval = ObjectiveEvaluation(
        objective_id="OBJ-1",
        health="INDETERMINADO",
        evaluated_key_results=1,
        indeterminate_key_results=1,
        evidence_refs=("ev:current",),
        rationale="Objective Health exige política governada.",
    )

    result = OrchestrationResponseComposer().compose_okr(
        request=SimpleNamespace(correlation_id="corr-1"),
        objective=ObjectiveContext(objective=objective, key_results=(kr,)),
        metric_states={"KR-1": metric_state},
        evaluations={"KR-1": evaluation},
        objective_evaluation=objective_eval,
    )

    assert result.capability == "strategic_okr"
    assert result.stage == "ANALYZE"
    assert "Progress: 60%" in result.response
    assert "Trend: DOWN" in result.response
    assert "Forecast: [SEM_DADO]" in result.response
    assert "Status: INDETERMINADO" in result.response
    assert "Progress, trend, forecast, deviation e status permanecem dimensões distintas" in result.response
    assert set(result.evidence_refs) == {"ev:objective", "ev:baseline", "ev:target", "ev:current"}


def test_compose_okr_does_not_render_missing_values_as_zero():
    objective = Objective(
        tenant_id="tenant-a",
        objective_id="OBJ-1",
        title="Improve delivery reliability",
        key_result_ids=("KR-1",),
    )
    kr = KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce lead time",
        metric_code="KPI-LEAD-TIME",
        direction=KeyResultDirection.DECREASE,
    )
    evaluation = KeyResultEvaluation(
        key_result_id="KR-1",
        baseline=None,
        target=None,
        current=None,
        progress_pct=None,
        trend=ValueTrend.SEM_DADO,
        forecast=None,
        deviation=None,
        status="INDETERMINADO",
        confidence="SEM_DADO",
        evidence_refs=(),
        limitations=("SEM_BASELINE", "SEM_TARGET_APROVADO", "SEM_MEDICAO_ATUAL"),
    )
    objective_eval = ObjectiveEvaluation(
        objective_id="OBJ-1",
        health="INDETERMINADO",
        evaluated_key_results=1,
        indeterminate_key_results=1,
        evidence_refs=(),
        rationale="Sem política e sem evidência suficiente.",
    )

    result = OrchestrationResponseComposer().compose_okr(
        request=SimpleNamespace(correlation_id="corr-2"),
        objective=ObjectiveContext(objective=objective, key_results=(kr,)),
        metric_states={},
        evaluations={"KR-1": evaluation},
        objective_evaluation=objective_eval,
    )

    assert "Baseline: [SEM_DADO]" in result.response
    assert "Current: [SEM_DADO]" in result.response
    assert "Progress: [SEM_DADO]" in result.response
    assert result.evidence_state == "INSUFFICIENT"
