"""Reconcile governed empirical capacity evidence with canonical PCP structures.

The reconciler is intentionally read-only. It identifies whether an empirical
capacity observation can be mapped to a canonical production stage and what is
still required before it can be persisted as a canonical capacity rule.

It never creates work centers, component types, conversion factors, tenants, or
capacity rows. Missing semantics remain explicit blockers/review items.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable, Mapping, Sequence


class CapacityReconciliationState(StrEnum):
    READY_FOR_CANONICALIZATION = "READY_FOR_CANONICALIZATION"
    NEEDS_WORK_CENTER = "NEEDS_WORK_CENTER"
    NEEDS_UNIT_CONVERSION = "NEEDS_UNIT_CONVERSION"
    NEEDS_STAGE_MAPPING = "NEEDS_STAGE_MAPPING"
    AMBIGUOUS_STAGE = "AMBIGUOUS_STAGE"


@dataclass(frozen=True, slots=True)
class EmpiricalCapacityEvidence:
    evidence_id: str
    activity: str
    quantity_per_day: float
    unit: str
    stage_codes: tuple[str, ...]
    source_ref: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id is required")
        if not self.activity.strip():
            raise ValueError("activity is required")
        if self.quantity_per_day <= 0:
            raise ValueError("quantity_per_day must be greater than zero")
        if not self.unit.strip():
            raise ValueError("unit is required")
        if not self.source_ref.strip():
            raise ValueError("source_ref is required")


@dataclass(frozen=True, slots=True)
class CapacityReconciliation:
    evidence_id: str
    state: CapacityReconciliationState
    matched_stage: str | None
    work_center_ref: str | None
    canonical_unit: str | None
    next_required_condition: str | None
    source_ref: str
    detail: str
    canonical_mutation: bool = False


_DIRECT_STAGE_UNITS = {
    "modulos/dia": "MODULOS_DIA",
    "módulos/dia": "MODULOS_DIA",
    "estruturas/dia": "ESTRUTURAS_DIA",
}


def _normalize_stage_codes(stage_codes: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(code.strip().upper() for code in stage_codes if code.strip()))


def _normalize_stage_work_centers(
    stage_work_centers: Mapping[str, str],
) -> dict[str, str]:
    return {
        stage.strip().upper(): center.strip()
        for stage, center in stage_work_centers.items()
        if stage.strip() and center.strip()
    }


def reconcile_capacity_evidence(
    evidence: EmpiricalCapacityEvidence,
    *,
    canonical_stage_codes: Sequence[str],
    stage_work_centers: Mapping[str, str] | None = None,
    accepted_direct_units: Sequence[str] = tuple(_DIRECT_STAGE_UNITS),
) -> CapacityReconciliation:
    """Classify one empirical capacity observation without inventing semantics.

    A stage match is necessary but not sufficient for canonicalization. The
    canonical MT capacity tables require a work-center relation *for the matched
    stage*, and observations expressed in component-level units (e.g.
    columns/day or bases/day) need an explicit conversion or component/resource
    model before they can represent a stage-level capacity.
    """
    stages = set(_normalize_stage_codes(canonical_stage_codes))
    requested = _normalize_stage_codes(evidence.stage_codes)
    matched = tuple(code for code in requested if code in stages)

    if not requested or not matched:
        return CapacityReconciliation(
            evidence_id=evidence.evidence_id,
            state=CapacityReconciliationState.NEEDS_STAGE_MAPPING,
            matched_stage=None,
            work_center_ref=None,
            canonical_unit=None,
            next_required_condition="canonical_stage_mapping",
            source_ref=evidence.source_ref,
            detail=f"declared_stages={requested or ()} matched=()",
        )
    if len(matched) > 1:
        return CapacityReconciliation(
            evidence_id=evidence.evidence_id,
            state=CapacityReconciliationState.AMBIGUOUS_STAGE,
            matched_stage=None,
            work_center_ref=None,
            canonical_unit=None,
            next_required_condition="single_canonical_stage",
            source_ref=evidence.source_ref,
            detail=f"matched_stages={matched}",
        )

    matched_stage = matched[0]
    normalized_unit = evidence.unit.strip().lower()
    accepted = {item.strip().lower() for item in accepted_direct_units}
    if normalized_unit not in accepted:
        return CapacityReconciliation(
            evidence_id=evidence.evidence_id,
            state=CapacityReconciliationState.NEEDS_UNIT_CONVERSION,
            matched_stage=matched_stage,
            work_center_ref=None,
            canonical_unit=None,
            next_required_condition="governed_unit_conversion_or_component_model",
            source_ref=evidence.source_ref,
            detail=(
                f"stage={matched_stage} unit={evidence.unit} quantity_per_day={evidence.quantity_per_day}"
            ),
        )

    centers = _normalize_stage_work_centers(stage_work_centers or {})
    work_center = centers.get(matched_stage)
    if not work_center:
        return CapacityReconciliation(
            evidence_id=evidence.evidence_id,
            state=CapacityReconciliationState.NEEDS_WORK_CENTER,
            matched_stage=matched_stage,
            work_center_ref=None,
            canonical_unit=_DIRECT_STAGE_UNITS.get(normalized_unit, normalized_unit.upper()),
            next_required_condition="canonical_stage_work_center",
            source_ref=evidence.source_ref,
            detail=(
                f"stage={matched_stage} direct_unit={evidence.unit} but no work center is mapped to this stage"
            ),
        )

    return CapacityReconciliation(
        evidence_id=evidence.evidence_id,
        state=CapacityReconciliationState.READY_FOR_CANONICALIZATION,
        matched_stage=matched_stage,
        work_center_ref=work_center,
        canonical_unit=_DIRECT_STAGE_UNITS.get(normalized_unit, normalized_unit.upper()),
        next_required_condition=None,
        source_ref=evidence.source_ref,
        detail=(
            f"stage={matched_stage} work_center={work_center} quantity_per_day={evidence.quantity_per_day}"
        ),
    )


def summarize_capacity_reconciliation(
    results: Sequence[CapacityReconciliation],
) -> dict[str, object]:
    """Summarize reconciliation states for health/orchestration handoff."""
    counts = {state.value: 0 for state in CapacityReconciliationState}
    for item in results:
        counts[item.state.value] += 1
    next_conditions = tuple(
        dict.fromkeys(
            item.next_required_condition
            for item in results
            if item.next_required_condition is not None
        )
    )
    return {
        "total": len(results),
        "counts": counts,
        "next_required_conditions": next_conditions,
        "canonical_mutation": False,
    }


__all__ = [
    "CapacityReconciliation",
    "CapacityReconciliationState",
    "EmpiricalCapacityEvidence",
    "reconcile_capacity_evidence",
    "summarize_capacity_reconciliation",
]
