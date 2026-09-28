"""Registra os harnesses existentes no TestHarness.

Não cria novos harnesses. Apenas conecta os existentes ao
orquestrador.

Refs: ELO_TEST_HARNESS_CONTRACT.
"""
from __future__ import annotations

from .test_harness import TestHarness


def build_default_test_harness() -> TestHarness:
    harness = TestHarness()

    try:
        from elo.cognitive.runtime.cognitive_harness import (
            CognitiveHarness,
            CognitiveHarnessFixture,
        )

        def _run_cognitive() -> None:
            fixture = CognitiveHarnessFixture(
                request_id="test-harness-cognitive",
            )
            report = CognitiveHarness().run(fixture)
            if report.metrics.get("error_stage_count", 0) > 0:
                raise RuntimeError(
                    f"cognitive_harness error: "
                    f"{report.metrics}"
                )

        harness.register_harness(
            "cognitive_harness", _run_cognitive
        )
    except Exception:
        pass

    try:
        from elo.agent_intake.hook_loop_harness import (
            evaluate_hook_loop_harness,
        )

        def _run_hook() -> None:
            m = evaluate_hook_loop_harness(repeats=3)
            if not m.repeatable:
                raise RuntimeError(
                    "hook_loop_harness not repeatable"
                )

        harness.register_harness("hook_loop_harness", _run_hook)
    except Exception:
        pass

    try:
        from elo.agent_intake.checkpoint_loop_harness import (
            evaluate_checkpoint_loop_harness,
        )

        def _run_checkpoint() -> None:
            m = evaluate_checkpoint_loop_harness(repeats=3)
            if not m.repeatable:
                raise RuntimeError(
                    "checkpoint_loop_harness not repeatable"
                )

        harness.register_harness(
            "checkpoint_loop_harness", _run_checkpoint
        )
    except Exception:
        pass

    return harness


__all__ = ["build_default_test_harness"]
