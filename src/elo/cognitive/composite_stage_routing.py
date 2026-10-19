"""Governed evidence for composite production stages.

Layer: cognitive
Owner: PCP operational health/readiness
Status: implemented
Authority: implementation
Related: operational_capacity_evidence_matrix, work_center_evidence

A canonical production stage can be a macro-stage composed of multiple observed
operational sectors. This module evaluates whether evidence is strong enough to
propose a governed routing model. It never creates routes, work centers or capacity
rules and never treats an observed sector as canonical authority by itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Sequence


class CompositeStageRoutingState(StrEnum):
    NEEDS_STAGE_EVIDENCE = "NEEDS_STAGE_EVIDENCE"
    NEEDS_CAPACITY_EVIDENCE = "NEEDS_CAPACITY_EVIDENCE"
    READY_FOR_ROUTING_PROPOSAL = "READY_FOR_ROUTING_PROPOSAL"
    CANONICAL_ROUTE_EXISTS = "CANONICAL_ROUTE_EXISTS"


@dataclass(frozen=True, slots=True)
class CompositeSectorEvidence:
    sector: str
    observation_count: int
    source_ref: str

    def __post_init__(self) -> None:
        if not self.sector.strip():
            raise ValueError("sector is required")
        if self.observation_count < 1:
            raise ValueError("observation_count must be positive")
        if not self.source_ref.strip():
            raise ValueError("source_ref is required")


@dataclass(frozen=True, slots=True)
class CompositeStageRoutingAssessment:
    stage_code: str
    state: CompositeStageRoutingState
    constituent_sectors: tuple[str, ...]
    aggregate_capacity_per_day: float | None
    aggregate_capacity_unit: str | None
    confidence: float
    next_required_condition: str | None
    evidence_refs: tuple[str, ...]
    canonical_mutation: bool = False


def assess_composite_stage_routing(
    *,
    stage_code: str,
    sector_evidence: Sequence[CompositeSectorEvidence],
    aggregate_capacity_per_day: float | None,
    aggregate_capacity_unit: str | None,
    capacity_source_ref: str | None,
    canonical_route_count: int = 0,
) -> CompositeStageRoutingAssessment:
    """Assess whether a macro-stage can advance to a routing proposal.

    Multiple real sectors are preserved as constituents instead of being forced into
    a single work center. A proposal still requires subsequent governed route and
    work-center registration.
    """
    stage = stage_code.strip().upper()
    if not stage:
        raise ValueError("stage_code is required")
    if canonical_route_count < 0:
        raise ValueError("canonical_route_count cannot be negative")
    if aggregate_capacity_per_day is not None and (
        not isfinite(aggregate_capacity_per_day) or aggregate_capacity_per_day <= 0
    ):
        raise ValueError("aggregate_capacity_per_day must be finite and greater than zero")

    real = tuple(sector_evidence)
    sectors = tuple(dict.fromkeys(item.sector.strip().upper() for item in real))
    refs = tuple(dict.fromkeys(item.source_ref for item in real))

    if canonical_route_count > 0:
        return CompositeStageRoutingAssessment(
            stage,
            CompositeStageRoutingState.CANONICAL_ROUTE_EXISTS,
            sectors,
            aggregate_capacity_per_day,
            aggregate_capacity_unit,
            1.0,
            None,
            refs + ((capacity_source_ref,) if capacity_source_ref else ()),
        )

    if len(sectors) < 2:
        return CompositeStageRoutingAssessment(
            stage,
            CompositeStageRoutingState.NEEDS_STAGE_EVIDENCE,
            sectors,
            aggregate_capacity_per_day,
            aggregate_capacity_unit,
            0.35 if sectors else 0.0,
            "multiple_constituent_operational_sectors",
            refs + ((capacity_source_ref,) if capacity_source_ref else ()),
        )

    if aggregate_capacity_per_day is None or not (aggregate_capacity_unit or "").strip() or not capacity_source_ref:
        count = sum(item.observation_count for item in real)
        return CompositeStageRoutingAssessment(
            stage,
            CompositeStageRoutingState.NEEDS_CAPACITY_EVIDENCE,
            sectors,
            None,
            None,
            min(0.7, 0.45 + 0.025 * min(count, 10)),
            "aggregate_capacity_with_provenance",
            refs,
        )

    count = sum(item.observation_count for item in real)
    confidence = min(0.9, 0.65 + 0.02 * min(count, 12))
    return CompositeStageRoutingAssessment(
        stage,
        CompositeStageRoutingState.READY_FOR_ROUTING_PROPOSAL,
        sectors,
        aggregate_capacity_per_day,
        aggregate_capacity_unit.strip(),
        round(confidence, 3),
        "governed_route_and_work_center_registration",
        tuple(dict.fromkeys(refs + (capacity_source_ref,))),
    )


__all__ = [
    "CompositeSectorEvidence",
    "CompositeStageRoutingAssessment",
    "CompositeStageRoutingState",
    "assess_composite_stage_routing",
]
