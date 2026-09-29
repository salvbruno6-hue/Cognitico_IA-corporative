"""Skill-level experience feedback for the canonical Symbiont learning loop.

This adapter gives every governed Skill execution the same learning contract:
execution outcome -> ExperienceRecord -> learning trigger -> candidate.

It is intentionally non-authoritative. It never approves, promotes, authorizes,
mutates Core, or bypasses the existing Evolution Gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from elo.core.learning_governance import ExperienceRecord, GovernedLearningService, LearningCandidate
from .symbiont_experience_learning import LearningTrigger, SymbiontLearningSignal, trigger_learning


@dataclass(frozen=True, slots=True)
class SkillExecutionContext:
    skill_id: str
    tenant_id: str
    domain: str
    principal_id: str
    decision_id: str
    expected_outcome: str
    observed_outcome: str
    evidence_ids: tuple[str, ...]
    dataset_version: str

    def __post_init__(self) -> None:
        required = {
            "skill_id": self.skill_id,
            "tenant_id": self.tenant_id,
            "domain": self.domain,
            "principal_id": self.principal_id,
            "decision_id": self.decision_id,
            "expected_outcome": self.expected_outcome,
            "observed_outcome": self.observed_outcome,
            "dataset_version": self.dataset_version,
        }
        missing = tuple(name for name, value in required.items() if not value)
        if missing:
            raise ValueError("skill execution context missing: " + ", ".join(missing))


@dataclass(frozen=True, slots=True)
class SkillLearningFeedback:
    skill_id: str
    experience: ExperienceRecord
    signal: SymbiontLearningSignal

    @property
    def trigger(self) -> LearningTrigger:
        return self.signal.trigger

    @property
    def learning_candidate(self) -> LearningCandidate | None:
        return self.signal.learning_candidate

    @property
    def canonical_mutation(self) -> bool:
        return self.signal.canonical_mutation

    @property
    def authorization_granted(self) -> bool:
        return self.signal.authorization_granted


def observe_skill_outcome(
    service: GovernedLearningService,
    context: SkillExecutionContext,
    *,
    repeated: bool = False,
    regression: bool = False,
    boundary_violation: bool = False,
    evidence_complete: bool = True,
) -> SkillLearningFeedback:
    """Capture one Skill outcome and feed it into the governed trigger loop."""
    experience = service.capture_outcome(
        tenant_id=context.tenant_id,
        domain=context.domain,
        principal_id=context.principal_id,
        decision_id=context.decision_id,
        expected_outcome=context.expected_outcome,
        observed_outcome=context.observed_outcome,
        evidence_ids=context.evidence_ids,
    )
    signal = trigger_learning(
        service,
        experience=experience,
        dataset_version=context.dataset_version,
        repeated=repeated,
        regression=regression,
        boundary_violation=boundary_violation,
        evidence_complete=evidence_complete,
    )
    return SkillLearningFeedback(
        skill_id=context.skill_id,
        experience=experience,
        signal=signal,
    )


def observe_skill_batch(
    service: GovernedLearningService,
    contexts: Iterable[SkillExecutionContext],
    *,
    repeated_skill_ids: frozenset[str] = frozenset(),
    regression_skill_ids: frozenset[str] = frozenset(),
    boundary_violation_skill_ids: frozenset[str] = frozenset(),
) -> tuple[SkillLearningFeedback, ...]:
    """Apply the same governed feedback contract to a set of Skill executions."""
    return tuple(
        observe_skill_outcome(
            service,
            context,
            repeated=context.skill_id in repeated_skill_ids,
            regression=context.skill_id in regression_skill_ids,
            boundary_violation=context.skill_id in boundary_violation_skill_ids,
            evidence_complete=bool(context.evidence_ids),
        )
        for context in contexts
    )


__all__ = [
    "SkillExecutionContext",
    "SkillLearningFeedback",
    "observe_skill_outcome",
    "observe_skill_batch",
]
