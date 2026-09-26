from elo.agent_intake.hermes_batch_functional_evaluation import evaluate_batch_functional_gain

def test_batch_candidate_proves_collision_free_task_identity():
    evidence = evaluate_batch_functional_gain()
    assert evidence.baseline_collision_free_batch_task_rate == 0.0
    assert evidence.adapted_collision_free_batch_task_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
