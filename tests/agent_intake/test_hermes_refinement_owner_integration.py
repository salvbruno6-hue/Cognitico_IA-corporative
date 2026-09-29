from elo.agent_intake.hermes_multiagent_functional_evaluation import evaluate_multiagent_functional_gain
from elo.agent_intake.hermes_cron_functional_evaluation import evaluate_cron_functional_gain


def test_live_steering_is_integrated_into_existing_multiagent_owner():
    evidence = evaluate_multiagent_functional_gain()
    assert evidence.live_steering_baseline_rate == 0.0
    assert evidence.live_steering_adapted_rate == 1.0
    assert evidence.live_steering_repeatable is True
    assert evidence.live_steering_boundary_integrity is True


def test_cron_continuity_is_integrated_into_existing_automation_owner():
    evidence = evaluate_cron_functional_gain()
    assert evidence.continuity_baseline_rate == 0.0
    assert evidence.continuity_adapted_rate == 1.0
    assert evidence.continuity_repeatable is True
    assert evidence.continuity_boundary_integrity is True
