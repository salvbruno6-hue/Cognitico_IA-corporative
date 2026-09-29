"""Governed refinement for Hermes live steering of delegated child agents.

This is an ELO-side contract. It never calls Hermes and never grants authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


CAPABILITY_ID = "EXT-MULTIAGENT-HERMES"
REFINEMENT_ID = "REF-LIVE-STEERING-HERMES"


class SteeringDisposition(str, Enum):
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class LiveSteeringSignal:
    signal_id: str
    parent_execution_id: str
    child_agent_id: str
    directive_digest: str
    provenance_ref: str
    explicit_directive: bool = False
    authority_transfer: bool = False


@dataclass(frozen=True, slots=True)
class LiveSteeringAssessment:
    signal_id: str
    disposition: SteeringDisposition
    boundary_integrity: bool
    execution_permitted: bool = False
    canonical_mutation: bool = False


def assess_live_steering(signal: LiveSteeringSignal) -> LiveSteeringAssessment:
    required = (
        signal.signal_id,
        signal.parent_execution_id,
        signal.child_agent_id,
        signal.directive_digest,
        signal.provenance_ref,
    )
    if not all(required):
        return LiveSteeringAssessment(
            signal.signal_id, SteeringDisposition.REJECTED, False
        )
    if not signal.explicit_directive or signal.authority_transfer:
        return LiveSteeringAssessment(
            signal.signal_id, SteeringDisposition.REJECTED, False
        )
    return LiveSteeringAssessment(
        signal.signal_id,
        SteeringDisposition.CANDIDATE,
        True,
        execution_permitted=False,
        canonical_mutation=False,
    )


def evaluate_live_steering_gain() -> tuple[float, float, bool, bool, tuple[str, ...]]:
    """Controlled contract evaluation; no live agent is started."""
    signals = tuple(
        LiveSteeringSignal(
            f"steer-{i}",
            "parent-execution",
            f"worker-{i}",
            f"directive-{i}",
            f"controlled-eval:live-steering/{i}",
            explicit_directive=True,
        )
        for i in range(1, 6)
    )
    baseline = 0.0
    adapted = sum(
        assess_live_steering(signal).boundary_integrity for signal in signals
    ) / len(signals)
    repeat = (
        sum(
            assess_live_steering(signal).boundary_integrity
            for signal in signals
        ) / len(signals)
    ) == adapted
    boundary = all(
        (assessment := assess_live_steering(signal)).disposition
        is SteeringDisposition.CANDIDATE
        and assessment.execution_permitted is False
        and assessment.canonical_mutation is False
        for signal in signals
    )
    refs = tuple(signal.provenance_ref for signal in signals)
    return baseline, adapted, repeat, boundary, refs


__all__ = [
    "CAPABILITY_ID",
    "REFINEMENT_ID",
    "LiveSteeringSignal",
    "LiveSteeringAssessment",
    "SteeringDisposition",
    "assess_live_steering",
    "evaluate_live_steering_gain",
]
