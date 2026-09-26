from elo.agent_intake.hermes_memory_provider_functional_evaluation import evaluate_memory_provider_functional_gain

def test_memory_provider_candidate_preserves_provider_evidence_identity():
    evidence = evaluate_memory_provider_functional_gain()
    assert evidence.baseline_identity_preservation_rate == 0.0
    assert evidence.adapted_identity_preservation_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
