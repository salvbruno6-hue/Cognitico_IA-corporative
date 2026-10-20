from dataclasses import FrozenInstanceError
import pytest
from elo.agent_intake.independent_review import IndependentReviewEvidence, validate_independent_review

def _review(**overrides):
    data = {
        "subject_id": "candidate:HERMES-DELEGATION",
        "subject_owner_id": "elo-forge",
        "reviewer_id": "elo-reviewer-01",
        "review_scope": "governance-contract",
        "context_snapshot_id": "ctx-001",
        "inherited_skill_ids": ("skill:review",),
        "authorized_tool_ids": ("tool:read",),
        "verdict": "PASS",
        "findings": (),
        "evidence_ids": ("test:independent-review",),
        "provenance": {"source": "hermes", "mode": "read_only"},
    }
    data.update(overrides)
    return IndependentReviewEvidence(**data)

def test_independent_reviewer_must_be_distinct_from_subject_owner():
    with pytest.raises(ValueError, match="distinct reviewer"):
        _review(reviewer_id="elo-forge")

def test_review_requires_context_snapshot_and_evidence():
    with pytest.raises(ValueError, match="context snapshot"):
        _review(context_snapshot_id="")
    with pytest.raises(ValueError, match="evidence_ids"):
        _review(evidence_ids=())

def test_review_verdict_is_bounded():
    with pytest.raises(ValueError, match="verdict"):
        _review(verdict="PROMOTE")

def test_review_is_immutable():
    review = _review()
    with pytest.raises(FrozenInstanceError):
        review.verdict = "FAIL"

def test_validation_accepts_matching_subject():
    assert validate_independent_review(_review(), expected_subject_id="candidate:HERMES-DELEGATION")

def test_validation_rejects_subject_mismatch():
    assert not validate_independent_review(_review(), expected_subject_id="candidate:HERMES-CONTEXT")

def test_review_does_not_imply_promotion():
    review = _review()
    assert not hasattr(review, "promotion_allowed")
    assert not hasattr(review, "merge_allowed")
