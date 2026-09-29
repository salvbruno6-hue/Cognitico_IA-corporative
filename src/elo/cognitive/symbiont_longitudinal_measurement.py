"""Longitudinal measurement for governed Skill evolution.

This layer measures change across comparable observations. It is evidence
analysis only: it does not authorize execution, approve learning, promote a
Skill, mutate Core, or replace the Evolution Gate.

The existing Hermes process contracts remain authoritative for metric identity
and direction. This adapter adds the missing temporal comparator: first
observation establishes a baseline; a later observation produces a directional
delta against that baseline.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence


class MeasurementStatus(str, Enum):
    BASELINE_ESTABLISHED = "BASELINE_ESTABLISHED"
    IMPROVED = "IMPROVED"
    STABLE = "STABLE"
    REGRESSED = "REGRESSED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DUPLICATE = "DUPLICATE"


@dataclass(frozen=True, slots=True)
class SkillObservation:
    observation_id: str
    skill_id: str
    tenant_id: str
    domain: str
    decision_id: str
    metric: str
    value: float | None
    direction: str
    evidence_refs: tuple[str, ...]
    source_ref: str
    dataset_version: str
    learning_context_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        required = {
            "observation_id": self.observation_id,
            "skill_id": self.skill_id,
            "tenant_id": self.tenant_id,
            "domain": self.domain,
            "decision_id": self.decision_id,
            "metric": self.metric,
            "direction": self.direction,
            "source_ref": self.source_ref,
            "dataset_version": self.dataset_version,
        }
        missing = tuple(name for name, value in required.items() if not value)
        if missing:
            raise ValueError("skill observation missing: " + ", ".join(missing))
        if self.direction not in {"maximize", "minimize"}:
            raise ValueError("direction must be maximize or minimize")


@dataclass(frozen=True, slots=True)
class LongitudinalMeasurement:
    skill_id: str
    tenant_id: str
    domain: str
    metric: str
    direction: str
    baseline_observation_id: str
    current_observation_id: str
    baseline_value: float | None
    current_value: float | None
    delta: float | None
    normalized_gain: float | None
    status: MeasurementStatus
    evidence_refs: tuple[str, ...]
    learning_context_ids: tuple[str, ...]
    canonical_mutation: bool = False
    authorization_granted: bool = False

    @property
    def comparable(self) -> bool:
        return self.status in {
            MeasurementStatus.IMPROVED,
            MeasurementStatus.STABLE,
            MeasurementStatus.REGRESSED,
        }


def measure_longitudinal_change(
    baseline: SkillObservation | None,
    current: SkillObservation,
    *,
    seen_observation_ids: Sequence[str] = (),
) -> LongitudinalMeasurement:
    """Compare two observations without creating or changing canonical state."""
    if current.observation_id in set(seen_observation_ids):
        return _result(current, None, None, None, MeasurementStatus.DUPLICATE, ())

    if baseline is None:
        return _result(
            current,
            None,
            None,
            None,
            MeasurementStatus.BASELINE_ESTABLISHED,
            current.evidence_refs,
        )

    _validate_pair(baseline, current)

    if (
        baseline.value is None
        or current.value is None
        or not baseline.evidence_refs
        or not current.evidence_refs
    ):
        return _result(
            current,
            baseline,
            None,
            None,
            MeasurementStatus.INSUFFICIENT_EVIDENCE,
            tuple(dict.fromkeys((*baseline.evidence_refs, *current.evidence_refs))),
        )

    raw_delta = round(current.value - baseline.value, 10)
    gain = raw_delta if current.direction == "maximize" else -raw_delta
    denominator = abs(baseline.value)
    normalized = round(gain / denominator, 10) if denominator else (None if gain == 0 else float("inf"))

    status = (
        MeasurementStatus.IMPROVED
        if gain > 0
        else MeasurementStatus.REGRESSED
        if gain < 0
        else MeasurementStatus.STABLE
    )
    return _result(
        current,
        baseline,
        raw_delta,
        normalized,
        status,
        tuple(dict.fromkeys((*baseline.evidence_refs, *current.evidence_refs))),
    )


def _validate_pair(baseline: SkillObservation, current: SkillObservation) -> None:
    fields = ("skill_id", "tenant_id", "domain", "metric", "direction", "dataset_version")
    for field in fields:
        if getattr(baseline, field) != getattr(current, field):
            raise ValueError(f"longitudinal comparison mismatch: {field}")
    if baseline.observation_id == current.observation_id:
        raise ValueError("baseline and current observation must be distinct")


def _result(
    current: SkillObservation,
    baseline: SkillObservation | None,
    delta: float | None,
    normalized_gain: float | None,
    status: MeasurementStatus,
    evidence_refs: tuple[str, ...],
) -> LongitudinalMeasurement:
    return LongitudinalMeasurement(
        skill_id=current.skill_id,
        tenant_id=current.tenant_id,
        domain=current.domain,
        metric=current.metric,
        direction=current.direction,
        baseline_observation_id=baseline.observation_id if baseline else current.observation_id,
        current_observation_id=current.observation_id,
        baseline_value=baseline.value if baseline else None,
        current_value=current.value,
        delta=delta,
        normalized_gain=normalized_gain,
        status=status,
        evidence_refs=evidence_refs,
        learning_context_ids=current.learning_context_ids,
    )


def observations_from_implementation_evidence(
    *,
    observation_id: str,
    skill_id: str,
    tenant_id: str,
    domain: str,
    decision_id: str,
    source_ref: str,
    dataset_version: str,
    baseline: dict[str, float],
    adapted: dict[str, float],
    metric_directions: dict[str, str],
    evidence_refs: Sequence[str],
    learning_context_ids: Sequence[str] = (),
) -> tuple[SkillObservation, ...]:
    """Expose existing implementation evidence as comparable observations.

    This is an adapter only. The existing ImplementationEvidence contract
    remains authoritative for the candidate's metric and direction.
    """
    common = baseline.keys() & adapted.keys()
    return tuple(
        SkillObservation(
            observation_id=f"{observation_id}:baseline:{metric}",
            skill_id=skill_id,
            tenant_id=tenant_id,
            domain=domain,
            decision_id=decision_id,
            metric=metric,
            value=baseline[metric],
            direction=metric_directions[metric],
            evidence_refs=tuple(evidence_refs),
            source_ref=source_ref,
            dataset_version=dataset_version,
            learning_context_ids=tuple(learning_context_ids),
        )
        for metric in sorted(common)
    ) + tuple(
        SkillObservation(
            observation_id=f"{observation_id}:adapted:{metric}",
            skill_id=skill_id,
            tenant_id=tenant_id,
            domain=domain,
            decision_id=decision_id,
            metric=metric,
            value=adapted[metric],
            direction=metric_directions[metric],
            evidence_refs=tuple(evidence_refs),
            source_ref=source_ref,
            dataset_version=dataset_version,
            learning_context_ids=tuple(learning_context_ids),
        )
        for metric in sorted(common)
    )


__all__ = [
    "LongitudinalMeasurement",
    "MeasurementStatus",
    "SkillObservation",
    "measure_longitudinal_change",
    "observations_from_implementation_evidence",
]
