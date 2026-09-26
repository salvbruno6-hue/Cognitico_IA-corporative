from elo.agent_intake.hermes_learning_functional_evaluation import evaluate_learning_functional_gain

def test_learn_candidate_blocks_unverified_skill_admission():
    evidence = evaluate_learning_functional_gain()
    assert evidence.baseline_unsafe_admission_block_rate == 0.0
    assert evidence.adapted_unsafe_admission_block_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
