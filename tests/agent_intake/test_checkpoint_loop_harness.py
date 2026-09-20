"""Tests for the controlled checkpoint implementation-loop harness."""
from src.elo.agent_intake.checkpoint_loop_harness import (
    evaluate_checkpoint_loop_harness,
)


def test_checkpoint_harness_produces_real_baseline_and_adapted_measurements():
    measurement = evaluate_checkpoint_loop_harness(
        tenant_scope="tenant-a",
        repeats=5,
    )

    assert measurement.baseline["recovery_success"] == 0.0
    assert measurement.adapted["recovery_success"] == 1.0
    assert measurement.metric_directions == {"recovery_success": "maximize"}
    assert measurement.regressions == ()
    assert measurement.repeatable is True


def test_checkpoint_harness_is_repeatable():
    first = evaluate_checkpoint_loop_harness(tenant_scope="tenant-a", repeats=3)
    second = evaluate_checkpoint_loop_harness(tenant_scope="tenant-a", repeats=3)

    assert first.baseline == second.baseline
    assert first.adapted == second.adapted
    assert first.repeatable is True
