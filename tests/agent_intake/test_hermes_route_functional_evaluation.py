from elo.agent_intake.hermes_route_functional_evaluation import evaluate_route_functional_gain

def test_route_candidate_blocks_unsafe_admission():
    evidence = evaluate_route_functional_gain()
    assert evidence.baseline_unsafe_route_admission_block_rate == 0.0
    assert evidence.adapted_unsafe_route_admission_block_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.provenance_refs
