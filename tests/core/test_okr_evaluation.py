from datetime import datetime, timedelta, timezone
from decimal import Decimal

from elo.application.queries.okr import KeyResultContext, ObjectiveContext
from elo.application.queries.okr_metric import FormalKpiLink, KeyResultMetricState
from elo.contracts.okr import (
    KeyResult,
    KeyResultDirection,
    Measurement,
    Objective,
    TargetApprovalState,
)
from elo.core.okr_evaluation import OkrEvaluationService, ValueTrend


def _measurement(mid: str, value: str, when: datetime):
    return Measurement(
        tenant_id="tenant-a",
        measurement_id=mid,
        key_result_id="KR-1",
        metric_code="KPI-LEAD-TIME",
        value=Decimal(value),
        measured_at=when,
        evidence_refs=(f"ev:{mid}",),
        source_ref=f"mt_snapshots_kpi:{mid}",
    )


def _kr(*, approved=True, direction=KeyResultDirection.DECREASE):
    return KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce lead time",
        metric_code="KPI-LEAD-TIME",
        direction=direction,
        baseline=Decimal("15"),
        target=Decimal("10"),
        baseline_evidence_refs=("ev:baseline",),
        target_evidence_refs=("ev:target",),
        target_approval_state=(TargetApprovalState.APPROVED if approved else TargetApprovalState.DRAFT),
        target_approval_ref=("approval:1" if approved else None),
    )


def _metric_state(current: Decimal | None, evidence_refs=()):
    return KeyResultMetricState(
        key_result_id="KR-1",
        metric_state="KPI_FORMAL_COM_MEDICAO" if current is not None else "KPI_FORMAL_SEM_MEDICAO",
        kpi=FormalKpiLink(
            metric_code="KPI-LEAD-TIME",
            name="Lead Time",
            unit="dias",
            formula="data_fim-data_inicio",
        ),
        current=current,
        current_measurement_id="M-2" if current is not None else None,
        current_evidence_refs=tuple(evidence_refs),
    )


def test_progress_trend_deviation_and_status_remain_separate():
    now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
    older = _measurement("M-1", "14", now - timedelta(days=7))
    latest = _measurement("M-2", "12", now)
    service = OkrEvaluationService()

    result = service.evaluate_key_result(
        context=KeyResultContext(key_result=_kr(), measurements=(older, latest)),
        metric_state=_metric_state(Decimal("12"), ("ev:M-2",)),
    )

    assert result.progress_pct == Decimal("60")
    assert result.trend is ValueTrend.DOWN
    assert result.deviation == Decimal("2")
    assert result.forecast is None
    assert result.status == "INDETERMINADO"


def test_draft_target_is_not_used_for_progress_or_deviation():
    service = OkrEvaluationService()

    result = service.evaluate_key_result(
        context=KeyResultContext(key_result=_kr(approved=False), measurements=()),
        metric_state=_metric_state(Decimal("12"), ("ev:M-2",)),
    )

    assert result.target is None
    assert result.progress_pct is None
    assert result.deviation is None
    assert "TARGET_NAO_APROVADO" in result.limitations
    assert result.status == "INDETERMINADO"


def test_missing_current_never_becomes_zero_progress():
    service = OkrEvaluationService()

    result = service.evaluate_key_result(
        context=KeyResultContext(key_result=_kr(), measurements=()),
        metric_state=_metric_state(None),
    )

    assert result.current is None
    assert result.progress_pct is None
    assert "SEM_MEDICAO_ATUAL" in result.limitations


def test_maintain_direction_requires_explicit_progress_policy():
    service = OkrEvaluationService()

    result = service.evaluate_key_result(
        context=KeyResultContext(key_result=_kr(direction=KeyResultDirection.MAINTAIN), measurements=()),
        metric_state=_metric_state(Decimal("12"), ("ev:M-2",)),
    )

    assert result.progress_pct is None
    assert "PROGRESSO_NAO_CALCULAVEL" in result.limitations


def test_objective_health_is_indeterminate_without_governed_policy():
    objective = Objective(
        tenant_id="tenant-a",
        objective_id="OBJ-1",
        title="Improve operational reliability",
        key_result_ids=("KR-1",),
    )
    service = OkrEvaluationService()
    kr_eval = service.evaluate_key_result(
        context=KeyResultContext(key_result=_kr(), measurements=()),
        metric_state=_metric_state(None),
    )

    result = service.evaluate_objective(
        objective=ObjectiveContext(objective=objective, key_results=(_kr(),)),
        evaluations=(kr_eval,),
    )

    assert result.health == "INDETERMINADO"
    assert "não é derivado por média simples" in result.rationale
