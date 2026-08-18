import pytest

from elo.core.context_resolution import (
    ContextEvidence,
    ContextPack,
    ContextQuery,
    ContextResolutionEngine,
    ContextSource,
)


def test_tenant_a_cannot_consume_tenant_b_sources_or_evidence():
    query = ContextQuery(
        "estado operacional",
        entity="Multiteiner",
        scope="Duque de Caxias",
        tenant_id="tenant-a",
    )
    pack = ContextPack(
        query=query,
        sources=(
            ContextSource("a", "project", "authorized", "Duque de Caxias", "tenant-a"),
            ContextSource("b", "project", "authorized", "Duque de Caxias", "tenant-b"),
        ),
        evidence=(
            ContextEvidence("a", "evidência A", 0.9, tenant_id="tenant-a", scope="Duque de Caxias"),
            ContextEvidence("b", "evidência B", 0.99, tenant_id="tenant-b", scope="Duque de Caxias"),
        ),
    )

    assert [source.source_id for source in pack.scoped_sources()] == ["a"]
    assert [evidence.source_id for evidence in pack.scoped_evidence()] == ["a"]


def test_mismatched_evidence_tenant_is_rejected_even_when_source_is_allowed():
    query = ContextQuery(
        "estado operacional",
        entity="Multiteiner",
        scope="Duque de Caxias",
        tenant_id="tenant-a",
    )
    pack = ContextPack(
        query=query,
        sources=(ContextSource("a", "project", "authorized", "Duque de Caxias", "tenant-a"),),
        evidence=(
            ContextEvidence("a", "evidência incompatível", 0.99, tenant_id="tenant-b", scope="Duque de Caxias"),
        ),
    )

    assert pack.scoped_evidence() == ()
    assert not pack.sufficient_evidence()


def test_mismatched_evidence_scope_is_rejected_even_when_tenant_is_allowed():
    query = ContextQuery(
        "estado operacional",
        entity="Multiteiner",
        scope="Duque de Caxias",
        tenant_id="tenant-a",
    )
    pack = ContextPack(
        query=query,
        sources=(ContextSource("a", "project", "authorized", "Duque de Caxias", "tenant-a"),),
        evidence=(
            ContextEvidence("a", "evidência de outra unidade", 0.99, tenant_id="tenant-a", scope="São Paulo"),
        ),
    )

    assert pack.scoped_evidence() == ()
    assert not pack.sufficient_evidence()


def test_evidence_source_scope_mismatch_is_rejected():
    query = ContextQuery("estado operacional", entity="Multiteiner", scope="Duque de Caxias")
    pack = ContextPack(
        query=query,
        sources=(ContextSource("a", "project", "authorized", "Duque de Caxias"),),
        evidence=(ContextEvidence("a", "evidência divergente", 0.99, scope="São Paulo"),),
    )

    assert pack.scoped_evidence() == ()


def test_blank_context_question_is_rejected_before_discovery():
    with pytest.raises(ValueError, match="question is required"):
        ContextResolutionEngine().resolve(ContextQuery("   "))


def test_enrichment_preserves_existing_uncertainty_and_adds_new_uncertainty():
    engine = ContextResolutionEngine()
    original = engine.resolve(ContextQuery("estado operacional"))

    enriched = engine.enrich(
        original,
        sources=(ContextSource("a", "project", "authorized"),),
        evidence=(ContextEvidence("a", "fato", 0.8),),
        uncertainties=("source timeout",),
    )

    assert "retrieval pending: authorized source adapters must execute the discovery plan" in enriched.uncertainties
    assert "source timeout" in enriched.uncertainties
    assert original.sources == ()
    assert original.evidence == ()
