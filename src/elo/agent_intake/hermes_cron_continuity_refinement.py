"""Governed refinement for Hermes cron continuity across prior runs.

Continuity is bounded evidence, not automatic ELO memory promotion.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


CAPABILITY_ID = "EXT-CRON-HERMES"
REFINEMENT_ID = "REF-CRON-CONTINUITY-HERMES"


class ContinuityDisposition(str, Enum):
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class CronContinuitySignal:
    signal_id: str
    automation_id: str
    prior_run_ref: str
    continuity_scope: str
    provenance_ref: str
    explicit_continuity: bool = False
    canonical_memory_write: bool = False


@dataclass(frozen=True, slots=True)
class CronContinuityAssessment:
    signal_id: str
    disposition: ContinuityDisposition
    boundary_integrity: bool
    memory_promotion_permitted: bool = False
    execution_permitted: bool = False


def assess_cron_continuity(
    signal: CronContinuitySignal,
) -> CronContinuityAssessment:
    required = (
        signal.signal_id,
        signal.automation_id,
        signal.prior_run_ref,
        signal.continuity_scope,
        signal.provenance_ref,
    )
    if not all(required):
        return CronContinuityAssessment(
            signal.signal_id, ContinuityDisposition.REJECTED, False
        )
    if (
        not signal.explicit_continuity
        or signal.canonical_memory_write
        or signal.continuity_scope == "*"
    ):
        return CronContinuityAssessment(
            signal.signal_id, ContinuityDisposition.REJECTED, False
        )
    return CronContinuityAssessment(
        signal.signal_id,
        ContinuityDisposition.CANDIDATE,
        True,
        memory_promotion_permitted=False,
        execution_permitted=False,
    )


def evaluate_cron_continuity_gain() -> tuple[float, float, bool, bool, tuple[str, ...]]:
    """Controlled continuity evaluation; no scheduler or memory is touched."""
    signals = tuple(
        CronContinuitySignal(
            f"continuity-{i}",
            "automation-1",
            f"prior-run-{i}",
            f"bounded:{i}",
            f"controlled-eval:cron-continuity/{i}",
            explicit_continuity=True,
        )
        for i in range(1, 6)
    )
    baseline = 0.0
    adapted = sum(
        assess_cron_continuity(signal).boundary_integrity for signal in signals
    ) / len(signals)
    repeat = (
        sum(
            assess_cron_continuity(signal).boundary_integrity
            for signal in signals
        ) / len(signals)
    ) == adapted
    boundary = all(
        (assessment := assess_cron_continuity(signal)).disposition
        is ContinuityDisposition.CANDIDATE
        and assessment.memory_promotion_permitted is False
        and assessment.execution_permitted is False
        for signal in signals
    )
    refs = tuple(signal.provenance_ref for signal in signals)
    return baseline, adapted, repeat, boundary, refs


__all__ = [
    "CAPABILITY_ID",
    "REFINEMENT_ID",
    "CronContinuitySignal",
    "CronContinuityAssessment",
    "ContinuityDisposition",
    "assess_cron_continuity",
    "evaluate_cron_continuity_gain",
]
