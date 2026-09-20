"""Controlled evaluation of EXT-WORKTREE-HERMES boundary recognition.

This evaluates the governed signal-assessment contract only. It does not create,
delete, mutate, merge, or activate Git worktrees.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .hermes_worktree_boundary import (
    WorktreeDisposition,
    WorktreeSignal,
    assess_worktree,
)

CAPABILITY_ID = "EXT-WORKTREE-HERMES"
PRIMARY_METRIC = "valid_isolation_recognition_rate"
METRIC_DIRECTION = "maximize"


@dataclass(frozen=True)
class WorktreeEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str


def _signals(prefix: str) -> Sequence[WorktreeSignal]:
    return tuple(
        WorktreeSignal(
            signal_id=f"{prefix}-{i}",
            tenant_scope="multiteiner",
            worktree_id=f"wt/{prefix.lower()}/{i}",
            source_refs=(f"git:worktree:{prefix.lower()}/{i}",),
            base_ref="main",
            isolated=True,
            provenance_verified=True,
        )
        for i in range(1, 6)
    )


def _recognition_rate(signals: Sequence[WorktreeSignal]) -> float:
    if not signals:
        return 0.0
    accepted = sum(
        assess_worktree(signal).disposition is WorktreeDisposition.CANDIDATE
        for signal in signals
    )
    return accepted / len(signals)


def _boundary_integrity_rate(signals: Sequence[WorktreeSignal]) -> float:
    if not signals:
        return 0.0
    safe = sum(
        (
            assessment := assess_worktree(signal)
        ).canonical_authority is False
        and assessment.merge_permitted is False
        for signal in signals
    )
    return safe / len(signals)


def evaluate() -> WorktreeEvaluation:
    baseline = _signals("BASE")
    adapted = _signals("HERMES")

    baseline_rate = _recognition_rate(baseline)
    adapted_rate = _recognition_rate(adapted)
    boundary_integrity_rate = _boundary_integrity_rate(adapted)

    repeatable = (
        _recognition_rate(_signals("REPEAT")) == adapted_rate
        and boundary_integrity_rate == 1.0
    )

    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"
    return WorktreeEvaluation(
        baseline_rate=baseline_rate,
        adapted_rate=adapted_rate,
        boundary_integrity_rate=boundary_integrity_rate,
        repeatable=repeatable,
        result=result,
    )
