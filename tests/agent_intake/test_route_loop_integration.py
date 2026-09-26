from elo.agent_intake.route_loop_integration import run_route_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage

def test_route_probe_preserves_retest_when_no_incremental_gain():
    decision, evidence = run_route_loop_probe()
    metric = "unsafe_route_admission_block_rate"
    assert evidence.baseline[metric] == 0.0
    assert evidence.adapted[metric] == 1.0
    assert evidence.repeatable is True
    assert evidence.regressions == ()
    assert evidence.boundary_integrity is True
    assert evidence.is_complete() is True
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
