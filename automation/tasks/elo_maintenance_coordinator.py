#!/usr/bin/env python3
"""Deterministic ELO maintenance coordinator.

Provider-neutral process logic. It evaluates evidence and produces a governed
next state; it is not an architectural authority and performs no network
mutation itself.
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
    if event.forbidden_action:
        return Outcome.BLOCKED, ["forbidden_or_destructive_action"]
    if not event.canonical_identity_valid:
        return Outcome.WAITING_FOR_EVIDENCE, ["canonical_identity_missing_or_invalid"]
    if not event.evidence_complete:
        return Outcome.WAITING_FOR_EVIDENCE, ["evidence_incomplete"]
    if event.specialist_pass is None:
        lane = specialist_lane(event.event_class)
        return Outcome.READY_FOR_SPECIALIST, [f"specialist_consultation_required:{lane or 'domain-review'}"]
    if not event.specialist_pass:
        return Outcome.BLOCKED, ["specialist_review_failed"]

    if event.architectural_impact:
        missing = []
        if not event.acceptance_pass:
            missing.append("acceptance_failed")
        if not event.ci_pass:
            missing.append("ci_failed")
        if not event.reviews_clear:
            missing.append("blocking_review_exists")
        if missing:
            return Outcome.WAITING_FOR_EVIDENCE, missing
        if not event.scope_compliant:
            return Outcome.BLOCKED, ["scope_non_compliant"]
        if not event.elo_approve_merge:
            return Outcome.READY_FOR_ELO_DECISION, ["explicit_elo_merge_authorization_required"]
        return Outcome.APPROVED_FOR_MERGE, ["all_merge_gates_pass"]

    if event.experience_value:
        missing = []
        if not event.provenance_complete:
            missing.append("provenance_incomplete")
        if not event.contradiction_free:
            missing.append("canonical_contradiction_check_required")
        if missing:
            return Outcome.WAITING_FOR_EVIDENCE, missing
        return Outcome.RECORDED_AS_TEMPORAL_EXPERIENCE, ["valuable_experience_without_canonical_structure_change"]

    return Outcome.ROADMAP_CANDIDATE, ["no_current_canonical_evolution_admitted"]


def merge_gate(event: Event) -> bool:
    return audit(event)[0] is Outcome.APPROVED_FOR_MERGE


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
        result.append({
            "issue": event.number,
            "event_class": event.event_class,
            "outcome": outcome.value,
            "reasons": reasons,
            "specialist": specialist_lane(event.event_class),
        })
    return result


if __name__ == "__main__":
    # Contract smoke mode used by CI. GitHub mutation is handled only by the
    # workflow adapter, never by this module.
    print("ELO Maintenance Coordinator contract: OK")
