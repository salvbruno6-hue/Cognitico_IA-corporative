"""Evidence-bounded OKR evaluation primitives for the ELO strategic domain.

Layer: cognitive
Owner: strategic-objective-domain
Status: implemented
Authority: implementation
Related: elo.contracts.okr, OkrMetricResolver, GovernedOrchestrator

This module owns only deterministic OKR-domain evaluation semantics. It does
not orchestrate, authorize, persist, execute actions, define KPIs, or promote
learning. In particular:

progress != trend != forecast != status

No status is inferred from progress alone. Objective health remains
``INDETERMINADO`` unless a separately supplied governed policy evaluates it.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Protocol, Sequence

from elo.application.queries.okr import KeyResultContext, ObjectiveContext
from elo.application.queries.okr_metric import KeyResultMetricState
from elo.contracts.okr import KeyResultDirection, TargetApprovalState


class ValueTrend(StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    STABLE = "STABLE"
    SEM_DADO = "SEM_DADO"


@dataclass(frozen=True, slots=True)
class KeyResultEvaluation:
    key_result_id: str
    baseline: Decimal | None
    target: Decimal | None
    current: Decimal | None
    progress_pct: Decimal | None
    trend: ValueTrend
    forecast: Decimal | None
    deviation: Decimal | None
    status: str
    confidence: str
    evidence_refs: tuple[str, ...]
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ObjectiveEvaluation:
    objective_id: str
    health: str
    evaluated_key_results: int
    indeterminate_key_results: int
    evidence_refs: tuple[str, ...]
    rationale: str


class ObjectiveHealthPolicy(Protocol):
    """Optional governed policy; the evaluator never invents one."""

    def evaluate(
        self,
        *,
        objective: ObjectiveContext,
        key_results: Sequence[KeyResultEvaluation],
    ) -> tuple[str, str]: ...


class OkrEvaluationService:
    """Calculate bounded KR facts while leaving status/health policy explicit."""

    def evaluate_key_result(
        self,
        *,
        context: KeyResultContext,
        metric_state: KeyResultMetricState,
    ) -> KeyResultEvaluation:
        kr = context.key_result
        current = metric_state.current
        baseline = kr.baseline
        target = kr.approved_target
        limitations: list[str] = []

        if kr.target is not None and kr.target_approval_state is not TargetApprovalState.APPROVED:
            limitations.append("TARGET_NAO_APROVADO")
        if baseline is None:
            limitations.append("SEM_BASELINE")
        if target is None:
            limitations.append("SEM_TARGET_APROVADO")
        if current is None:
            limitations.append("SEM_MEDICAO_ATUAL")
        if metric_state.kpi is None:
            limitations.append("SEM_KPI_FORMAL_REGISTRADO")

        progress = self._progress(
            direction=kr.direction,
            baseline=baseline,
            target=target,
            current=current,
        )
        if progress is None and all(value is not None for value in (baseline, target, current)):
            limitations.append("PROGRESSO_NAO_CALCULAVEL")

        trend = self._trend(context)
        deviation = (current - target) if current is not None and target is not None else None

        evidence_refs = tuple(
            dict.fromkeys(
                [
                    *kr.baseline_evidence_refs,
                    *kr.target_evidence_refs,
                    *metric_state.current_evidence_refs,
                ]
            )
        )
        confidence = "OBSERVED" if not limitations and evidence_refs else "PARCIAL" if evidence_refs else "SEM_DADO"

        return KeyResultEvaluation(
            key_result_id=kr.key_result_id,
            baseline=baseline,
            target=target,
            current=current,
            progress_pct=progress,
            trend=trend,
            forecast=None,
            deviation=deviation,
            status="INDETERMINADO",
            confidence=confidence,
            evidence_refs=evidence_refs,
            limitations=tuple(dict.fromkeys(limitations)),
        )

    def evaluate_objective(
        self,
        *,
        objective: ObjectiveContext,
        evaluations: Sequence[KeyResultEvaluation],
        policy: ObjectiveHealthPolicy | None = None,
    ) -> ObjectiveEvaluation:
        expected_ids = {item.key_result_id for item in objective.key_results}
        observed_ids = {item.key_result_id for item in evaluations}
        if observed_ids - expected_ids:
            raise ValueError("Objective evaluation contains unrelated KeyResults")

        evidence_refs = tuple(
            dict.fromkeys(
                ref
                for item in evaluations
                for ref in item.evidence_refs
            )
        )
        indeterminate = sum(1 for item in evaluations if item.status == "INDETERMINADO")

        if policy is None:
            return ObjectiveEvaluation(
                objective_id=objective.objective.objective_id,
                health="INDETERMINADO",
                evaluated_key_results=len(evaluations),
                indeterminate_key_results=indeterminate,
                evidence_refs=evidence_refs,
                rationale=(
                    "Objective Health exige política governada; não é derivado por média simples "
                    "nem por percentual de progresso isolado."
                ),
            )

        health, rationale = policy.evaluate(objective=objective, key_results=evaluations)
        if not health.strip() or not rationale.strip():
            raise ValueError("ObjectiveHealthPolicy must return health and rationale")
        return ObjectiveEvaluation(
            objective_id=objective.objective.objective_id,
            health=health.strip(),
            evaluated_key_results=len(evaluations),
            indeterminate_key_results=indeterminate,
            evidence_refs=evidence_refs,
            rationale=rationale.strip(),
        )

    @staticmethod
    def _progress(
        *,
        direction: KeyResultDirection,
        baseline: Decimal | None,
        target: Decimal | None,
        current: Decimal | None,
    ) -> Decimal | None:
        if baseline is None or target is None or current is None:
            return None
        if direction is KeyResultDirection.MAINTAIN:
            return None
        denominator = (
            target - baseline
            if direction is KeyResultDirection.INCREASE
            else baseline - target
        )
        if denominator == 0:
            return None
        numerator = (
            current - baseline
            if direction is KeyResultDirection.INCREASE
            else baseline - current
        )
        return (numerator / denominator) * Decimal("100")

    @staticmethod
    def _trend(context: KeyResultContext) -> ValueTrend:
        ordered = sorted(context.measurements, key=lambda item: item.measured_at)
        if len(ordered) < 2:
            return ValueTrend.SEM_DADO
        previous, latest = ordered[-2], ordered[-1]
        if latest.value > previous.value:
            return ValueTrend.UP
        if latest.value < previous.value:
            return ValueTrend.DOWN
        return ValueTrend.STABLE


__all__ = [
    "KeyResultEvaluation",
    "ObjectiveEvaluation",
    "ObjectiveHealthPolicy",
    "OkrEvaluationService",
    "ValueTrend",
]
