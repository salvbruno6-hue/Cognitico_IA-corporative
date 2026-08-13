"""Outcome feedback primitives for measuring decision quality over time."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OutcomeFeedback:
    decision_id: str
    outcome_id: str
    expected: str
    observed: str
    assessment: str
    evidence_ids: tuple[str, ...] = ()
