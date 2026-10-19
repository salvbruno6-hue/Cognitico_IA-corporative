"""Build a governed matrix connecting capacity evidence to canonical production semantics.

This module is read-only. It combines empirical capacity evidence, observed operational
sectors/resources, and canonical stage mappings without inventing work centers or unit
conversions. It is intended for orchestration and health/readiness decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Mapping, Sequence


class CapacityMatrixState(StrEnum):
    READY_FOR_PROPOSAL = "READY_FOR_PROPOSAL"
    NEEDS_STAGE_MAPPING = "NEEDS_STAGE_MAPPING"
    NEEDS_WORK_CENTER = "NEEDS_WORK_CENTER"
    NEEDS_UNIT_MODEL = "NEEDS_UNIT_MODEL"
    NEEDS_OPERATIONAL_EVIDENCE = "NEEDS_OPERATIONAL_EVIDENCE"
    AMBIGUOUS_OPERATIONAL_SECTOR = "AMBIGUOUS_OPERATIONAL_SECTOR"
    SCOPE_MISMATCH = "SCOPE_MISMATCH"


@dataclass(frozen=True, slots=True)
class CapacityEvidenceRow:
    capacity_id: str
    activity: str
    quantity_per_day: float
    unit: str
    declared_stage_codes: tuple[str, ...]
    source_ref: str

    def __post_init__(self) -> None:
        if not self.capacity_id.strip():
            raise ValueError("capacity_id is required")
        if not self.activity.strip():
            raise ValueError("activity is required")
        if not isfinite(self.quantity_per_day) or self.quantity_per_day <= 0:
            raise ValueError("quantity_per_day must be finite and greater than zero")
        if not self.unit.strip():
            raise ValueError("unit is required")
        if not self.source_ref.strip():
            raise ValueError("source_ref is required")


@dataclass(frozen=True, slots=True)
class OperationalEvidence:
    sector: str
    stage_codes: tuple[str, ...]
    source_ref: str
    evidence_count: int = 1
    simulated: bool = False
    output_unit: str | None = None

    def __post_init__(self) -> None:
        if not self.sector.strip():
            raise ValueError("sector is required")
        if self.evidence_count < 1:
            raise ValueError("evidence_count must be positive")
        if not self.source_ref.strip():
            raise ValueError("source_ref is required")
        if self.output_unit is not None and not self.output_unit.strip():
            raise ValueError("output_unit cannot be blank")


@dataclass(frozen=True, slots=True)
class CapacityEvidenceMatrixRow:
    capacity_id: str
    state: CapacityMatrixState
    canonical_stage: str | None
    observed_sector: str | None
    work_center_ref: str | None
    canonical_unit: str | None
    confidence: float
    next_required_condition: str | None
    evidence_refs: tuple[str, ...]
    canonical_mutation: bool = False


_DIRECT_UNITS = {
    "módulos/dia": "MODULOS_DIA",
    "modulos/dia": "MODULOS_DIA",
    "estruturas/dia": "ESTRUTURAS_DIA",
}


def _norm_codes(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(v.strip().upper() for v in values if v.strip()))


def _canonical_unit(value: str | None) -> str | None:
    if value is None:
        return None
    return _DIRECT_UNITS.get(value.strip().lower())


def build_capacity_evidence_matrix_row(
    capacity: CapacityEvidenceRow,
    *,
    canonical_stage_codes: Sequence[str],
    operational_evidence: Sequence[OperationalEvidence],
    stage_work_centers: Mapping[str, str] | None = None,
) -> CapacityEvidenceMatrixRow:
    canonical = set(_norm_codes(canonical_stage_codes))
    declared = _norm_codes(capacity.declared_stage_codes)
    if not declared or any(code not in canonical for code in declared) or len(declared) != 1:
        return CapacityEvidenceMatrixRow(capacity.capacity_id, CapacityMatrixState.NEEDS_STAGE_MAPPING, None, None, None, None, 0.0, "single_fully_mapped_canonical_stage", (capacity.source_ref,))

    stage = declared[0]
    canonical_unit = _canonical_unit(capacity.unit)
    if canonical_unit is None:
        return CapacityEvidenceMatrixRow(capacity.capacity_id, CapacityMatrixState.NEEDS_UNIT_MODEL, stage, None, None, None, 0.25, "governed_unit_conversion_or_component_model", (capacity.source_ref,))

    stage_candidates = [ev for ev in operational_evidence if not ev.simulated and stage in _norm_codes(ev.stage_codes)]
    mismatched = [ev for ev in stage_candidates if ev.output_unit is not None and _canonical_unit(ev.output_unit) not in (None, canonical_unit)]
    candidates = [ev for ev in stage_candidates if ev.output_unit is None or _canonical_unit(ev.output_unit) in (None, canonical_unit)]

    if stage_candidates and not candidates and mismatched:
        refs = tuple(dict.fromkeys((capacity.source_ref,) + tuple(ev.source_ref for ev in mismatched)))
        return CapacityEvidenceMatrixRow(capacity.capacity_id, CapacityMatrixState.SCOPE_MISMATCH, stage, None, None, canonical_unit, 0.2, "operational_evidence_with_matching_output_scope", refs)

    sectors = tuple(dict.fromkeys(ev.sector.strip().upper() for ev in candidates))
    refs = tuple(dict.fromkeys((capacity.source_ref,) + tuple(ev.source_ref for ev in candidates)))
    if not sectors:
        return CapacityEvidenceMatrixRow(capacity.capacity_id, CapacityMatrixState.NEEDS_OPERATIONAL_EVIDENCE, stage, None, None, canonical_unit, 0.35, "observed_operational_sector_or_resource", refs)
    if len(sectors) > 1:
        return CapacityEvidenceMatrixRow(capacity.capacity_id, CapacityMatrixState.AMBIGUOUS_OPERATIONAL_SECTOR, stage, None, None, canonical_unit, 0.5, "single_governed_operational_sector_mapping", refs)

    sector = sectors[0]
    center = (stage_work_centers or {}).get(stage)
    if not center:
        count = sum(ev.evidence_count for ev in candidates)
        confidence = min(0.85, 0.55 + 0.05 * min(count, 6))
        return CapacityEvidenceMatrixRow(capacity.capacity_id, CapacityMatrixState.NEEDS_WORK_CENTER, stage, sector, None, canonical_unit, confidence, "canonical_stage_work_center", refs)

    return CapacityEvidenceMatrixRow(capacity.capacity_id, CapacityMatrixState.READY_FOR_PROPOSAL, stage, sector, center, canonical_unit, 0.9, None, refs)


def summarize_capacity_evidence_matrix(rows: Sequence[CapacityEvidenceMatrixRow]) -> dict[str, object]:
    counts = {state.value: 0 for state in CapacityMatrixState}
    for row in rows:
        counts[row.state.value] += 1
    return {"total": len(rows), "counts": counts, "ready_for_proposal": counts[CapacityMatrixState.READY_FOR_PROPOSAL.value], "canonical_mutation": False}


__all__ = ["CapacityEvidenceMatrixRow", "CapacityEvidenceRow", "CapacityMatrixState", "OperationalEvidence", "build_capacity_evidence_matrix_row", "summarize_capacity_evidence_matrix"]
