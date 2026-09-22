from elo.core.specialist_skill_resolution import SkillPreIntakeComponent, SpecialistSkill
from elo.cognitive.symbiont_skill_runtime import SymbiontSkillRuntime


def test_runtime_exposes_skill_pre_intake_before_creation():
    result = SymbiontSkillRuntime.pre_intake_skill(
        skills=(),
        skill_id="ELO-KE-SKILL-EXAMPLE-001",
        domain_family="BUDGETING",
        required_components=(
            SkillPreIntakeComponent("memory", "FOUND"),
            SkillPreIntakeComponent("precedent_search", "MISSING", gap="build first"),
        ),
    )
    assert result.decision == "DEVELOP_FIRST"
    assert result.ready_for_intake is False
    assert result.readiness_score == 0.5


def test_runtime_pre_intake_reuses_existing_skill():
    result = SymbiontSkillRuntime.pre_intake_skill(
        skills=(
            SpecialistSkill(
                "FORGE-BUDGETING-001",
                "BUDGETING",
                "GOVERNED",
                authorization_required=False,
            ),
        ),
        skill_id="ELO-KE-SKILL-EXAMPLE-001",
        domain_family="BUDGETING",
        required_components=(SkillPreIntakeComponent("memory", "FOUND"),),
    )
    assert result.decision == "REUSE_EXISTING"
    assert result.existing_skill_id == "FORGE-BUDGETING-001"
