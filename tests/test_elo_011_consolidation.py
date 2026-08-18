from datetime import datetime
from decimal import Decimal

from elo.core.context_resolution import ContextEvidence, ContextPack, ContextQuery
from elo.core.cross_domain import CorporateDomain, CrossDomainRelation


def build_context(tenant="tenant-a"):
    query = ContextQuery(
        intent="budgeting",
        tenant_id=tenant,
        domain="ORCAMENTO",
        principal_id="principal-a",
        request_id="request-a",
        correlation_id="corr-a",
    )
    evidence = ContextEvidence(
        source_id="budget-source-1",
        fact="budget evidence",
        confidence=0.9,
        tenant_id=tenant,
        domain="ORCAMENTO",
        principal_id="principal-a",
    )
    return ContextPack(query=query, sources=(), evidence=(evidence,))


def test_context_blocks_cross_tenant_evidence():
    pack = build_context(tenant="tenant-a")
    foreign = ContextEvidence(
        source_id="foreign-source",
        fact="foreign evidence",
        confidence=0.99,
        tenant_id="tenant-b",
        domain="ORCAMENTO",
    )
    restricted = ContextPack(query=pack.query, sources=pack.sources, evidence=(foreign,))
    assert restricted.scoped_evidence() == ()
    assert "tenant" in " ".join(restricted.integrity_gaps())


def test_cross_domain_relation_preserves_provenance_and_rejects_tenant_mismatch():
    relation = CrossDomainRelation(
        relation_id="r-011",
        origin_domain=CorporateDomain.COMMERCIAL,
        destination_domain=CorporateDomain.BUDGET,
        relation_type="INFORMS",
        statement="commercial demand informs budget premise",
        tenant_id="tenant-a",
        principal_id="principal-a",
        source_id="commercial-source",
        evidence_id="evidence-a",
        provenance={"source": "test"},
        confidence=0.9,
    )
    assert relation.tenant_id == "tenant-a"
    assert relation.provenance["source"] == "test"
