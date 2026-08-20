#!/usr/bin/env python3
"""Deterministic ELO maintenance coordinator.

This module is deliberately provider-neutral. It evaluates GitHub evidence and
produces a governed decision; it does not act as an autonomous architectural
authority. A real GitHub adapter can consume the returned decision and apply
labels/comments/auto-merge only when repository policy permits it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class Outcome(str, Enum):
    READY_FOR_SPECIALIST = "READY_FOR_SPECIALIST"
    WAITING_FOR_EVIDENCE = "WAITING_FOR_EVIDENCE"
    READY_FOR_ELO_DECISION = "READY_FOR_ELO_DECISION"
    APPROVED_FOR_MERGE = "APPROVED_FOR_MERGE"
    RECORDED_AS_TEMPORAL_EXPERIENCE = "RECORDED_AS_TEMPORAL_EXPERIENCE"
    ROADMAP_CANDIDATE = "ROADMAP_CANDIDATE"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class Event:
    number: int
    concept_id: str | None
    event_class: str
    acceptance_pass: bool
    specialist_pass: bool | None
    ci_pass: bool
    reviews_clear: bool
    scope_compliant: bool
    forbidden_action: bool
    elo_approve_merge: bool
    evidence_complete: bool
    canonical_identity_valid: bool
    architectural_impact: bool
    experience_value: bool
    provenance_complete: bool = False
    contradiction_free: bool = False
    labels: frozenset[str] = field(default_factory=frozenset)


SPECIALIST_BY_EVENT = {
    "architecture": "architecture",
    "structure": "architecture",
    "budget": "domain-finance",
    "costing": "domain-finance",
    "regulatory": "domain-regulatory",
    "security": "security",
    "data": "data",
    "automation": "operations-automation",
    "runtime": "operations-automation",
    "testing": "testing",
    "memory": "cognitive-knowledge",
    "experience": "cognitive-knowledge",
}


def specialist_lane(event_class: str) -> str | None:
    return SPECIALIST_BY_EVENT.get(event_class.lower().strip())


def audit(event: Event) -> tuple[Outcome, list[str]]:
    """Return the next governed state and machine-readable reasons."""
    reasons: list[str] = []

    if event.forbidden_action:
        return Outcome.BLOCKED, ["forbidden_or_destructive_action"]

    if not event.canonical_identity_valid:
        return Outcome.WAITING_FOR_EVIDENCE, ["canonical_identity_missing_or_invalid"]

    if not event.evidence_complete:
        return Outcome.WAITING_FOR_EVIDENCE, ["evidence_incomplete"]

    if event.specialist_pass is None:
        lane = specialist_lane(event.event_class)
        return Outcome.READY_FOR_SPECIALIST, [
            f"specialist_consultation_required:{lane or 'domain-review'}"
        ]

    if not event.specialist_pass:
        return Outcome.BLOCKED, ["specialist_review_failed"]

    if event.architectural_impact:
        if not event.acceptance_pass or not event.ci_pass or not event.reviews_clear:
            return Outcome.WAITING_FOR_EVIDENCE, [
                *([] if event.acceptance_pass else ["acceptance_failed"]),
                *([] if event.ci_pass else ["ci_failed"]),
                *([] if event.reviews_clear else ["blocking_review_exists"]),
            ]
        if not event.scope_compliant:
            return Outcome.BLOCKED, ["scope_non_compliant"]
        if not event.elo_approve_merge:
            return Outcome.READY_FOR_ELO_DECISION, ["explicit_elo_merge_authorization_required"]
        return Outcome.APPROVED_FOR_MERGE, ["all_merge_gates_pass"]

    # Non-architectural learning is admitted only as governed experience.
    if event.experience_value:
        if not event.provenance_complete or not event.contradiction_free:
            return Outcome.WAITING_FOR_EVIDENCE, [
                *([] if event.provenance_complete else ["provenance_incomplete"]),
                *([] if event.contradiction_free else ["canonical_contradiction_check_required"]),
            ]
        return Outcome.RECORDED_AS_TEMPORAL_EXPERIENCE, [
            "valuable_experience_without_canonical_structure_change"
        ]

    return Outcome.ROADMAP_CANDIDATE, ["no_current_canonical_evolution_admitted"]


def merge_gate(event: Event) -> bool:
    """Strict predicate for enabling repository auto-merge."""
    outcome, _ = audit(event)
    return outcome is Outcome.APPROVED_FOR_MERGE


def consultation_request(event: Event) -> dict[str, object]:
    lane = specialist_lane(event.event_class) or "domain-review"
    return {
        "issue": event.number,
        "concept_id": event.concept_id,
        "specialist_lane": lane,
        "question": "Can this event be admitted as the next governed ELO evolution?",
        "requires_canonical_identity": True,
        "evidence_required": True,
    }


def summarize(events: Iterable[Event]) -> list[dict[str, object]]:
    result = []
    for event in events:
        outcome, reasons = audit(event)
        result.append(
            {
                "issue": event.number,
                "event_class": event.event_class,
                "outcome": outcome.value,
                "reasons": reasons,
                "specialist": specialist_lane(event.event_class),
            }
        )
    return result


if __name__ == "__main__":
    raise SystemExit(
        "Use this module from a GitHub adapter or test harness; no network mutation is performed here."
    )
