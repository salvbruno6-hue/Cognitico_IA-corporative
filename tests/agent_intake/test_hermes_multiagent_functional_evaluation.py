from elo.agent_intake.hermes_multiagent_functional_evaluation import evaluate_multiagent_functional_gain

def test_multiagent_candidate_has_context_isolation_gain():
    evidence = evaluate_multiagent_functional_gain()
    assert evidence.baseline_context_isolation_rate == 0.0
    assert evidence.adapted_context_isolation_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
