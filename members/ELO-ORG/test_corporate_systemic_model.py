from members.ELO_ORG.corporate_systemic_model import (  # type: ignore[import-not-found]
    AnalysisState,
    CorporateFlow,
    CorporateSystemicModel,
    DomainNode,
    DomainRelation,
    RelationKind,
)


def model() -> CorporateSystemicModel:
    result = CorporateSystemicModel()
    for domain in ("COMERCIAL", "LICITACOES", "ORCAMENTO", "PROJETOS", "PRODUCAO", "PCP", "LOGISTICA"):
        result.add_domain(DomainNode(domain_id=domain, name=domain))
    return result


def test_comercial_to_orcamento_supported() -> None:
    result = model()
    result.add_relation(DomainRelation("COMERCIAL", "ORCAMENTO", RelationKind.SUPPLIES, "ev-1", "2026-01-01"))
    flow = CorporateFlow("f1", ("COMERCIAL", "ORCAMENTO"), "src-1", "tenant-a", "principal-a")
    assert result.analyze_flow(flow).state is AnalysisState.SUPPORTED


def test_comercial_licitacoes_orcamento_supported() -> None:
    result = model()
    result.add_relation(DomainRelation("COMERCIAL", "LICITACOES", RelationKind.DEPENDS_ON, "ev-1", "2026-01-01"))
    result.add_relation(DomainRelation("LICITACOES", "ORCAMENTO", RelationKind.IMPACTS, "ev-2", "2026-01-01"))
    flow = CorporateFlow("f2", ("COMERCIAL", "LICITACOES", "ORCAMENTO"), "src-2", "tenant-a", "principal-a")
    analysis = result.analyze_flow(flow)
    assert analysis.state is AnalysisState.SUPPORTED
    assert analysis.evidence_refs == ("ev-1", "ev-2")


def test_orcamento_projetos_producao_supported() -> None:
    result = model()
    result.add_relation(DomainRelation("ORCAMENTO", "PROJETOS", RelationKind.IMPACTS, "ev-3", "2026-01-01"))
    result.add_relation(DomainRelation("PROJETOS", "PRODUCAO", RelationKind.IMPACTS, "ev-4", "2026-01-01"))
    flow = CorporateFlow("f3", ("ORCAMENTO", "PROJETOS", "PRODUCAO"), "src-3", "tenant-a", "principal-a")
    assert result.analyze_flow(flow).state is AnalysisState.SUPPORTED


def test_pcp_producao_logistica_supported() -> None:
    result = model()
    result.add_relation(DomainRelation("PCP", "PRODUCAO", RelationKind.DEPENDS_ON, "ev-5", "2026-01-01"))
    result.add_relation(DomainRelation("PRODUCAO", "LOGISTICA", RelationKind.SUPPLIES, "ev-6", "2026-01-01"))
    flow = CorporateFlow("f4", ("PCP", "PRODUCAO", "LOGISTICA"), "src-4", "tenant-a", "principal-a")
    assert result.analyze_flow(flow).state is AnalysisState.SUPPORTED


def test_missing_relation_is_inconclusive_not_false() -> None:
    result = model()
    result.add_relation(DomainRelation("COMERCIAL", "ORCAMENTO", RelationKind.SUPPLIES, "ev-7", "2026-01-01"))
    flow = CorporateFlow("f5", ("COMERCIAL", "PCP"), "src-5", "tenant-a", "principal-a")
    analysis = result.analyze_flow(flow)
    assert analysis.state is AnalysisState.INCONCLUSIVE
    assert analysis.conflicts == ("missing relation: COMERCIAL->PCP",)


def test_missing_context_is_blocked() -> None:
    result = model()
    flow = CorporateFlow("f6", ("COMERCIAL", "ORCAMENTO"), "src-6", "", "principal-a")
    assert result.analyze_flow(flow).state is AnalysisState.BLOCKED


def test_cross_domain_relation_requires_evidence() -> None:
    result = model()
    relation = DomainRelation("COMERCIAL", "ORCAMENTO", RelationKind.SUPPLIES, "", "2026-01-01")
    try:
        result.add_relation(relation)
    except ValueError:
        pass
    else:
        raise AssertionError("relations without evidence must be rejected")
