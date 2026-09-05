import pytest

from elo.core.context_resolution import ContextEvidence, ContextPack, ContextQuery
from elo.core.gpt_handoff import GPTDecisionHandoff
from elo.core.maturity_engine import MaturityAssessment
from elo.core.source_discovery import DiscoveryPlan
from elo.core.specialist_skill_resolution import SpecialistSkill, SpecialistSkillResolver, skill_from_registry_record


def _mature() -> MaturityAssessment:
    return MaturityAssessment({dimension: 1.0 for dimension in (
        "enterprise_context", "end_to_end_process", "systemic_reasoning", "evidence_analysis",
        "decision_memory", "uncertainty_management", "outcome_feedback",
    )})


def _context(domain: str = "BUDGETING") -> ContextPack:
    query = ContextQuery(
        "validar orçamento", entity="SO-TEST", domain=domain,
        tenant_id="tenant", principal_id="principal", request_id="req",
    )
    return ContextPack(
        query=query,
        discovery_plan=DiscoveryPlan("budget", (), (), (), metadata={}),
        sources=(),
        evidence=(ContextEvidence("budget-source", "custo evidenciado", 0.9, tenant_id="tenant", domain=domain),),
    )


def test_budgeting_domain_resolves_registered_governed_skill():
    resolver = SpecialistSkillResolver((
        SpecialistSkill("FORGE-BUDGETING-001", "BUDGETING", "GOVERNED"),
    ))
    result = resolver.resolve(domain_family="BUDGETING", authorized=lambda skill: True)
    assert result.resolved
    assert result.skill_id == "FORGE-BUDGETING-001"


def test_missing_skill_is_an_explicit_gap_not_an_invented_skill():
    result = SpecialistSkillResolver(()).resolve(domain_family="HR")
    assert result.status == "GAP"
    assert result.skill_id is None


def test_unauthorized_skill_is_blocked():
    skill = SpecialistSkill("FORGE-BUDGETING-001", "BUDGETING", "GOVERNED")
    result = SpecialistSkillResolver((skill,)).resolve(domain_family="BUDGETING", authorized=lambda _: False)
    assert result.status == "BLOCKED"
    assert result.skill_id is None


def test_handoff_requires_and_carries_resolved_skill_for_specialist_validation():
    context = _context()
    resolution = SpecialistSkillResolver((
        SpecialistSkill("FORGE-BUDGETING-001", "BUDGETING", "GOVERNED"),
    )).resolve(domain_family="BUDGETING", authorized=lambda _: True)
    handoff = GPTDecisionHandoff.from_context(
        objective="validar", context=context, maturity=_mature(), skill_resolution=resolution,
    )
    assert handoff.skill_id == "FORGE-BUDGETING-001"
    assert handoff.consultation_payload()["skill_id"] == "FORGE-BUDGETING-001"


def test_handoff_rejects_specialist_validation_without_skill():
    with pytest.raises(ValueError, match="resolved governed skill"):
        GPTDecisionHandoff.from_context(
            objective="validar", context=_context(), maturity=_mature(),
        )


def test_handoff_rejects_skill_from_wrong_domain():
    resolution = SpecialistSkillResolver((
        SpecialistSkill("FORGE-PCP-001", "PCP", "GOVERNED"),
    )).resolve(domain_family="PCP", authorized=lambda _: True)
    with pytest.raises(ValueError, match="domain"):
        GPTDecisionHandoff.from_context(
            objective="validar", context=_context("BUDGETING"), maturity=_mature(),
            skill_resolution=resolution,
        )


def test_registry_record_adapter_does_not_change_authority_boundary():
    skill = skill_from_registry_record({
        "skill_id": "FORGE-BUDGETING-001",
        "domain_family": "BUDGETING",
        "maturity": "GOVERNED",
        "authorization_required": True,
    })
    assert skill.skill_id == "FORGE-BUDGETING-001"
    assert skill.authorization_required is True
