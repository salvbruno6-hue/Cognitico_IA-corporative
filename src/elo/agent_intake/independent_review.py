"""Governed evidence contract for independent review of ELO artifacts.

This module records review evidence only. It does not execute reviewers, mutate
canonical state, approve merges, or promote learning. It captures the useful
Hermes pattern of a fresh reviewer context while keeping authority in ELO's
existing validation and Evolution Gate boundaries.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

VALID_VERDICTS = frozenset({"PASS", "FAIL", "ABSTAIN"})

@dataclass(frozen=True)
class IndependentReviewEvidence:
    """Immutable, provenance-bearing result from an independent reviewer."""
    subject_id: str
    subject_owner_id: str
    reviewer_id: str
    review_scope: str
    context_snapshot_id: str
    inherited_skill_ids: tuple[str, ...] = ()
    authorized_tool_ids: tuple[str, ...] = ()
    verdict: str = "ABSTAIN"
    findings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    provenance: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        required = (self.subject_id, self.subject_owner_id, self.reviewer_id,
                    self.review_scope, self.context_snapshot_id)
        if not all(required):
            raise ValueError("review identity, scope and context snapshot are required")
        if self.reviewer_id == self.subject_owner_id:
            raise ValueError("independent review requires a distinct reviewer identity")
        if self.verdict not in VALID_VERDICTS:
            raise ValueError("verdict must be PASS, FAIL or ABSTAIN")
        if not self.evidence_ids:
            raise ValueError("independent review requires evidence_ids")
        if self.provenance is None or not self.provenance:
            raise ValueError("provenance is required")

def validate_independent_review(
    review: IndependentReviewEvidence,
    *,
    expected_subject_id: str | None = None,
) -> bool:
    """Validate review evidence without granting promotion or merge authority."""
    if expected_subject_id is not None and review.subject_id != expected_subject_id:
        return False
    if review.reviewer_id == review.subject_owner_id:
        return False
    if not review.context_snapshot_id or not review.evidence_ids:
        return False
    return review.verdict in VALID_VERDICTS

__all__ = ["IndependentReviewEvidence", "validate_independent_review"]
