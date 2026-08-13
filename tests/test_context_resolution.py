from elo.core.context_resolution import (
    ContextEvidence,
    ContextPack,
    ContextQuery,
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
        evidence=(ContextEvidence("caxias", "pedido ativo", 0.9),),
    )
    assert populated.sufficient_evidence()
