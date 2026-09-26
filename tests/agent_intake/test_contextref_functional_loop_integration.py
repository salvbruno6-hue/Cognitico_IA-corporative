from src.elo.agent_intake.contextref_functional_loop_integration import run_contextref_functional_loop_probe


def test_contextref_functional_loop_reaches_evolution_gate():
    implementation, evidence = run_contextref_functional_loop_probe()
    assert implementation.status == "READY_FOR_ELO_REVIEW"
    assert evidence.metric_directions["unsafe_malformed_reference_admission_rate"] == "minimize"
    assert evidence.baseline["unsafe_malformed_reference_admission_rate"] == 0.4
    assert evidence.adapted["unsafe_malformed_reference_admission_rate"] == 0.0
    assert evidence.boundary_integrity is True
