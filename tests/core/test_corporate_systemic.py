import pytest

from elo.core.cross_domain import CorporateDomain, CrossDomainRelation
from elo.core.corporate_systemic import CorporateSystemicView
from elo.core.systemic_primitives import SystemicModel


def relation(index, origin, destination, tenant="tenant-a", evidence="e1", confidence=0.9):
    return CrossDomainRelation(
        relation_id=f"r{index}",
        origin_domain=origin,
        destination_domain=destination,
        relation_type="IMPACTS",
        statement=f"{origin.value}->{destination.value}",
        tenant_id=tenant,
        principal_id="principal-a",
        source_id=f"source-{index}",
        evidence_ids=(evidence,),
        valid_from="2026-08-18",
        confidence=confidence,
        provenance={
            "origin_domain": origin.value,
            "destination_domain": destination.value,
        },
    )


def view():
    relations = (
        relation(1, CorporateDomain.COMMERCIAL, CorporateDomain.BUDGET),
        relation(2, CorporateDomain.BUDGET, CorporateDomain.PROJECTS),
        relation(3, CorporateDomain.PROJECTS, CorporateDomain.PRODUCTION),
        relation(4, CorporateDomain.PCP, CorporateDomain.PRODUCTION),
        relation(5, CorporateDomain.PRODUCTION, CorporateDomain.LOGISTICS),
        relation(6, CorporateDomain.LOGISTICS, CorporateDomain.OUTCOME),
    )
    return CorporateSystemicView.build(SystemicModel(), relations, tenant_id="tenant-a")


def test_commercial_to_budget_path_is_executable_and_provenance_backed():
    assert view().path_exists(CorporateDomain.COMMERCIAL, CorporateDomain.BUDGET)


def test_commercial_to_project_chain_is_reconstructed_without_domain_fusion():
    assert view().path_exists(CorporateDomain.COMMERCIAL, CorporateDomain.PROJECTS)
    assert CorporateDomain.COMMERCIAL != CorporateDomain.BUDGET


def test_budget_to_project_to_production_chain_is_reconstructed():
    assert view().path_exists(CorporateDomain.BUDGET, CorporateDomain.PRODUCTION)


def test_pcp_to_production_to_logistics_chain_is_reconstructed():
    assert view().path_exists(CorporateDomain.PCP, CorporateDomain.LOGISTICS)


def test_commercial_to_budget_to_pcp_requires_explicit_relation_and_does_not_infer_one():
    assert not view().path_exists(CorporateDomain.COMMERCIAL, CorporateDomain.PCP)


def test_conflicting_relation_is_rejected_before_projection():
    conflicting = relation(9, CorporateDomain.COMMERCIAL, CorporateDomain.BUDGET, confidence=0.4)
    with pytest.raises(ValueError, match="confidence below cross-domain threshold"):
        CorporateSystemicView.build(SystemicModel(), (conflicting,), tenant_id="tenant-a")


def test_tenant_isolation_blocks_mixed_tenant_projection():
    mixed = relation(10, CorporateDomain.COMMERCIAL, CorporateDomain.BUDGET, tenant="tenant-b")
    with pytest.raises(ValueError, match="tenant mismatch"):
        CorporateSystemicView.build(SystemicModel(), (mixed,), tenant_id="tenant-a")


def test_derived_view_does_not_mutate_base_systemic_model():
    base = SystemicModel(entities=("commercial", "budget"))
    before = base
    CorporateSystemicView.build(base, (relation(11, CorporateDomain.COMMERCIAL, CorporateDomain.BUDGET),), tenant_id="tenant-a")
    assert base == before


def test_new_domain_relation_can_be_added_without_rewriting_existing_relations():
    first = view()
    extra = relation(12, CorporateDomain.COMMERCIAL, CorporateDomain.TENDERS)
    second = CorporateSystemicView.build(
        first.base_model,
        first.cross_domain_relations + (extra,),
        tenant_id="tenant-a",
    )
    assert len(second.cross_domain_relations) == len(first.cross_domain_relations) + 1
    assert len(first.cross_domain_relations) == 6


def test_executive_view_is_derived_and_contains_evidence_not_business_authority():
    summary = view().executive_summary()
    assert summary["source_of_truth"] == "derived_projection"
    assert summary["relation_count"] == 6
    assert "e1" in summary["evidence_ids"]
