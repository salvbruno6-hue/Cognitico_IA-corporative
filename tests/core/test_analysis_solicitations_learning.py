from elo.core import build_learning_candidate, classify_candidate
from scripts.solicitations_learning_consolidate import _concept_key, _normalize


def test_single_observation_is_precedent():
    candidate = build_learning_candidate(
        solicitation_id="SO 120.26",
        category="EQUIVALENT_SOLUTION",
        statement="PIR 32 mm accepted after client clarification",
        evidence_refs=["SO120.26:question-03"],
        confidence=0.9,
    )
    assert candidate.validation_status == "CAPTURED"
    assert classify_candidate(candidate) == "PRECEDENT"


def test_repeated_unvalidated_observation_is_learning_candidate():
    candidate = build_learning_candidate(
        solicitation_id="SO 121.26",
        category="REUSABLE_QUESTION",
        statement="Confirm QGBT dimensions before electrical budget closure",
        evidence_refs=["SO121.26:q-02", "SO122.26:q-04"],
        confidence=0.8,
    )
    candidate = candidate.__class__(**{**candidate.__dict__, "recurrence_count": 2})
    assert classify_candidate(candidate) == "LEARNING_CANDIDATE"


def test_same_concept_across_solicitations_is_not_duplicated():
    left = _concept_key("PRECEDENT", "SO 155.26: confirmar produtividade de acoplamento")
    right = _concept_key("PRECEDENT", "SO 156.26: confirmar produtividade de acoplamento")
    assert left == right


def test_different_budget_experience_is_new_concept():
    left = _concept_key("PRECEDENT", "SO 155.26: confirmar produtividade de acoplamento")
    right = _concept_key("PRECEDENT", "SO 155.26: dimensionar drenagem subterrânea")
    assert left != right


def test_normalization_removes_solicitation_identity_only():
    assert _normalize("SO 155.26  Confirmar produtividade") == "<so> confirmar produtividade"
