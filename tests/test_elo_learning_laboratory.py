import pytest

from src.elo.core.learning_laboratory import (
    CANDIDATE,
    EXPERIENCE,
    PROMOTED,
    VALIDATED,
    GovernedLearningLaboratory,
    LearningObservation,
)


def observation(observation_id="o1", tenant_id="t1", evidence_ids=()):
    return LearningObservation(
        observation_id=observation_id,
        tenant_id=tenant_id,
        source_type="AI_PROVIDER",
        problem="budget mission",
        result="draft result",
        evidence_ids=evidence_ids,
    )


def test_lifecycle_requires_evidence_and_validation():
    lab = GovernedLearningLaboratory()
    lab.record(observation())
    with pytest.raises(ValueError, match="requires evidence"):
        lab.propose("o1")

    lab.record(observation("o2", evidence_ids=("e1",)))
    assert lab.propose("o2").status == CANDIDATE
    assert lab.validate("o2").status == VALIDATED
    assert lab.promote("o2").status == PROMOTED


def test_new_observations_are_experience_and_ids_are_unique():
    lab = GovernedLearningLaboratory()
    assert lab.record(observation()).status == EXPERIENCE
    with pytest.raises(ValueError, match="already exists"):
        lab.record(observation())


def test_tenant_isolation():
    lab = GovernedLearningLaboratory()
    lab.record(observation("a", "tenant-a"))
    lab.record(observation("b", "tenant-b"))
    assert [o.observation_id for o in lab.list_tenant("tenant-a")] == ["a"]
    assert [o.observation_id for o in lab.list_tenant("tenant-b")] == ["b"]
