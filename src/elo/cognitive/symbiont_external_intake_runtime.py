"""Native orchestration for the governed external-mechanism intake path.

The bridge composes existing canonical boundaries: AbsorptionEnvelope ->
SymbiontPatternIntake -> Symbiont Lab. It owns no registry, memory, provider,
authorization or evolution authority and never promotes a candidate itself.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.contracts.absorption_envelope import AbsorptionEnvelope
from elo.cognitive.symbiont_pattern_intake import (
    ExternalPatternInput,
    PatternIntakeDecision,
    SymbiontPatternIntake,
)
from elo.cognitive.symbionte_lab import SymbiontLabObservation


@dataclass(frozen=True)
class ExternalIntakeResult:
    envelope: AbsorptionEnvelope
    decision: PatternIntakeDecision
    lab_observation: SymbiontLabObservation | None


class NativeSymbiontExternalIntake:
    """Compose the universal intake envelope with the existing ELO lab."""

    def __init__(self, intake: SymbiontPatternIntake | None = None) -> None:
        self.intake = intake or SymbiontPatternIntake()

    def classify_for_lab(
        self,
        envelope: AbsorptionEnvelope,
        *,
        problem: str,
        expected_outcome: str,
        observed_outcome: str,
        decision_id: str,
        baseline: str,
        experiment: str,
        result: str,
        regression_status: str,
        generalization_status: str,
        hypothesis: str | None = None,
        existing_owner: str | None = None,
    ) -> ExternalIntakeResult:
        pattern = ExternalPatternInput(
            pattern_id=envelope.candidate_id,
            tenant_id=envelope.tenant_id,
            domain="external-mechanism",
            source_ref=envelope.source_ref,
            source_commit=envelope.source_commit,
            problem=problem,
            mechanism=envelope.mechanism,
            evidence_ids=envelope.evidence_ids,
            existing_owner=existing_owner,
            scope=envelope.scope,
            tenant_scope=envelope.tenant_id,
            source_kind="repository",
            risk=envelope.risk,
        )
        decision = self.intake.classify(pattern)
        if not decision.candidate_creation_allowed:
            return ExternalIntakeResult(envelope, decision, None)
        observation = self.intake.to_lab_observation(
            pattern,
            expected_outcome=expected_outcome,
            observed_outcome=observed_outcome,
            decision_id=decision_id,
            baseline=baseline,
            experiment=experiment,
            result=result,
            regression_status=regression_status,
            generalization_status=generalization_status,
            hypothesis=hypothesis,
        )
        return ExternalIntakeResult(envelope, decision, observation)
