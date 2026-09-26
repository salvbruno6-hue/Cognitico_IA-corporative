from elo.agent_intake.learning_loop_integration import run_learning_loop_probe

def test_learn_functional_gain_reaches_governed_review():
    decision, evidence = run_learning_loop_probe()
    assert evidence.adapted["unsafe_skill_admission_block_rate"] == 1.0
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
