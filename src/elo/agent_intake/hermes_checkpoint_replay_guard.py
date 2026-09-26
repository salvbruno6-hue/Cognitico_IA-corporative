"""Candidate-specific checkpoint replay guard for controlled Hermes evaluation.

This guard does not replace ELO State Recovery. It adds one measurable,
candidate-owned invariant: a checkpoint may not be replayed against a newer
execution-state version.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReplayGuardEvidence:
    expected_state_version: int
    checkpoint_state_version: int
    replay_blocked: bool
    fresh_checkpoint_accepted: bool


def evaluate_checkpoint_replay_guard(
    *,
    expected_state_version: int,
    checkpoint_state_version: int,
) -> ReplayGuardEvidence:
    if expected_state_version < 1 or checkpoint_state_version < 1:
        raise ValueError("state versions must be >= 1")

    stale = checkpoint_state_version < expected_state_version
    return ReplayGuardEvidence(
        expected_state_version=expected_state_version,
        checkpoint_state_version=checkpoint_state_version,
        replay_blocked=stale,
        fresh_checkpoint_accepted=not stale,
    )


__all__ = ["ReplayGuardEvidence", "evaluate_checkpoint_replay_guard"]
