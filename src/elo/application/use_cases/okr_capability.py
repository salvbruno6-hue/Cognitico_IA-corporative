"""Strategic OKR application capability consumed by GovernedOrchestrator.

Layer: cognitive
Owner: strategic-objective-domain
Status: implemented
Authority: implementation
Related: GovernedOrchestrator, CapabilityRegistry, OkrQueryService,
         OkrMetricResolver, OkrEvaluationService, OrchestrationResponseComposer

This is a domain/application capability, not an orchestrator. It composes the
existing OKR-domain owners and returns already-evaluated facts for the canonical
orchestration response boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from elo.application.queries.okr import OkrQueryService
from elo.application.queries.okr_metric import KeyResultMetricState, OkrMetricResolver
from elo.cognitive.response.intelligent_orchestration_response import (
    IntelligentOrchestrationResponse,
    OrchestrationResponseComposer,
)
from elo.core.capability_registry import CapabilityProbe
from elo.core.okr_evaluation import KeyResultEvaluation, OkrEvaluationService


CAPABILITY_NAME = "strategic_okr"
CAPABILITY_KIND = "domain"


@dataclass(frozen=True, slots=True)
class OkrCapabilitySnapshot:
    objective_id: str
    metric_states: Mapping[str, KeyResultMetricState]
    evaluations: Mapping[str, KeyResultEvaluation]
    objective_health: str


class StrategicOkrCapability:
    """Read-only strategic capability under the canonical orchestrator."""

    def __init__(
        self,
        *,
        queries: OkrQueryService,
        metrics: OkrMetricResolver,
        evaluator: OkrEvaluationService | None = None,
        composer: OrchestrationResponseComposer | None = None,
    ) -> None:
        self._queries = queries
        self._metrics = metrics
        self._evaluator = evaluator or OkrEvaluationService()
        self._composer = composer or OrchestrationResponseComposer()

    def consult_objective(
        self,
        *,
        request,
        objective_id: str,
    ) -> tuple[OkrCapabilitySnapshot, IntelligentOrchestrationResponse] | None:
        context = self._queries.objective_context(
            tenant_id=request.tenant_id,
            objective_id=objective_id,
        )
        if context is None:
            return None

        metric_states: dict[str, KeyResultMetricState] = {}
        evaluations: dict[str, KeyResultEvaluation] = {}
        for kr in context.key_results:
            kr_context = self._queries.key_result_context(
                tenant_id=request.tenant_id,
                key_result_id=kr.key_result_id,
            )
            if kr_context is None:
                continue
            metric_state = self._metrics.resolve(kr_context)
            metric_states[kr.key_result_id] = metric_state
            evaluations[kr.key_result_id] = self._evaluator.evaluate_key_result(
                context=kr_context,
                metric_state=metric_state,
            )

        objective_evaluation = self._evaluator.evaluate_objective(
            objective=context,
            evaluations=tuple(evaluations.values()),
        )
        response = self._composer.compose_okr(
            request=request,
            objective=context,
            metric_states=metric_states,
            evaluations=evaluations,
            objective_evaluation=objective_evaluation,
        )
        return (
            OkrCapabilitySnapshot(
                objective_id=context.objective.objective_id,
                metric_states=metric_states,
                evaluations=evaluations,
                objective_health=objective_evaluation.health,
            ),
            response,
        )


def build_okr_capability_probe(*, health_check=None) -> CapabilityProbe:
    """Register only the OKR capability actually implemented on this branch."""

    return CapabilityProbe(
        kind=CAPABILITY_KIND,
        name=CAPABILITY_NAME,
        version="1",
        health_check=health_check,
        metadata={
            "capabilities": ",".join(
                (
                    "objective_context",
                    "key_result_context",
                    "formal_kpi_link",
                    "kr_evaluation",
                    "objective_health",
                    "diagnosis_bridge",
                    "symbiont_observation",
                )
            ),
            "authority": "governed_orchestrator_consumer",
            "read_only": "true",
        },
    )


__all__ = [
    "CAPABILITY_KIND",
    "CAPABILITY_NAME",
    "OkrCapabilitySnapshot",
    "StrategicOkrCapability",
    "build_okr_capability_probe",
]
