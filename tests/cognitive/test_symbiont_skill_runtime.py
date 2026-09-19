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
