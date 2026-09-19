"""Governed post-approval loop for already-approved candidates.

This module consumes the canonical DecisionLifecycle. It does not create a
second decision authority, approve candidates, or promote canonical state.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .decision_outcome_loop import DecisionLifecycle, DecisionState


class CandidateApprovalState(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class PostApprovalState(StrEnum):
    OBSERVING = "observing"
    OUTCOME = "outcome"
    REVIEW = "review"


@dataclass(frozen=True)
class ApprovedCandidate:
    candidate_id: str
    skill_id: str
    approval_state: CandidateApprovalState
    implementation_ref: str
    implementation_decision_id: str


@dataclass(frozen=True)
class PostApprovalActivation:
    decision_id: str
    candidate_id: str
    skill_id: str
    implementation_ref: str
    state: PostApprovalState


class ApprovedCandidateLoop:
    """Fail-closed activation boundary after the canonical decision is approved."""

    def activate(
        self,
        *,
        lifecycle: DecisionLifecycle,
        candidates: tuple[ApprovedCandidate, ...],
    ) -> tuple[PostApprovalActivation, ...]:
        if lifecycle.state is not DecisionState.APPROVED:
            raise ValueError("implementation decision must be approved")

        matching = tuple(
            candidate
            for candidate in candidates
            if candidate.implementation_decision_id == lifecycle.decision.decision_id
        )
        activations: list[PostApprovalActivation] = []
        for candidate in matching:
            if candidate.approval_state is not CandidateApprovalState.APPROVED:
                raise ValueError(f"candidate is not approved: {candidate.candidate_id}")
            if not candidate.implementation_ref:
                raise ValueError(
                    f"approved candidate lacks implementation reference: {candidate.candidate_id}"
                )
            activations.append(
                PostApprovalActivation(
                    decision_id=lifecycle.decision.decision_id,
                    candidate_id=candidate.candidate_id,
                    skill_id=candidate.skill_id,
                    implementation_ref=candidate.implementation_ref,
                    state=PostApprovalState.OBSERVING,
                )
            )
        return tuple(activations)
