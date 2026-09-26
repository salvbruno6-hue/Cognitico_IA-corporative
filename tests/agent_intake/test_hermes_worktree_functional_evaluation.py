from src.elo.agent_intake.hermes_worktree_functional_evaluation import evaluate_worktree_functional_gain

def test_worktree_candidate_has_candidate_specific_collision_free_gain():
    evidence = evaluate_worktree_functional_gain()
    assert evidence.baseline_collision_free_rate == 0.0
    assert evidence.adapted_collision_free_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
