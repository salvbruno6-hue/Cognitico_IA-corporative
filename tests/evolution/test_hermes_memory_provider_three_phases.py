from elo.agent_intake.hermes_memory_provider_evaluation import evaluate


def test_memory_provider_three_phase_controlled_evaluation():
    result = evaluate()
    assert result.baseline_rate == 0.0
    assert result.adapted_rate == 1.0
    assert result.boundary_integrity_rate == 1.0
    assert result.repeatable is True
    assert result.result == "EVOLUTION_GATE_REQUIRED"
