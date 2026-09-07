"""Executable bridge from laboratory observations into governed learning.

This adapter is intentionally thin: the laboratory remains candidate-only,
while GovernedLearningService and EvolutionGate remain the canonical
learning/promotion authorities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from elo.core.evolution_gate import EvolutionGate, EvolutionProposal
from elo.core.learning_governance import (
    ExperienceRecord,
    GovernedLearningService,
    LearningCandidate,
)


LAB_ONLY = "LAB_ONLY"


@dataclass(frozen=True)
class SymbiontLabObservation:
    observation_id: str
    tenant_id: str
    domain: str
    decision_id: str
    expected_outcome: str
    observed_outcome: str
    evidence_ids: tuple[str, ...]
    source_ref: str
    source_commit: str
    hypothesis: str
    baseline: str
    experiment: str
    result: str
    regression_status: str
    generalization_status: str
    risk: str
    existing_owner: str | None
    scope: str


@dataclass(frozen=True)
class SymbiontLabEvaluation:
    observation: SymbiontLabObservation
    experience: ExperienceRecord
    candidate: LearningCandidate
    evolution_classification: str
    disposition: str
    state: str = LAB_ONLY


class SymbiontLabAdapter:
    """Bridge laboratory observations to existing governed learning APIs."""

    def __init__(self, learning: GovernedLearningService) -> None:
        self.learning = learning

    def evaluate(
        self,
        observation: SymbiontLabObservation,
        *,
        principal_id: str,
        dataset_version: str,
    ) -> SymbiontLabEvaluation:
        self._validate(observation)

        experience = self.learning.capture_outcome(
            tenant_id=observation.tenant_id,
            domain=observation.domain,
            principal_id=principal_id,
            decision_id=observation.decision_id,
            expected_outcome=observation.expected_outcome,
            observed_outcome=observation.observed_outcome,
            evidence_ids=observation.evidence_ids,
        )
        candidate = self.learning.propose_candidate(
            experience,
            dataset_version=dataset_version,
            hypothesis=observation.hypothesis,
        )

        proposal = EvolutionProposal(
            proposal_id=observation.observation_id,
            tenant_id=observation.tenant_id,
            source_id=observation.source_ref,
            summary=observation.hypothesis,
            purpose_alignment=True,
            identity_compatible=True,
            architecture_compatible=True,
            governance_compatible=True,
            evidence_ids=observation.evidence_ids,
            maturity_score=self._maturity_score(observation),
            existing_owner=observation.existing_owner,
            provenance={
                "source_ref": observation.source_ref,
                "source_commit": observation.source_commit,
                "tenant_scope": observation.tenant_id,
                "scope": observation.scope,
            },
        )
        decision = EvolutionGate().evaluate(proposal)

        disposition = "HOLD"
        if decision.existing_owner is False if hasattr(decision, "existing_owner") else False:
            disposition = "HOLD"
        if decision.classification.value == "DUPLICATE/SUPERSEDED":
            disposition = "REUSE"
        elif decision.classification.value == "COMPATIBLE":
            disposition = "CANDIDATE_FOR_GOVERNED_LEARNING"
        elif decision.classification.value == "ADAPT_REQUIRED":
            disposition = "STRENGTHEN"
        elif decision.classification.value in {"EVOLUTIONARY_CONFLICT", "INCOMPATIBLE"}:
            disposition = "BLOCK"

        return SymbiontLabEvaluation(
            observation=observation,
            experience=experience,
            candidate=candidate,
            evolution_classification=decision.classification.value,
            disposition=disposition,
            state=LAB_ONLY,
        )

    @staticmethod
    def _validate(observation: SymbiontLabObservation) -> None:
        required = (
            observation.observation_id,
            observation.tenant_id,
            observation.domain,
            observation.decision_id,
            observation.source_ref,
            observation.source_commit,
            observation.hypothesis,
            observation.baseline,
            observation.experiment,
            observation.result,
            observation.scope,
        )
        if not all(required):
            raise ValueError("laboratory observation requires identity, provenance, experiment and scope")
        if not observation.evidence_ids:
            raise ValueError("laboratory observation requires evidence")
        if observation.regression_status == "REGRESSION":
            raise ValueError("regression blocks laboratory evaluation")
        if observation.generalization_status == "UNCONFIRMED":
            raise ValueError("unconfirmed generalization remains LAB_ONLY")

    @staticmethod
    def _maturity_score(observation: SymbiontLabObservation) -> float:
        status = observation.generalization_status.upper()
        risk = observation.risk.upper()
        score = {
            "CONFIRMED": 0.9,
            "PARTIAL": 0.6,
            "UNCONFIRMED": 0.3,
        }.get(status, 0.3)
        if risk in {"HIGH", "CRITICAL", "ALTO", "CRITICO"}:
            score = min(score, 0.4)
        return score
