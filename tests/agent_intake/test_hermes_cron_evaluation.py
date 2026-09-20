from src.elo.agent_intake.hermes_cron_evaluation import evaluate

def test_cron_controlled_evaluation_is_deterministic_and_bounded():
    result=evaluate()
    assert result.baseline_rate==1.0
    assert result.adapted_rate==1.0
    assert result.boundary_integrity_rate==1.0
    assert result.repeatable is True
    assert result.result=="RETEST"
