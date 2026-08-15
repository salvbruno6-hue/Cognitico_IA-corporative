from members.ELO_ORG.corporate_systemic_model import (
    AnalysisState,
    CorporateFlow,
    CorporateSystemicModel,
    DomainNode,
    DomainRelation,
    RelationKind,
)


def build_model() -> CorporateSystemicModel:
    model = CorporateSystemicModel()
    for domain in ("COMERCIAL", "LICITACOES", "ORCAMENTO", "PROJETO", "COMPRAS", "PRODUCAO", "PCP", "LOGISTICA"):
        model.add_domain(DomainNode(domain_id=domain, name=domain))
    chain = [
        ("COMERCIAL", "ORCAMENTO"),
        ("ORCAMENTO", "PROJETO"),
        ("PROJETO", "COMPRAS"),
        ("COMPRAS", "PRODUCAO"),
        ("PRODUCAO", "PCP"),
        ("PCP", "LOGISTICA"),
    ]
    for source, target in chain:
        model.add_relation(
            DomainRelation(source, target, RelationKind.DEPENDS_ON, f"evidence://{source.lower()}-{target.lower()}", "2026-01-01")
        )
    return model


def test_corporate_chain_is_supported_with_evidence() -> None:
    result = build_model().analyze_flow(
        CorporateFlow("flow-1", ("COMERCIAL", "ORCAMENTO", "PROJETO", "COMPRAS", "PRODUCAO", "PCP", "LOGISTICA"), "source://flow-1", "tenant-a", "principal-1")
    )
    assert result.state is AnalysisState.SUPPORTED
    assert len(result.matched_relations) == 6
    assert len(result.evidence_refs) == 6


def test_missing_relation_is_inconclusive_not_fact() -> None:
    model = build_model()
    result = model.analyze_flow(
        CorporateFlow("flow-2", ("COMERCIAL", "LICITACOES", "ORCAMENTO"), "source://flow-2", "tenant-a", "principal-1")
    )
    assert result.state is AnalysisState.INCONCLUSIVE
    assert "missing relation: COMERCIAL->LICITACOES" in result.conflicts


def test_invalid_context_blocks_analysis() -> None:
    result = build_model().analyze_flow(
        CorporateFlow("flow-3", ("COMERCIAL", "ORCAMENTO"), "source://flow-3", "", "principal-1")
    )
    assert result.state is AnalysisState.BLOCKED


def test_relation_requires_evidence() -> None:
    model = build_model()
    try:
        model.add_relation(DomainRelation("COMERCIAL", "LICITACOES", RelationKind.DEPENDS_ON, "", "2026-01-01"))
    except ValueError:
        return
    raise AssertionError("a cross-domain relation without evidence must be rejected")
