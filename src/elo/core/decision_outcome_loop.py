"""Governed Decision Outcome Loop primitives.

The loop extends the existing DecisionRecord/OutcomeFeedback boundary. It is a
stateful Core value/service layer only: it does not execute enterprise actions,
authorize writes, or create a second memory authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Mapping

from .systemic_primitives import DecisionRecord, OutcomeFeedback


class DecisionState(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    EXECUTED = "executed"
    OBSERVING = "observing"
    EVALUATED = "evaluated"
    ATTRIBUTED = "attributed"
    LEARNED = "learned"
    CLOSED = "closed"
    ESCALATED = "escalated"
    REVERTED = "reverted"


_ALLOWED: dict[DecisionState, frozenset[DecisionState]] = {
    DecisionState.PROPOSED: frozenset({DecisionState.APPROVED, DecisionState.ESCALATED}),
    DecisionState.APPROVED: frozenset({DecisionState.EXECUTED, DecisionState.REVERTED, DecisionState.ESCALATED}),
    DecisionState.EXECUTED: frozenset({DecisionState.OBSERVING, DecisionState.ESCALATED, DecisionState.REVERTED}),
    DecisionState.OBSERVING: frozenset({DecisionState.EVALUATED, DecisionState.ESCALATED, DecisionState.REVERTED}),
    DecisionState.EVALUATED: frozenset({DecisionState.ATTRIBUTED, DecisionState.ESCALATED}),
    DecisionState.ATTRIBUTED: frozenset({DecisionState.LEARNED, DecisionState.ESCALATED}),
    DecisionState.LEARNED: frozenset({DecisionState.CLOSED}),
    DecisionState.CLOSED: frozenset(),
    DecisionState.ESCALATED: frozenset({DecisionState.APPROVED, DecisionState.REVERTED, DecisionState.CLOSED}),
    DecisionState.REVERTED: frozenset({DecisionState.CLOSED}),
}


@dataclass(frozen=True)
class DecisionTransition:
    decision_id: str
    from_state: DecisionState
    to_state: DecisionState
    occurred_at: datetime
    evidence_ids: tuple[str, ...] = ()
    actor: str | None = None


@dataclass
class DecisionLifecycle:
    decision: DecisionRecord
    state: DecisionState = DecisionState.PROPOSED
    outcome: OutcomeFeedback | None = None
    attribution: Mapping[str, float] = field(default_factory=dict)
    learning_candidate: Mapping[str, object] | None = None
    history: list[DecisionTransition] = field(default_factory=list)

    def transition(
        self,
        to_state: DecisionState,
        *,
        evidence_ids: tuple[str, ...] = (),
        actor: str | None = None,
    ) -> DecisionTransition:
        if to_state not in _ALLOWED[self.state]:
            raise ValueError(f"invalid decision transition: {self.state.value} -> {to_state.value}")
        if to_state in {DecisionState.EVALUATED, DecisionState.ATTRIBUTED, DecisionState.LEARNED, DecisionState.CLOSED} and not evidence_ids:
            raise ValueError(f"{to_state.value} requires evidence")
        event = DecisionTransition(
            decision_id=self.decision.decision_id,
            from_state=self.state,
            to_state=to_state,
            occurred_at=datetime.now(timezone.utc),
            evidence_ids=tuple(dict.fromkeys(evidence_ids)),
            actor=actor,
        )
        self.state = to_state
        self.history.append(event)
        return event

    def attach_outcome(self, outcome: OutcomeFeedback) -> None:
        if outcome.decision_id != self.decision.decision_id:
            raise ValueError("outcome decision_id does not match decision")
        if self.state != DecisionState.OBSERVING:
            raise ValueError("outcome can only be attached while observing")
        if not outcome.evidence_ids:
            raise ValueError("outcome requires evidence")
        self.outcome = outcome

    def attach_attribution(self, attribution: Mapping[str, float]) -> None:
        if self.state != DecisionState.EVALUATED:
            raise ValueError("attribution requires evaluated state")
        if not attribution:
            raise ValueError("attribution is required")
        if any(value < 0 for value in attribution.values()):
            raise ValueError("attribution weights cannot be negative")
        total = sum(attribution.values())
        if total <= 0:
            raise ValueError("attribution weights must have positive total")
        self.attribution = {key: value / total for key, value in attribution.items()}

    def attach_learning(self, candidate: Mapping[str, object]) -> None:
        if self.state != DecisionState.ATTRIBUTED:
            raise ValueError("learning requires attributed state")
        if not candidate:
            raise ValueError("learning candidate is required")
        self.learning_candidate = dict(candidate)


    def handoff_to_symbiont(
        self,
        *,
        adapter: "SymbiontLabAdapter",
        observation: "SymbiontLabObservation",
        principal_id: str,
        dataset_version: str,
    ) -> "SymbiontLabEvaluation":
        """Send an evaluated decision outcome through the existing Symbiont Lab.

        The lifecycle remains the decision authority; Symbiont remains the
        laboratory/learning bridge. No second candidate or memory path is
        created here. The decision enters learned only when Symbiont returns
        a learning candidate.
        """
        if self.state is not DecisionState.ATTRIBUTED:
            raise ValueError("Symbiont handoff requires attributed state")
        if observation.decision_id != self.decision.decision_id:
            raise ValueError("Symbiont observation decision_id does not match decision")
        if self.outcome is None:
            raise ValueError("Symbiont handoff requires an attached outcome")
        if not self.attribution:
            raise ValueError("Symbiont handoff requires attribution")
        if not observation.evidence_ids:
            raise ValueError("Symbiont handoff requires evidence")

        evaluation = adapter.evaluate(
            observation,
            principal_id=principal_id,
            dataset_version=dataset_version,
        )
        if evaluation.candidate is not None:
            self.attach_learning({
                "candidate_id": evaluation.candidate.candidate_id,
                "experience_id": evaluation.candidate.experience_id,
                "dataset_version": evaluation.candidate.dataset_version,
                "hypothesis": evaluation.candidate.hypothesis,
                "evolution_classification": evaluation.evolution_classification,
            })
            self.transition(
                DecisionState.LEARNED,
                evidence_ids=tuple(observation.evidence_ids),
                actor="symbiont",
            )
        return evaluation
