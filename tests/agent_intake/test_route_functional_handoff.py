from elo.agent_intake.route_loop_integration import run_route_loop_probe

def test_route_functional_gain_reaches_governed_review():
    decision, evidence = run_route_loop_probe()
    assert evidence.adapted["unsafe_route_admission_block_rate"] == 1.0
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
