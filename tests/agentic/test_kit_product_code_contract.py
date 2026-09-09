from elo.agentic.contracts import KnowledgeCandidate


def test_kit_candidate_exposes_product_code_explicitly() -> None:
    candidate = KnowledgeCandidate(
        source_id="KIT-M01:item-1",
        content="Quadro de distribuição",
        source_type="ELO_MEMORY",
        status="REFERENCE",
        relevance=1.0,
        confidence=1.0,
        context_match=1.0,
        product_code="ELE032",
        metadata={"cod_produt": "ELE032"},
    )

    assert candidate.product_code == "ELE032"
    assert candidate.metadata["cod_produt"] == candidate.product_code
