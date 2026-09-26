from elo.agent_intake.batch_loop_integration import run_batch_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage

def test_batch_probe_reaches_governed_review_with_functional_gain():
    decision, evidence = run_batch_loop_probe()
    assert evidence.baseline["collision_free_batch_task_rate"] == 0.0
    assert evidence.adapted["collision_free_batch_task_rate"] == 1.0
    assert evidence.repeatable is True and evidence.regressions == ()
    assert evidence.boundary_integrity is True and evidence.is_complete() is True
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
