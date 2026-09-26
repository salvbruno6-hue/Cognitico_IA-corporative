from src.elo.agent_intake.checkpoint_loop_harness import evaluate_checkpoint_loop_harness


def test_checkpoint_candidate_specific_replay_guard_proves_incremental_gain():
    measurement = evaluate_checkpoint_loop_harness(repeats=3)

    assert measurement.baseline["recovery_success"] == 1.0
    assert measurement.adapted["recovery_success"] == 1.0
    assert measurement.baseline["unsafe_replay_block_rate"] == 0.0
    assert measurement.adapted["unsafe_replay_block_rate"] == 1.0
    assert measurement.candidate_incremental_effect_isolated is True
    assert measurement.to_candidate_measurement().result == "EVOLUTION_GATE_REQUIRED"


def test_checkpoint_replay_guard_accepts_fresh_checkpoint():
    from src.elo.agent_intake.hermes_checkpoint_replay_guard import (
        evaluate_checkpoint_replay_guard,
    )

    evidence = evaluate_checkpoint_replay_guard(
        expected_state_version=2,
        checkpoint_state_version=2,
    )

    assert evidence.replay_blocked is False
    assert evidence.fresh_checkpoint_accepted is True
