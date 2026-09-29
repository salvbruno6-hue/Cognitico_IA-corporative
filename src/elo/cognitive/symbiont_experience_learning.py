"""Experience-driven learning triggers for the canonical Symbiont loop.

The trigger engine converts observed outcomes into a governed learning signal.
It never mutates Core, grants authorization, promotes a Skill, or replaces the
Evolution Gate. Persistence and candidate creation remain the responsibility
of GovernedLearningService.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from elo.core.learning_governance import ExperienceRecord, GovernedLearningService, LearningCandidate


class LearningTrigger(str, Enum):
    POSITIVE_GAIN = "POSITIVE_GAIN"
    REGRESSION = "REGRESSION"
    REPEATED_OUTCOME = "REPEATED_OUTCOME"
    BOUNDARY_VIOLATION = "BOUNDARY_VIOLATION"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"


@dataclass(frozen=True, slots=True)
class SymbiontLearningSignal:
    trigger: LearningTrigger
    experience_id: str
    decision_id: str
    action: str
    hypothesis: str
    evidence_refs: tuple[str, ...]
    learning_candidate: LearningCandidate | None = None
    canonical_mutation: bool = False
    authorization_granted: bool = False


def detect_learning_trigger(
    *,
    experience: ExperienceRecord,
    repeated: bool = False,
    regression: bool = False,
    boundary_violation: bool = False,
    evidence_complete: bool = True,
) -> LearningTrigger:
    """Select one deterministic learning trigger from an observed experience."""
    if not evidence_complete or not experience.evidence_ids:
        return LearningTrigger.MISSING_EVIDENCE
    if boundary_violation:
        return LearningTrigger.BOUNDARY_VIOLATION
    if regression:
        return LearningTrigger.REGRESSION
    if repeated:
        return LearningTrigger.REPEATED_OUTCOME
    return LearningTrigger.POSITIVE_GAIN


def trigger_learning(
    service: GovernedLearningService,
    *,
    experience: ExperienceRecord,
    dataset_version: str,
    repeated: bool = False,
    regression: bool = False,
    boundary_violation: bool = False,
    evidence_complete: bool = True,
) -> SymbiontLearningSignal:
    """Turn experience into a governed learning candidate when justified.

    The important boundary is intentional: a trigger can create a candidate
    for governed learning, but it cannot approve, promote, authorize, or mutate
    canonical ELO state.
    """
    trigger = detect_learning_trigger(
        experience=experience,
        repeated=repeated,
        regression=regression,
        boundary_violation=boundary_violation,
        evidence_complete=evidence_complete,
    )

    actions = {
        LearningTrigger.POSITIVE_GAIN: (
            "RETAIN_AND_TEST",
            "The observed decision outcome improved; test whether the same decision pattern generalizes.",
        ),
        LearningTrigger.REGRESSION: (
            "DIAGNOSE_AND_CORRECT",
            "The observed outcome regressed; reproduce the regression and test a bounded correction.",
        ),
        LearningTrigger.REPEATED_OUTCOME: (
            "AGGREGATE_EXPERIENCE",
            "The outcome repeated; aggregate evidence before proposing a reusable learning pattern.",
        ),
        LearningTrigger.BOUNDARY_VIOLATION: (
            "BLOCK_AND_REVIEW",
            "A governance boundary was violated; preserve the evidence and require review before reuse.",
        ),
        LearningTrigger.MISSING_EVIDENCE: (
            "COLLECT_EVIDENCE",
            "The outcome cannot become learning until evidence and provenance are complete.",
        ),
    }
    action, hypothesis = actions[trigger]

    candidate = None
    if trigger not in {
        LearningTrigger.BOUNDARY_VIOLATION,
        LearningTrigger.MISSING_EVIDENCE,
    }:
        candidate = service.propose_candidate(
            experience,
            dataset_version=dataset_version,
            hypothesis=hypothesis,
        )

    return SymbiontLearningSignal(
        trigger=trigger,
        experience_id=experience.experience_id,
        decision_id=experience.decision_id,
        action=action,
        hypothesis=hypothesis,
        evidence_refs=tuple(experience.evidence_ids),
        learning_candidate=candidate,
    )


__all__ = [
    "LearningTrigger",
    "SymbiontLearningSignal",
    "detect_learning_trigger",
    "trigger_learning",
]
