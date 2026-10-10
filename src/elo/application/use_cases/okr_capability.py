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

from dataclasses import dataclass, replace
from typing import Mapping

from elo.application.queries.okr import OkrQueryService
from elo.application.queries.okr_evidence import OkrEvidenceResolver
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
        evidence: OkrEvidenceResolver | None = None,
        evaluator: OkrEvaluationService | None = None,
        composer: OrchestrationResponseComposer | None = None,
    ) -> None:
        self._queries = queries
        self._metrics = metrics
        self._evidence = evidence
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
        verified_refs: list[str] = []
        evidence_states: list[str] = []

        objective_state, objective_verified = self._resolve_refs(
            tenant_id=request.tenant_id,
            evidence_refs=context.objective.evidence_refs,
        )
        evidence_states.append(objective_state)
        verified_refs.extend(objective_verified)

        for kr in context.key_results:
            kr_context = self._queries.key_result_context(
                tenant_id=request.tenant_id,
                key_result_id=kr.key_result_id,
            )
            if kr_context is None:
                continue
            metric_state = self._metrics.resolve(kr_context)
            metric_states[kr.key_result_id] = metric_state
            raw_refs = tuple(
                dict.fromkeys(
                    [
                        *kr.baseline_evidence_refs,
                        *kr.target_evidence_refs,
                        *metric_state.current_evidence_refs,
                    ]
                )
            )
            evidence_state, kr_verified = self._resolve_refs(
                tenant_id=request.tenant_id,
                evidence_refs=raw_refs,
            )
            evidence_states.append(evidence_state)
            verified_refs.extend(kr_verified)
            evaluations[kr.key_result_id] = self._evaluator.evaluate_key_result(
                context=kr_context,
                metric_state=metric_state,
                evidence_state=evidence_state,
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
        response = replace(
            response,
            evidence_state=self._aggregate_evidence_state(tuple(evidence_states)),
            evidence_refs=tuple(dict.fromkeys(verified_refs)),
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

    def _resolve_refs(self, *, tenant_id: str, evidence_refs: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
        if not evidence_refs:
            return "SEM_DADO", ()
        if self._evidence is None:
            return "NAO_COMPROVADO", ()
        state = self._evidence.resolve_refs(tenant_id=tenant_id, evidence_refs=evidence_refs)
        return state.state, tuple(item.evidence_id for item in state.evidence)

    @staticmethod
    def _aggregate_evidence_state(states: tuple[str, ...]) -> str:
        relevant = tuple(state for state in states if state != "SEM_DADO")
        if not relevant:
            return "INSUFFICIENT"
        if all(state == "COMPROVADO" for state in relevant):
            return "OBSERVED"
        if any(state in {"COMPROVADO", "PARCIAL"} for state in relevant):
            return "PARTIAL"
        return "INSUFFICIENT"


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
