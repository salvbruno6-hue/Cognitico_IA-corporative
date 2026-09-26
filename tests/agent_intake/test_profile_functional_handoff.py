from elo.agent_intake.profile_loop_integration import run_profile_loop_probe

def test_profile_functional_gain_reaches_governed_review():
    decision, evidence = run_profile_loop_probe()
    assert evidence.adapted["collision_free_profile_task_rate"] == 1.0
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
