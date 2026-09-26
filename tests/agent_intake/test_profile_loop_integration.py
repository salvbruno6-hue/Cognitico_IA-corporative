from elo.agent_intake.profile_loop_integration import run_profile_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage

def test_profile_probe_preserves_retest_when_no_incremental_gain():
    decision, evidence = run_profile_loop_probe()
    metric = "bounded_profile_isolation_integrity_rate"
    assert evidence.baseline[metric] == 0.0
    assert evidence.adapted[metric] == 1.0
    assert evidence.repeatable is True and evidence.regressions == ()
    assert evidence.boundary_integrity is True and evidence.is_complete() is True
    assert decision.stage is ImplementationStage.MEASURED_GAIN
    assert decision.result == "RETEST"
    assert decision.canonical_mutation is False
