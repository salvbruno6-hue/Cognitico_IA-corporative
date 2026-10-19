"""Governed work-center evidence candidates for ELO PCP.

Operational sector/resource evidence may justify a candidate for canonical
registration, but it is not itself a canonical work center. This module keeps
that boundary explicit and read-only.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Sequence


class WorkCenterEvidenceState(StrEnum):
    OBSERVED_CANDIDATE = "OBSERVED_CANDIDATE"
    NEEDS_STAGE_MAPPING = "NEEDS_STAGE_MAPPING"
    AMBIGUOUS_STAGE = "AMBIGUOUS_STAGE"
    REJECT_SIMULATED = "REJECT_SIMULATED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True, slots=True)
class OperationalSectorEvidence:
    sector: str
    source_ref: str
    observation_count: int
    canonical_stage_codes: tuple[str, ...] = ()
    production_per_shift: float | None = None
    shift_minutes: float | None = None
    simulated: bool = False

    def __post_init__(self) -> None:
        if not self.sector.strip():
            raise ValueError("sector is required")
        if not self.source_ref.strip():
            raise ValueError("source_ref is required")
        if self.observation_count < 0:
            raise ValueError("observation_count cannot be negative")
        for value, name in (
            (self.production_per_shift, "production_per_shift"),
            (self.shift_minutes, "shift_minutes"),
        ):
            if value is not None and (not isfinite(value) or value <= 0):
                raise ValueError(f"{name} must be finite and greater than zero")


@dataclass(frozen=True, slots=True)
class WorkCenterEvidenceAssessment:
    sector: str
    state: WorkCenterEvidenceState
    matched_stage: str | None
    evidence_strength: float
    next_required_condition: str | None
    source_ref: str
    detail: str
    canonical_mutation: bool = False


def assess_work_center_evidence(
    evidence: OperationalSectorEvidence,
    *,
    active_stage_codes: Sequence[str],
) -> WorkCenterEvidenceAssessment:
    """Assess a sector as a candidate, never as an automatic work center."""
    active = {item.strip().upper() for item in active_stage_codes if item.strip()}
    declared = tuple(
        dict.fromkeys(
            item.strip().upper()
            for item in evidence.canonical_stage_codes
            if item.strip()
        )
    )

    if evidence.simulated:
        return WorkCenterEvidenceAssessment(
            evidence.sector,
            WorkCenterEvidenceState.REJECT_SIMULATED,
            None,
            0.0,
            "real_operational_evidence",
            evidence.source_ref,
            "simulated resource/sector evidence cannot establish a canonical work center",
        )
    if evidence.observation_count == 0:
        return WorkCenterEvidenceAssessment(
            evidence.sector,
            WorkCenterEvidenceState.INSUFFICIENT_EVIDENCE,
            None,
            0.0,
            "operational_observation",
            evidence.source_ref,
            "no operational observations",
        )

    matched = tuple(item for item in declared if item in active)
    unmapped = tuple(item for item in declared if item not in active)
    if not declared or unmapped or not matched:
        strength = min(evidence.observation_count / 3.0, 1.0) * 0.5
        return WorkCenterEvidenceAssessment(
            evidence.sector,
            WorkCenterEvidenceState.NEEDS_STAGE_MAPPING,
            matched[0] if len(matched) == 1 else None,
            round(strength, 3),
            "governed_stage_mapping",
            evidence.source_ref,
            f"declared={declared} matched={matched} unmapped={unmapped}",
        )
    if len(matched) > 1:
        strength = min(evidence.observation_count / 3.0, 1.0) * 0.5
        return WorkCenterEvidenceAssessment(
            evidence.sector,
            WorkCenterEvidenceState.AMBIGUOUS_STAGE,
            None,
            round(strength, 3),
            "single_stage_mapping",
            evidence.source_ref,
            f"matched={matched}",
        )

    evidence_dimensions = 1
    if evidence.production_per_shift is not None:
        evidence_dimensions += 1
    if evidence.shift_minutes is not None:
        evidence_dimensions += 1
    strength = min(evidence.observation_count / 3.0, 1.0) * (
        evidence_dimensions / 3.0
    )
    return WorkCenterEvidenceAssessment(
        evidence.sector,
        WorkCenterEvidenceState.OBSERVED_CANDIDATE,
        matched[0],
        round(strength, 3),
        "governed_work_center_registration",
        evidence.source_ref,
        (
            f"observations={evidence.observation_count} "
            f"production_per_shift={evidence.production_per_shift} "
            f"shift_minutes={evidence.shift_minutes}"
        ),
    )


def summarize_work_center_evidence(
    assessments: Sequence[WorkCenterEvidenceAssessment],
) -> dict[str, object]:
    counts = {state.value: 0 for state in WorkCenterEvidenceState}
    for item in assessments:
        counts[item.state.value] += 1
    return {
        "total": len(assessments),
        "counts": counts,
        "candidate_sectors": tuple(
            item.sector
            for item in assessments
            if item.state is WorkCenterEvidenceState.OBSERVED_CANDIDATE
        ),
        "canonical_mutation": False,
    }


__all__ = [
    "OperationalSectorEvidence",
    "WorkCenterEvidenceAssessment",
    "WorkCenterEvidenceState",
    "assess_work_center_evidence",
    "summarize_work_center_evidence",
]
