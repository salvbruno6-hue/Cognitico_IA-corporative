"""Canonical laboratory handoff for EVOLUÇÃO_DE_CAPACIDADES.

The evolution review remains read-only. This module only translates an
explicitly selected review action and explicitly supplied experiment evidence
into the existing SymbiontLabObservation contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.symbionte_lab import SymbiontLabObservation
from .symbiont_capability_evolution import CapabilityEvolutionReview


@dataclass(frozen=True, slots=True)
class CapabilityExperimentHandoff:
    observation: SymbiontLabObservation
    review: CapabilityEvolutionReview


def prepare_capability_experiment_handoff(
    review: CapabilityEvolutionReview,
    *,
    tenant_id: str,
    decision_id: str,
    observation_id: str,
    source_ref: str,
    source_commit: str,
    item: str,
    hypothesis: str,
    baseline: str,
    experiment: str,
    result: str,
    regression_status: str,
    generalization_status: str,
    risk: str,
    scope: str = "EVOLUÇÃO_DE_CAPACIDADES",
    existing_owner: str | None = None,
) -> CapabilityExperimentHandoff:
    if review.trigger_id != "EVOLUÇÃO_DE_CAPACIDADES":
        raise ValueError("invalid evolution review trigger")
    if not review.evidence_refs:
        raise ValueError("capability experiment requires evidence")
    if not any(metric.item == item for metric in review.metrics):
        raise ValueError("experiment item is not present in review")

    observation = SymbiontLabObservation(
        observation_id=observation_id,
        tenant_id=tenant_id,
        domain="EVOLUÇÃO_DE_CAPACIDADES",
        decision_id=decision_id,
        expected_outcome=f"capability={item}",
        observed_outcome=result,
        evidence_ids=review.evidence_refs,
        source_ref=source_ref,
        source_commit=source_commit,
        hypothesis=hypothesis,
        baseline=baseline,
        experiment=experiment,
        result=result,
        regression_status=regression_status,
        generalization_status=generalization_status,
        risk=risk,
        existing_owner=existing_owner,
        scope=scope,
        tenant_scope=tenant_id,
        source_kind="runtime",
    )
    return CapabilityExperimentHandoff(observation=observation, review=review)
