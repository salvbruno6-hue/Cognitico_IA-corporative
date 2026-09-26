from elo.agent_intake.hermes_cron_evaluation import evaluate


def test_cron_three_phase_controlled_evaluation():
    result = evaluate()
    assert result.baseline_rate == 0.0
    assert result.adapted_rate == 1.0
    assert result.boundary_integrity_rate == 1.0
    assert result.repeatable is True
    assert result.result == "EVOLUTION_GATE_REQUIRED"
