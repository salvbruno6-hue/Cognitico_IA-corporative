from elo.core.specialist_skill_resolution import (
    SpecialistSkill,
    SpecialistSkillResolver,
    skill_from_registry_record,
)


def test_exact_domain_and_maturity_resolution_is_deterministic() -> None:
    resolver = SpecialistSkillResolver(
        [
            SpecialistSkill("SKILL-B", "BUDGETING", "GOVERNED", authorization_required=False),
            SpecialistSkill("SKILL-A", "BUDGETING", "STRUCTURED", authorization_required=False),
        ]
    )
    result = resolver.resolve(domain_family="BUDGETING", minimum_maturity="STRUCTURED")
    assert result.resolved is True
    assert result.skill_id == "SKILL-B"
    assert result.maturity == "GOVERNED"


def test_unknown_domain_is_gap() -> None:
    result = SpecialistSkillResolver([]).resolve(domain_family="UNKNOWN")
    assert result.status == "GAP"
    assert result.resolved is False


def test_unknown_minimum_maturity_is_blocked() -> None:
    result = SpecialistSkillResolver([]).resolve(
        domain_family="BUDGETING", minimum_maturity="NOT_A_REAL_MATURITY"
    )
    assert result.status == "BLOCKED"


def test_authorization_is_external_and_can_block() -> None:
    skill = SpecialistSkill("SKILL-A", "BUDGETING", "GOVERNED", authorization_required=True)
    result = SpecialistSkillResolver([skill]).resolve(
        domain_family="BUDGETING", authorized=lambda _: False
    )
    assert result.status == "BLOCKED"
    assert result.resolved is False


def test_record_adapter_requires_identity_fields() -> None:
    skill = skill_from_registry_record(
        {
            "skill_id": "FORGE-BUDGETING-001",
            "domain_family": "BUDGETING",
            "maturity": "GOVERNED",
            "scope": "budgeting",
            "boundaries": "recommendation only",
            "authorization_required": True,
        }
    )
    assert skill.skill_id == "FORGE-BUDGETING-001"
    assert skill.domain_family == "BUDGETING"
    assert skill.maturity == "GOVERNED"
