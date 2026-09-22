from elo.core.specialist_skill_resolution import (
    SkillPreIntakeComponent,
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


def test_pre_intake_develops_first_when_a_required_component_is_missing() -> None:
    result = SpecialistSkillResolver([]).pre_intake(
        skill_id="ELO-KE-SKILL-EXAMPLE-001",
        domain_family="BUDGETING",
        required_components=(
            SkillPreIntakeComponent("memory", "FOUND", "src/elo/cognitive/memory"),
            SkillPreIntakeComponent(
                "precedent_search",
                "MISSING",
                gap="no reusable precedent search mechanism found",
            ),
        ),
    )
    assert result.status == "BLOCKED"
    assert result.decision == "DEVELOP_FIRST"
    assert result.readiness_score == 0.5
    assert result.develop_first is True


def test_pre_intake_is_ready_when_all_components_exist_and_no_duplicate_exists() -> None:
    result = SpecialistSkillResolver([]).pre_intake(
        skill_id="ELO-KE-SKILL-NEW-001",
        domain_family="BUDGETING",
        required_components=(
            SkillPreIntakeComponent("memory", "FOUND", "memory"),
            SkillPreIntakeComponent("precedent_search", "FOUND", "precedent"),
            SkillPreIntakeComponent("human_response", "FOUND", "humanizer"),
            SkillPreIntakeComponent("evolution_gate", "FOUND", "gate"),
        ),
    )
    assert result.status == "READY"
    assert result.decision == "READY_FOR_INTAKE"
    assert result.readiness_score == 1.0
    assert result.ready_for_intake is True


def test_pre_intake_reuses_existing_governed_skill_instead_of_creating_duplicate() -> None:
    existing = SpecialistSkill(
        "FORGE-BUDGETING-001",
        "BUDGETING",
        "GOVERNED",
        authorization_required=False,
    )
    result = SpecialistSkillResolver([existing]).pre_intake(
        skill_id="ELO-KE-SKILL-EXAMPLE-001",
        domain_family="BUDGETING",
        required_components=(
            SkillPreIntakeComponent("memory", "FOUND"),
            SkillPreIntakeComponent("precedent_search", "FOUND"),
        ),
    )
    assert result.status == "REUSE_EXISTING"
    assert result.decision == "REUSE_EXISTING"
    assert result.existing_skill_id == "FORGE-BUDGETING-001"
    assert result.reuse_existing is True
