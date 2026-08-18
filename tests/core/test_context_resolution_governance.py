import pytest

from elo.core.context_resolution import (
    ContextEvidence,
    ContextQuery,
    ContextResolutionEngine,
    ContextSource,
)


def test_context_pack_preserves_tenant_domain_principal_and_request_context():
    engine = ContextResolutionEngine()
    pack = engine.resolve(
        ContextQuery(
            question="avaliar projeto",
            tenant_id="tenant-a",
            domain="PROJECTS",
            principal_id="principal-a",
            session_id="session-a",
            request_id="request-a",
            correlation_id="corr-a",
        )
    )
    assert pack.query.tenant_id == "tenant-a"
    assert pack.query.domain == "PROJECTS"
    assert pack.query.principal_id == "principal-a"
    assert pack.query.correlation_id == "corr-a"
    assert "retrieval pending" in pack.integrity_gaps()


def test_context_scoping_rejects_cross_tenant_and_cross_domain_evidence():
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery("avaliar", tenant_id="tenant-a", domain="PROJECTS"))
    pack = engine.enrich(
        pack,
        sources=(
            ContextSource("a", "document", "external", tenant_id="tenant-a", domain="PROJECTS"),
            ContextSource("b", "document", "external", tenant_id="tenant-b", domain="PROJECTS"),
            ContextSource("c", "document", "external", tenant_id="tenant-a", domain="BUDGET"),
        ),
        evidence=(
            ContextEvidence("a", "valid project fact", 0.9, tenant_id="tenant-a", domain="PROJECTS"),
            ContextEvidence("b", "other tenant fact", 0.9, tenant_id="tenant-b", domain="PROJECTS"),
            ContextEvidence("c", "other domain fact", 0.9, tenant_id="tenant-a", domain="BUDGET"),
        ),
    )
    assert pack.evidence_ids() == ("a",)


def test_principal_scoping_rejects_evidence_from_another_principal():
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery("avaliar", tenant_id="tenant-a", principal_id="principal-a"))
    pack = engine.enrich(
        pack,
        sources=(ContextSource("s1", "document", "external", tenant_id="tenant-a"),),
        evidence=(
            ContextEvidence(
                "s1",
                "restricted fact",
                0.9,
                tenant_id="tenant-a",
                provenance={"principal_id": "principal-b"},
            ),
        ),
    )
    assert pack.evidence_ids() == ()
    assert "evidence is not authorized for requested principal" in pack.integrity_gaps()


def test_context_evidence_confidence_is_bounded():
    with pytest.raises(ValueError):
        ContextEvidence("s1", "fact", 1.1)


def test_consultation_payload_separates_evidence_gaps_and_decision_need():
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery("avaliar", tenant_id="tenant-a", request_id="r1", correlation_id="c1"))
    payload = pack.consultation_payload()
    assert payload["request_id"] == "r1"
    assert payload["correlation_id"] == "c1"
    assert "evidence" in payload
    assert "gaps" in payload
    assert payload["requires_human_decision"] is True
