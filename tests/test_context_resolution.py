from elo.core.context_resolution import (
    ContextEvidence,
    ContextPack,
    ContextQuery,
    ContextResolutionEngine,
    ContextSource,
)


def test_scope_filters_unrelated_sources():
    pack = ContextPack(
        query=ContextQuery("estado da Multiteiner Caxias", "Multiteiner", "Duque de Caxias"),
        sources=(
            ContextSource("caxias", "project", "authorized", "Duque de Caxias"),
            ContextSource("other", "project", "authorized", "São Paulo"),
            ContextSource("global", "knowledge", "canonical"),
        ),
    )
    assert [s.source_id for s in pack.scoped_sources()] == ["caxias", "global"]


def test_context_pack_requires_relevant_evidence():
    query = ContextQuery("estado da Multiteiner Caxias", "Multiteiner", "Duque de Caxias")
    empty = ContextPack(query=query)
    assert not empty.sufficient_evidence()

    populated = ContextPack(
        query=query,
        evidence=(ContextEvidence("caxias", "pedido ativo", 0.9, scope="Duque de Caxias"),),
    )
    assert populated.sufficient_evidence()


def test_resolution_automatically_builds_discovery_plan():
    query = ContextQuery(
        "qual o estado da Multiteiner Caxias?",
        entity="Multiteiner",
        scope="Duque de Caxias",
    )
    pack = ContextResolutionEngine().resolve(query)
    candidates = ContextResolutionEngine.candidate_sources(pack)

    assert pack.discovery_plan is not None
    assert pack.discovery_plan.entities == ("Multiteiner",)
    assert candidates
    assert {candidate.kind for candidate in candidates} & {"CHATGPT_PROJECTS", "GITHUB", "ELO_MEMORY"}
    assert not pack.sufficient_evidence()
    assert not pack.requires_specialist()


def test_specialist_mode_requires_discovered_evidence():
    query = ContextQuery("estado da Multiteiner Caxias", "Multiteiner", "Duque de Caxias")
    pack = ContextResolutionEngine().resolve(query)
    assert not pack.requires_specialist()

    enriched = ContextPack(
        query=query,
        discovery_plan=pack.discovery_plan,
        sources=(ContextSource("caxias", "project", "authorized", "Duque de Caxias"),),
        evidence=(ContextEvidence("caxias", "pedido ativo", 0.9, scope="Duque de Caxias"),),
    )
    assert enriched.requires_specialist()
