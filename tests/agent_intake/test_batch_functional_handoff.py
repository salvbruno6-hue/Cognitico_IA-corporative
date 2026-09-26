from elo.agent_intake.batch_loop_integration import run_batch_loop_probe

def test_batch_functional_gain_reaches_governed_review():
    decision, evidence = run_batch_loop_probe()
    assert evidence.adapted["collision_free_batch_task_rate"] == 1.0
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
