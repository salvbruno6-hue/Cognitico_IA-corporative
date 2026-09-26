from elo.agent_intake.profile_loop_integration import run_profile_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage

def test_profile_probe_reaches_governed_review_with_functional_gain():
    decision, evidence = run_profile_loop_probe()
    metric = "collision_free_profile_task_rate"
    assert evidence.baseline[metric] == 0.0
    assert evidence.adapted[metric] == 1.0
    assert evidence.repeatable is True and evidence.regressions == ()
    assert evidence.boundary_integrity is True and evidence.is_complete() is True
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
