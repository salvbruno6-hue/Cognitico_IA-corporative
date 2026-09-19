"""Governed post-approval loop for already-approved candidates.

This module does not approve candidates and does not promote canonical state.
It only activates candidates that already carry an explicit approved status
after an implementation decision reaches APPROVED.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CandidateApprovalState(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class PostApprovalState(StrEnum):
    APPROVED = "approved"
    DEPLOYED = "deployed"
    USED = "used"
    OBSERVING = "observing"
    OUTCOME = "outcome"
    REVIEW = "review"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class ApprovedCandidate:
    candidate_id: str
    skill_id: str
    approval_state: CandidateApprovalState
    implementation_ref: str


@dataclass(frozen=True)
class ImplementationDecision:
    decision_id: str
    state: str
    approved_candidate_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class PostApprovalActivation:
    decision_id: str
    candidate_id: str
    skill_id: str
    implementation_ref: str
    state: PostApprovalState


class ApprovedCandidateLoop:
    """Fail-closed activation boundary after an implementation decision."""

    def activate(
        self,
        *,
        decision: ImplementationDecision,
        candidates: tuple[ApprovedCandidate, ...],
    ) -> tuple[PostApprovalActivation, ...]:
        if decision.state != "approved":
            raise ValueError("implementation decision must be approved")
        candidate_map = {candidate.candidate_id: candidate for candidate in candidates}
        activations: list[PostApprovalActivation] = []
        for candidate_id in decision.approved_candidate_ids:
            candidate = candidate_map.get(candidate_id)
            if candidate is None:
                raise ValueError(f"approved candidate not found: {candidate_id}")
            if candidate.approval_state is not CandidateApprovalState.APPROVED:
                raise ValueError(
                    f"candidate is not approved: {candidate.candidate_id}"
                )
            if not candidate.implementation_ref:
                raise ValueError(
                    f"approved candidate lacks implementation reference: {candidate.candidate_id}"
                )
            activations.append(
                PostApprovalActivation(
                    decision_id=decision.decision_id,
                    candidate_id=candidate.candidate_id,
                    skill_id=candidate.skill_id,
                    implementation_ref=candidate.implementation_ref,
                    state=PostApprovalState.OBSERVING,
                )
            )
        return tuple(activations)
