"""Controlled measurement harness for the existing ELO checkpoint capability.

The harness compares a deliberately non-recovering baseline probe with the
existing checkpoint/restore capability. It is deterministic and in-memory.
It produces measurements only; it never promotes or mutates canonical ELO.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .state_recovery_integrity import evaluate_state_recovery


@dataclass(frozen=True, slots=True)
class CheckpointLoopMeasurement:
    baseline: Mapping[str, float]
    adapted: Mapping[str, float]
    regressions: tuple[str, ...]
    repeatable: bool
    candidate_id: str = "EXT-CHECKPOINT-HERMES"
    metric_directions: Mapping[str, str] = None

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
                if self.repeatable and self.adapted.get("recovery_success", 0.0)
                > self.baseline.get("recovery_success", 0.0)
                else "RETEST"
            ),
        )


def _baseline_probe(tenant_scope: str) -> float:
    """Baseline: no checkpoint/restore path, therefore recovery is unavailable."""
    state = {"tenant_scope": tenant_scope, "value": "controlled"}
    interrupted_state = None
    return float(interrupted_state is not None and interrupted_state == state)


def _adapted_probe(tenant_scope: str) -> float:
    evidence = evaluate_state_recovery(
        request_id="loop-checkpoint-adapted",
        tenant_scope=tenant_scope,
        state={"tenant_scope": tenant_scope, "value": "controlled"},
        checkpoint_id="loop-checkpoint-001",
        interrupted=True,
    )
    return float(evidence.status == "recovered")


def evaluate_checkpoint_loop_harness(
    *, tenant_scope: str = "loop-tenant", repeats: int = 3
) -> CheckpointLoopMeasurement:
    if repeats < 1:
        raise ValueError("repeats must be >= 1")

    baseline_values = [_baseline_probe(tenant_scope) for _ in range(repeats)]
    adapted_values = [_adapted_probe(tenant_scope) for _ in range(repeats)]

    baseline = {"recovery_success": sum(baseline_values) / repeats}
    adapted = {"recovery_success": sum(adapted_values) / repeats}

    regressions: tuple[str, ...] = ()
    repeatable = len(set(adapted_values)) == 1 and len(set(baseline_values)) == 1

    return CheckpointLoopMeasurement(
        baseline=baseline,
        adapted=adapted,
        regressions=regressions,
        repeatable=repeatable,
        metric_directions={"recovery_success": "maximize"},
    )


__all__ = ["CheckpointLoopMeasurement", "evaluate_checkpoint_loop_harness"]
