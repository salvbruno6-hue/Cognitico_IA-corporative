from datetime import datetime, timezone

import pytest

from elo.members import ELOOrgMember, ResultStatus, StructuralAssertion


TENANT = "tenant-a"
PROVENANCE = "doc:org-model:v1#pcp-produces"


def assertion(
    *,
    source_domain: str = "PCP",
    target_domain: str = "Produção",
    relation: str = "provides",
    source_id: str = "pcp",
    target_id: str = "production",
    tenant_id: str = TENANT,
    provenance: str = PROVENANCE,
    valid_from: datetime | None = None,
    valid_to: datetime | None = None,
) -> StructuralAssertion:
    return StructuralAssertion(
        assertion_id=f"a-{source_id}-{target_id}",
        tenant_id=tenant_id,
        source_domain=source_domain,
        target_domain=target_domain,
        relation=relation,
        source_id=source_id,
        target_id=target_id,
        provenance=provenance,
        owner="org-governance",
        valid_from=valid_from,
        valid_to=valid_to,
    )


def test_org_001_identity_and_version() -> None:
    member = ELOOrgMember()
    health = member.health()
    assert health == {"member_id": "ELO-ORG", "version": "1.0.0", "status": "ACTIVE"}


def test_org_002_capability_discovery_is_bounded() -> None:
    assert "organizational_structure" in ELOOrgMember.capabilities
    assert "decision_governance" not in ELOOrgMember.capabilities
    assert "provider_orchestration" not in ELOOrgMember.capabilities


def test_org_003_missing_provenance_is_blocked() -> None:
    member = ELOOrgMember([assertion(provenance="")])
    result = member.query(tenant_id=TENANT, source_domain="PCP", target_domain="Produção", relation="provides")
    assert result.status is ResultStatus.BLOCKED


def test_org_004_tenant_isolation() -> None:
    member = ELOOrgMember([assertion(tenant_id="tenant-b")])
    result = member.query(tenant_id=TENANT, source_domain="PCP", target_domain="Produção", relation="provides")
    assert result.status is ResultStatus.INCONCLUSIVE
    assert result.assertions == ()


def test_org_005_domain_scope() -> None:
    member = ELOOrgMember([assertion()])
    result = member.query(tenant_id=TENANT, source_domain="Compras", target_domain="Produção", relation="provides")
    assert result.status is ResultStatus.INCONCLUSIVE


def test_org_006_conflicting_structural_assertions_are_not_overwritten() -> None:
    member = ELOOrgMember(
        [
            assertion(target_id="production-a", provenance="doc:a"),
            assertion(target_id="production-b", provenance="doc:b", source_id="pcp"),
        ]
    )
    result = member.query(tenant_id=TENANT, source_domain="PCP", target_domain="Produção", relation="provides")
    assert result.status is ResultStatus.CONFLICTING
    assert {a.target_id for a in result.assertions} == {"production-a", "production-b"}


def test_org_007_temporal_validity() -> None:
    member = ELOOrgMember(
        [
            assertion(
                valid_from=datetime(2026, 1, 1, tzinfo=timezone.utc),
                valid_to=datetime(2026, 6, 1, tzinfo=timezone.utc),
            )
        ]
    )
    result = member.query(
        tenant_id=TENANT,
        source_domain="PCP",
        target_domain="Produção",
        relation="provides",
        at=datetime(2026, 3, 1, tzinfo=timezone.utc),
    )
    assert result.status is ResultStatus.SUPPORTED


def test_org_008_unavailable_member_has_no_synthetic_pass() -> None:
    member = ELOOrgMember()
    result = member.query(tenant_id=TENANT, source_domain="PCP", target_domain="Produção", relation="provides")
    assert result.status is ResultStatus.INCONCLUSIVE
    assert result.confidence is None


def test_org_009_malformed_scope_is_blocked() -> None:
    member = ELOOrgMember([assertion()])
    result = member.query(tenant_id=TENANT, source_domain="", target_domain="Produção", relation="provides")
    assert result.status is ResultStatus.BLOCKED


def test_org_010_contract_result_contains_version_scope_and_evidence() -> None:
    member = ELOOrgMember([assertion()])
    result = member.query(tenant_id=TENANT, source_domain="PCP", target_domain="Produção", relation="provides")
    assert result.status is ResultStatus.SUPPORTED
    assert result.member_id == "ELO-ORG"
    assert result.member_version == "1.0.0"
    assert result.scope == "PCP->Produção"
    assert result.evidence_refs == (PROVENANCE,)


@pytest.mark.parametrize(
    ("source", "target", "relation"),
    [
        ("Comercial", "Orçamento", "requests_quote"),
        ("Licitações", "Orçamento", "defines_requirement"),
        ("Orçamento", "Projetos / Engenharia", "technical_dependency"),
        ("Projetos / Engenharia", "Produção", "depends_on"),
        ("Compras / Suprimentos", "Produção", "provides"),
        ("PCP", "Produção", "provides"),
        ("Produção", "Logística / Expedição", "provides"),
    ],
)
def test_org_011_to_017_cross_domain_semantics_are_distinct(source: str, target: str, relation: str) -> None:
    member = ELOOrgMember([assertion(source_domain=source, target_domain=target, relation=relation)])
    result = member.query(tenant_id=TENANT, source_domain=source, target_domain=target, relation=relation)
    assert result.status is ResultStatus.SUPPORTED
    assert result.assertions[0].relation == relation


def test_org_018_result_to_learning_is_not_structural_ownership() -> None:
    member = ELOOrgMember([assertion(source_domain="Resultado", target_domain="Learning", relation="derived_from")])
    result = member.query(tenant_id=TENANT, source_domain="Resultado", target_domain="Learning", relation="derived_from")
    assert result.status is ResultStatus.SUPPORTED
    assert result.assertions[0].owner == "org-governance"


def test_org_019_full_cross_domain_chain_preserves_provenance_and_tenant() -> None:
    relations = [
        ("Licitações", "Orçamento", "defines_requirement"),
        ("Orçamento", "Projetos / Engenharia", "technical_dependency"),
        ("Projetos / Engenharia", "Produção", "depends_on"),
        ("Produção", "Logística / Expedição", "provides"),
    ]
    assertions = [
        assertion(source_domain=s, target_domain=t, relation=r, source_id=s, target_id=t, provenance=f"doc:{i}")
        for i, (s, t, r) in enumerate(relations)
    ]
    member = ELOOrgMember(assertions)
    for source, target, relation in relations:
        result = member.query(tenant_id=TENANT, source_domain=source, target_domain=target, relation=relation)
        assert result.status is ResultStatus.SUPPORTED
        assert result.assertions[0].tenant_id == TENANT
        assert result.evidence_refs


def test_org_020_invalid_temporal_window_is_inconclusive() -> None:
    member = ELOOrgMember(
        [
            assertion(
                valid_from=datetime(2026, 7, 1, tzinfo=timezone.utc),
                valid_to=datetime(2026, 8, 1, tzinfo=timezone.utc),
            )
        ]
    )
    result = member.query(
        tenant_id=TENANT,
        source_domain="PCP",
        target_domain="Produção",
        relation="provides",
        at=datetime(2026, 9, 1, tzinfo=timezone.utc),
    )
    assert result.status is ResultStatus.INCONCLUSIVE
