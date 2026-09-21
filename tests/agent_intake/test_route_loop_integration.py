from elo.agent_intake.route_loop_integration import run_route_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage
def test_route_probe_preserves_retest_when_no_incremental_gain():
    decision, evidence = run_route_loop_probe()
    assert evidence.baseline["successful_policy_routed_execution_rate"] == 1.0
    assert evidence.adapted["successful_policy_routed_execution_rate"] == 1.0
    assert evidence.repeatable is True
    assert evidence.regressions == ()
    assert evidence.boundary_integrity is True
    assert evidence.is_complete() is True
    assert decision.stage is ImplementationStage.MEASURED_GAIN
    assert decision.result == "RETEST"
    assert decision.canonical_mutation is False
