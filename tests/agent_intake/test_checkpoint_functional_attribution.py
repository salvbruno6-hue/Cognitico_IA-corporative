from src.elo.agent_intake.checkpoint_loop_harness import evaluate_checkpoint_loop_harness

def test_checkpoint_does_not_promote_owner_gain_as_candidate_gain():
    measurement = evaluate_checkpoint_loop_harness(repeats=3)
    assert measurement.adapted['recovery_success'] > measurement.baseline['recovery_success']
    assert measurement.candidate_incremental_effect_isolated is False
    assert measurement.to_candidate_measurement().result == 'RETEST'