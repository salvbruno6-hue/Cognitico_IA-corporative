from elo.agent_intake.hermes_multiagent_evaluation import evaluate

def test_multiagent_three_phase_evidence():
    result = evaluate()
    assert result.baseline_rate == 0.0
    assert result.adapted_rate == 1.0
    assert result.boundary_integrity_rate == 1.0
    assert result.repeatable is True
    assert result.result == "EVOLUTION_GATE_REQUIRED"
