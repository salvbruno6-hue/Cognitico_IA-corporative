import pytest

from src.elo.core.learning_laboratory import (
    CANDIDATE, EXPERIENCE, PROMOTED, VALIDATED,
    GovernedLearningLaboratory, LearningObservation,
)


def make_observation(evidence_ids=()):
    return LearningObservation(
        observation_id="obs-1", tenant_id="tenant-1", source_type="ai",
        problem="calculo de orçamento", result="resultado observado",
        evidence_ids=evidence_ids,
    )


def test_new_learning_is_isolated_as_experience():
    lab = GovernedLearningLaboratory()
    observed = lab.record(make_observation())
    assert observed.status == EXPERIENCE
    assert lab.list_tenant("tenant-1") == (observed,)


def test_candidate_requires_evidence():
    lab = GovernedLearningLaboratory()
    lab.record(make_observation())
    with pytest.raises(ValueError):
        lab.propose("obs-1")


def test_learning_requires_validation_before_promotion():
    lab = GovernedLearningLaboratory()
    lab.record(make_observation(("evidence-1",)))
    assert lab.propose("obs-1").status == CANDIDATE
    assert lab.validate("obs-1").status == VALIDATED
    assert lab.promote("obs-1").status == PROMOTED


def test_tenant_isolation_in_learning_laboratory():
    lab = GovernedLearningLaboratory()
    lab.record(make_observation(("evidence-1",)))
    assert lab.list_tenant("tenant-2") == ()
