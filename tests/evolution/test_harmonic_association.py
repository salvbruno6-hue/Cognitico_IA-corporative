import pytest

from elo.cognitive.harmonic_association import (
    HarmonicAssociationEngine,
    HarmonicAssociationObservation,
    LAB_ONLY,
)


def obs(observation_id: str, tenant_id: str = "tenant-a", owner: str | None = None):
    return HarmonicAssociationObservation(
        observation_id=observation_id,
        tenant_id=tenant_id,
        context="orcamento",
        need="compor custo",
        capability="budget reasoning",
        skill="cost composition",
        tool="calculator",
        result="validated",
        evidence_ids=(f"ev-{observation_id}",),
        source_ref=f"pr-{observation_id}",
        source_commit=f"commit-{observation_id}",
        existing_owner=owner,
    )


def test_associates_repeated_harmonic_pattern_without_canonical_mutation():
    associations = HarmonicAssociationEngine.associate([obs("1"), obs("2")], association_id="assoc-1")
    assert len(associations) == 1
    association = associations[0]
    assert association.state == LAB_ONLY
    assert association.disposition == "CANDIDATE_FOR_GOVERNED_LEARNING"
    assert association.source_observation_ids == ("1", "2")
    assert set(association.evidence_ids) == {"ev-1", "ev-2"}


def test_reuses_existing_owner_without_creating_parallel_authority():
    associations = HarmonicAssociationEngine.associate(
        [obs("1", owner="canonical-budget"), obs("2", owner="canonical-budget")],
        association_id="assoc-2",
    )
    assert associations[0].disposition == "REUSE"
    assert associations[0].existing_owner == "canonical-budget"
    assert associations[0].state == LAB_ONLY


def test_cross_tenant_association_is_blocked():
    with pytest.raises(ValueError, match="tenant boundaries"):
        HarmonicAssociationEngine.associate([obs("1", "tenant-a"), obs("2", "tenant-b")], association_id="assoc-3")


def test_missing_evidence_is_blocked_before_association():
    bad = obs("1")
    bad = HarmonicAssociationObservation(**{**bad.__dict__, "evidence_ids": ()})
    with pytest.raises(ValueError, match="evidence"):
        HarmonicAssociationEngine.associate([bad, obs("2")], association_id="assoc-4")


def test_different_contexts_do_not_create_false_harmonic_link():
    first = obs("1")
    second = HarmonicAssociationObservation(**{**obs("2").__dict__, "context": "producao"})
    assert HarmonicAssociationEngine.associate([first, second], association_id="assoc-5") == ()
