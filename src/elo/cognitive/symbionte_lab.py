"""Executable bridge from laboratory observations into governed learning.

The adapter validates the laboratory evidence boundary before recording any
experience. It preserves the canonical learning and evolution authorities and
never performs promotion itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from elo.core.evolution_gate import EvolutionClassification, EvolutionGate, EvolutionProposal
from elo.core.execution_boundary import ExecutionOutcome, ExecutionStatus
from elo.core.learning_governance import ExperienceRecord, GovernedLearningService, LearningCandidate

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
    tenant_scope: str | None = None
    source_kind: str | None = None

    @classmethod
    def from_execution_outcome(
        cls,
        outcome: ExecutionOutcome,
        *,
        decision_id: str,
        domain: str,
        expected_outcome: str,
        observed_outcome: str,
        hypothesis: str,
        baseline: str,
        experiment: str,
        result: str,
        regression_status: str,
        generalization_status: str,
        risk: str,
        existing_owner: str | None,
        scope: str,
        tenant_id: str,
        observation_id: str,
    ) -> "SymbiontLabObservation":
        """Bind a governed execution result to the existing laboratory contract."""
        if outcome.status is not ExecutionStatus.EXECUTED or not outcome.executed:
            raise ValueError("only successfully executed outcomes can enter the laboratory")
        if not outcome.evidence_ids:
            raise ValueError("execution outcome requires evidence")
        if not outcome.occurred_at:
            raise ValueError("execution outcome requires timestamp")
        if outcome.correlation_id != decision_id:
            raise ValueError("execution outcome is not bound to the decision")
        if not outcome.request_id:
            raise ValueError("execution outcome requires execution identity")
        if not source_commit:
            raise ValueError("laboratory observation requires source commit")
    def validate_execution_outcome(self, outcome: ExecutionOutcome) -> None:
        """Fail closed when an observation is crossed with another execution."""
        if outcome.status is not ExecutionStatus.EXECUTED or not outcome.executed:
            raise ValueError("only successfully executed outcomes can back a laboratory observation")
        if outcome.request_id != self.source_ref:
            raise ValueError("execution identity does not match laboratory observation")
        if tuple(outcome.evidence_ids) != tuple(self.evidence_ids):
            raise ValueError("execution evidence does not match laboratory observation")
        if outcome.correlation_id != self.decision_id:
            raise ValueError("execution decision binding does not match laboratory observation")
        if not outcome.occurred_at:
            raise ValueError("execution outcome requires timestamp")


        return cls(
            observation_id=observation_id,
            tenant_id=tenant_id,
            domain=domain,
            decision_id=decision_id,
            expected_outcome=expected_outcome,
            observed_outcome=observed_outcome,
            evidence_ids=tuple(outcome.evidence_ids),
            source_ref=outcome.request_id,
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
            source_kind="benchmark",
        )


@dataclass(frozen=True)
class SymbiontLabEvaluation:
    observation: SymbiontLabObservation
    experience: ExperienceRecord | None
    candidate: LearningCandidate | None
    evolution_classification: str
    disposition: str
    state: str = LAB_ONLY


class SymbiontLabAdapter:
    """Thin adapter; no ownership of memory, routing or promotion."""

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
                "tenant_scope": observation.tenant_scope or observation.tenant_id,
                "scope": observation.scope,
            },
        )
        decision = EvolutionGate().evaluate(proposal)
        disposition = self._disposition(decision.classification)

        # Unconfirmed generalization is retained as laboratory evidence only;
        # it must not manufacture a learning candidate.

        # Reuse is an association outcome, not a new learning candidate.
        # Blocked evolution likewise must not create a parallel candidate.
        if decision.classification in {
            EvolutionClassification.DUPLICATE_SUPERSEDED,
            EvolutionClassification.EVOLUTIONARY_CONFLICT,
            EvolutionClassification.INCOMPATIBLE,
        }:
            return SymbiontLabEvaluation(
                observation=observation,
                experience=None,
                candidate=None,
                evolution_classification=decision.classification.value,
                disposition=disposition,
            )

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
        return SymbiontLabEvaluation(
            observation=observation,
            experience=experience,
            candidate=candidate,
            evolution_classification=decision.classification.value,
            disposition=disposition,
        )

    @staticmethod
    def _disposition(classification: EvolutionClassification) -> str:
        return {
            EvolutionClassification.DUPLICATE_SUPERSEDED: "REUSE",
            EvolutionClassification.COMPATIBLE: "CANDIDATE_FOR_GOVERNED_LEARNING",
            EvolutionClassification.ADAPT_REQUIRED: "STRENGTHEN",
            EvolutionClassification.EVOLUTIONARY_CONFLICT: "BLOCK",
            EvolutionClassification.INCOMPATIBLE: "BLOCK",
        }[classification]

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
        if observation.tenant_scope and observation.tenant_scope != observation.tenant_id:
            raise ValueError("tenant scope does not match tenant identity")
        if observation.source_kind and observation.source_kind.strip().lower() not in {
            "repository", "zip", "pr", "issue", "experience", "runtime", "benchmark", "human",
        }:
            raise ValueError("unsupported laboratory source kind")
        if observation.regression_status.upper() in {"REGRESSION", "FAIL"}:
            raise ValueError("regression blocks laboratory evaluation")
        if observation.generalization_status.upper() == "UNCONFIRMED":
            raise ValueError("unconfirmed generalization blocks learning")
        if observation.generalization_status.upper() not in {"CONFIRMED", "PARTIAL"}:
            raise ValueError("unsupported generalization status")
        if observation.risk.upper() in {"CRITICAL", "CRITICO"}:
            raise ValueError("critical risk blocks laboratory evaluation")

    @staticmethod
    def _maturity_score(observation: SymbiontLabObservation) -> float:
        score = {
            "CONFIRMED": 0.9,
            "PARTIAL": 0.6,
            "UNCONFIRMED": 0.3,
        }.get(observation.generalization_status.upper(), 0.3)
        if observation.risk.upper() in {"HIGH", "CRITICAL", "ALTO", "CRITICO"}:
            score = min(score, 0.4)
        return score
