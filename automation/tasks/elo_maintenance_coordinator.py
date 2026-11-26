#!/usr/bin/env python3
"""Deterministic ELO maintenance coordinator.

Provider-neutral process logic. It evaluates evidence and produces a governed
next state; it is not an architectural authority and performs no network
mutation itself.

Canonical reconciliation is an evidence source for this coordinator. The
coordinator remains the single decision gate: it does not discover or create a
second architectural authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping


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
    # Canonicality facts are populated by repository reconciliation. Defaults
    # are conservative so legacy callers cannot silently prove unknown facts.
    canonical_target_resolved: bool = False
    source_of_truth_resolved: bool = False
    reuse_analysis_complete: bool = False
    duplicate_or_parallel_found: bool | None = None
    contract_conflict: bool | None = None
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


def canonicality_admission(
    facts: Mapping[str, object],
) -> tuple[Outcome | None, list[str]]:
    """Evaluate canonicality facts once, for both Events and PR adapters.

    None means only that canonicality is clear. It does not grant permission,
    certify specialist review, or approve merge. Missing or malformed booleans
    are UNKNOWN; a proven conflict always blocks.
    """
    blockers: list[str] = []
    for key, reason in (
        ("canonical_identity_valid", "canonical_identity_missing_or_invalid"),
        ("canonical_target_resolved", "canonical_target_unresolved"),
        ("source_of_truth_resolved", "source_of_truth_unresolved"),
        ("reuse_analysis_complete", "reuse_analysis_incomplete"),
    ):
        if facts.get(key) is not True:
            blockers.append(reason)

    conflict = False
    for key, unknown, confirmed in (
        ("duplicate_or_parallel_found", "duplicate_or_parallel_state_unknown",
         "duplicate_or_parallel_capability_found"),
        ("contract_conflict", "contract_conflict_state_unknown",
         "canonical_contract_conflict"),
    ):
        value = facts.get(key)
        if value is True:
            blockers.append(confirmed)
            conflict = True
        elif value is not False:
            blockers.append(unknown)
    if conflict:
        return Outcome.BLOCKED, blockers
    if blockers:
        return Outcome.WAITING_FOR_EVIDENCE, blockers
    return None, []


def canonicality_gate(event: Event) -> tuple[bool, list[str]]:
    """Compatibility adapter to the single canonicality admission rule."""
    outcome, reasons = canonicality_admission(vars(event))
    return outcome is None, reasons


def audit(event: Event) -> tuple[Outcome, list[str]]:
    """Return the next governed state and machine-readable reasons."""
    if event.forbidden_action:
        return Outcome.BLOCKED, ["forbidden_or_destructive_action"]
    if not event.canonical_identity_valid:
        return Outcome.WAITING_FOR_EVIDENCE, ["canonical_identity_missing_or_invalid"]
    if not event.evidence_complete:
        return Outcome.WAITING_FOR_EVIDENCE, ["evidence_incomplete"]

    canonical_outcome, canonical_reasons = canonicality_admission(vars(event))
    if canonical_outcome is not None:
        return canonical_outcome, canonical_reasons

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
    print("ELO Maintenance Coordinator contract: OK")
