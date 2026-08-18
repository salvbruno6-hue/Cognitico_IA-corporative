import pytest

from elo.core.cross_domain import CorporateDomain, CrossDomainGovernance, CrossDomainRelation


def relation(**overrides):
    values = dict(
        relation_id="r1",
        origin_domain=CorporateDomain.COMMERCIAL,
        destination_domain=CorporateDomain.BUDGET,
        relation_type="INFORMS",
        statement="commercial demand informs budget premise",
        tenant_id="tenant-a",
        principal_id="principal-a",
        source_id="source-1",
        evidence_ids=("e1",),
        valid_from="2026-08-18",
        confidence=0.9,
        provenance={
            "origin_domain": CorporateDomain.COMMERCIAL.value,
            "destination_domain": CorporateDomain.BUDGET.value,
        },
    )
    values.update(overrides)
    return CrossDomainRelation(**values)


def test_cross_domain_relation_preserves_distinct_domain_ownership_and_evidence():
    item = relation()
    result = CrossDomainGovernance().validate(item, expected_tenant_id="tenant-a")
    assert result.status == "VALID"
    assert item.origin_domain == CorporateDomain.COMMERCIAL
    assert item.destination_domain == CorporateDomain.BUDGET
    assert item.evidence_ids == ("e1",)


def test_cross_domain_relation_rejects_same_domain():
    with pytest.raises(ValueError):
        relation(destination_domain=CorporateDomain.COMMERCIAL)


def test_cross_domain_governance_blocks_tenant_mismatch_and_low_confidence():
    item = relation(confidence=0.4)
    result = CrossDomainGovernance().validate(item, expected_tenant_id="tenant-b")
    assert result.status == "BLOCKED"
    assert "tenant mismatch" in result.gaps
    assert "confidence below cross-domain threshold" in result.gaps


def test_cross_domain_governance_blocks_provenance_domain_conflict():
    item = relation(provenance={"origin_domain": CorporateDomain.PCP.value})
    result = CrossDomainGovernance().validate(item)
    assert result.status == "BLOCKED"
    assert "provenance origin domain mismatch" in result.gaps


def test_canonical_chain_keeps_commercial_tenders_and_budget_distinct():
    chain = CrossDomainGovernance.canonical_chain()
    assert (CorporateDomain.COMMERCIAL, CorporateDomain.TENDERS) in chain
    assert (CorporateDomain.TENDERS, CorporateDomain.BUDGET) in chain
    assert (CorporateDomain.COMMERCIAL, CorporateDomain.BUDGET) in chain
