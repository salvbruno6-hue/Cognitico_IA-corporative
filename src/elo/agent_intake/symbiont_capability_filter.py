"""Deep, fail-closed filter for candidate capability evolution.

This module does not create a new authority. It sits before implementation review
and asks whether a candidate truly deepens an existing ELO mechanism instead of
adding a parallel owner, duplicating capability, or changing the owner's purpose.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .hermes_functional_value_proof import FunctionalValueEvidence


class FilterDisposition(StrEnum):
    ACCEPT = "ACCEPT"
    RETEST = "RETEST"
    REJECT = "REJECT"


@dataclass(frozen=True, slots=True)
class CapabilityEvolutionProposal:
    candidate_id: str
    existing_owner: str
    proposed_owner: str
    mechanism_objective: str
    owner_objective: str
    objective_alignment_confirmed: bool
    creates_new_authority: bool = False
    creates_parallel_owner: bool = False
    duplicates_existing_capability: bool = False
    changes_owner_objective: bool = False


@dataclass(frozen=True, slots=True)
class CapabilityFilterDecision:
    candidate_id: str
    disposition: FilterDisposition
    reasons: tuple[str, ...]
    owner_preserved: bool
    objective_preserved: bool
    functional_gain_proven: bool


def evaluate_capability_evolution(
    proposal: CapabilityEvolutionProposal,
    evidence: FunctionalValueEvidence | None,
) -> CapabilityFilterDecision:
    """Admit only net functional evolution attached to the existing owner."""
    reasons: list[str] = []
    owner_preserved = (
        bool(proposal.existing_owner.strip())
        and proposal.existing_owner == proposal.proposed_owner
        and not proposal.creates_new_authority
        and not proposal.creates_parallel_owner
    )
    objective_preserved = (
        bool(proposal.mechanism_objective.strip())
        and bool(proposal.owner_objective.strip())
        and proposal.objective_alignment_confirmed
        and not proposal.changes_owner_objective
    )

    if not owner_preserved:
        reasons.append("existing_owner_must_remain_authoritative")
    if not objective_preserved:
        reasons.append("mechanism_must_deepen_existing_owner_objective")
    if proposal.duplicates_existing_capability:
        reasons.append("duplicate_capability_is_not_evolution")

    structural_reject = (
        not owner_preserved
        or not objective_preserved
        or proposal.duplicates_existing_capability
    )
    if structural_reject:
        return CapabilityFilterDecision(
            proposal.candidate_id,
            FilterDisposition.REJECT,
            tuple(reasons),
            owner_preserved,
            objective_preserved,
            False,
        )

    gain_proven = bool(
        evidence is not None
        and evidence.candidate_id == proposal.candidate_id
        and evidence.functional_gain_proven
    )
    if not gain_proven:
        reasons.append("candidate_attributed_repeatable_functional_gain_required")
        return CapabilityFilterDecision(
            proposal.candidate_id,
            FilterDisposition.RETEST,
            tuple(reasons),
            owner_preserved,
            objective_preserved,
            False,
        )

    return CapabilityFilterDecision(
        proposal.candidate_id,
        FilterDisposition.ACCEPT,
        ("net_functional_evolution_confirmed",),
        True,
        True,
        True,
    )


__all__ = [
    "CapabilityEvolutionProposal",
    "CapabilityFilterDecision",
    "FilterDisposition",
    "evaluate_capability_evolution",
]
