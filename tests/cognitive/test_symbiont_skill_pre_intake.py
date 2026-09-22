from elo.core.specialist_skill_resolution import SkillPreIntakeComponent, SpecialistSkill
from elo.cognitive.symbiont_operational_contract import SymbiontRequestGuard, SymbiontOperation
from elo.cognitive.symbiont_skill_runtime import SymbiontSkillRuntime


def guard(**overrides):
    values = dict(
        request_id="req-1",
        tenant_scope="tenant-a",
        acknowledged=True,
        authorized=True,
    )
    values.update(overrides)
    return SymbiontRequestGuard(**values)


def test_skill_001_is_runnable_through_runtime_adapter():
    SymbiontSkillRuntime.validate_boundary(guard())


def test_skill_001_remains_fail_closed():
    SymbiontSkillRuntime.validate_boundary(guard(high_risk=True))
    assert guard(high_risk=True).human_escalation().required is True


def test_skill_001_operation_dispatch_uses_canonical_contract():
    assert SymbiontSkillRuntime.validate_operation("query") == SymbiontOperation.QUERY.value


def test_runtime_exposes_all_four_skill_paths():
    assert callable(SymbiontSkillRuntime.validate_boundary)
    assert callable(SymbiontSkillRuntime.handoff_decision)
    assert callable(SymbiontSkillRuntime.evaluate_lab)
    assert callable(SymbiontSkillRuntime.propose_capability)


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


def test_runtime_pre_intake_reuses_existing_skill():
    result = SymbiontSkillRuntime.pre_intake_skill(
        skills=(
            SpecialistSkill("FORGE-BUDGETING-001", "BUDGETING", "GOVERNED", authorization_required=False),
        ),
        skill_id="ELO-KE-SKILL-EXAMPLE-001",
        domain_family="BUDGETING",
        required_components=(SkillPreIntakeComponent("memory", "FOUND"),),
    )
    assert result.decision == "REUSE_EXISTING"
    assert result.existing_skill_id == "FORGE-BUDGETING-001"
