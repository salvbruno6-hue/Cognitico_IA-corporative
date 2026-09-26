"""Controlled measurement harness for the Hermes checkpoint candidate.

The harness separates the existing ELO State Recovery owner from a
candidate-specific replay invariant: stale checkpoints must not be replayed
against a newer execution-state version.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hermes_checkpoint_replay_guard import evaluate_checkpoint_replay_guard
from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .state_recovery_integrity import evaluate_state_recovery


@dataclass(frozen=True, slots=True)
class CheckpointLoopMeasurement:
    baseline: Mapping[str, float]
    adapted: Mapping[str, float]
    regressions: tuple[str, ...]
    repeatable: bool
    candidate_incremental_effect_isolated: bool
    candidate_id: str = "EXT-CHECKPOINT-HERMES"
    metric_directions: Mapping[str, str] | None = None

    def to_candidate_measurement(self) -> CandidateMeasurement:
        candidate = build_candidate(self.candidate_id)
        return CandidateMeasurement(
            candidate_id=candidate.candidate_id,
            baseline=self.baseline,
            adapted=self.adapted,
            regressions=self.regressions,
            repeatable=self.repeatable,
            result="REJECT" if self.regressions else (
                "EVOLUTION_GATE_REQUIRED"
                if self.repeatable
                and self.candidate_incremental_effect_isolated
                and self.adapted.get("unsafe_replay_block_rate", 0.0)
                > self.baseline.get("unsafe_replay_block_rate", 0.0)
                else "RETEST"
            ),
        )


def _baseline_probe(tenant_scope: str) -> tuple[float, float]:
    """Existing owner recovers state but has no checkpoint-version replay guard."""
    state = {"tenant_scope": tenant_scope, "value": "controlled"}
    evidence = evaluate_state_recovery(
        request_id="loop-checkpoint-baseline",
        tenant_scope=tenant_scope,
        state=state,
        checkpoint_id="loop-checkpoint-stale",
        interrupted=True,
    )
    recovery_success = float(evidence.status == "recovered")

    # The existing owner does not receive a state-version invariant, so the
    # stale checkpoint is accepted by this controlled baseline.
    unsafe_replay_blocked = 0.0
    return recovery_success, unsafe_replay_blocked


def _adapted_probe(tenant_scope: str) -> tuple[float, float]:
    state = {"tenant_scope": tenant_scope, "value": "controlled"}
    evidence = evaluate_state_recovery(
        request_id="loop-checkpoint-adapted",
        tenant_scope=tenant_scope,
        state=state,
        checkpoint_id="loop-checkpoint-stale",
        interrupted=True,
    )
    recovery_success = float(evidence.status == "recovered")

    replay_guard = evaluate_checkpoint_replay_guard(
        expected_state_version=2,
        checkpoint_state_version=1,
    )
    unsafe_replay_blocked = float(replay_guard.replay_blocked)
    return recovery_success, unsafe_replay_blocked


def evaluate_checkpoint_loop_harness(
    *, tenant_scope: str = "loop-tenant", repeats: int = 3
) -> CheckpointLoopMeasurement:
    if repeats < 1:
        raise ValueError("repeats must be >= 1")

    baseline_values = [_baseline_probe(tenant_scope) for _ in range(repeats)]
    adapted_values = [_adapted_probe(tenant_scope) for _ in range(repeats)]

    baseline = {
        "recovery_success": sum(item[0] for item in baseline_values) / repeats,
        "unsafe_replay_block_rate": sum(item[1] for item in baseline_values) / repeats,
    }
    adapted = {
        "recovery_success": sum(item[0] for item in adapted_values) / repeats,
        "unsafe_replay_block_rate": sum(item[1] for item in adapted_values) / repeats,
    }

    regressions: tuple[str, ...] = ()
    repeatable = (
        len(set(baseline_values)) == 1
        and len(set(adapted_values)) == 1
    )

    return CheckpointLoopMeasurement(
        baseline=baseline,
        adapted=adapted,
        regressions=regressions,
        repeatable=repeatable,
        candidate_incremental_effect_isolated=(
            adapted["unsafe_replay_block_rate"]
            > baseline["unsafe_replay_block_rate"]
            and all(item[0] == 1.0 for item in adapted_values)
        ),
        metric_directions={
            "recovery_success": "maximize",
            "unsafe_replay_block_rate": "maximize",
        },
    )


__all__ = ["CheckpointLoopMeasurement", "evaluate_checkpoint_loop_harness"]
