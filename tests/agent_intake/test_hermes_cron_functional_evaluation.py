from elo.agent_intake.hermes_cron_functional_evaluation import evaluate_cron_functional_gain

def test_cron_candidate_has_idempotency_collision_gain():
    evidence = evaluate_cron_functional_gain()
    assert evidence.baseline_idempotency_collision_free_rate == 0.0
    assert evidence.adapted_idempotency_collision_free_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
