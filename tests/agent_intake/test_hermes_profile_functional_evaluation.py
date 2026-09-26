from elo.agent_intake.hermes_profile_functional_evaluation import evaluate_profile_functional_gain

def test_profile_candidate_proves_collision_free_task_isolation():
    evidence = evaluate_profile_functional_gain()
    assert evidence.baseline_collision_free_profile_task_rate == 0.0
    assert evidence.adapted_collision_free_profile_task_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
