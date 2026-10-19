"""Partial ordered-route evidence for operational health.

Layer: cognitive
Owner: PCP operational health/readiness
Status: implemented
Authority: implementation
Related: composite_stage_routing, operational_capacity_evidence_matrix

The module preserves order only where the source explicitly provides it. Independent
ordered fragments are never concatenated by inference. It is read-only and cannot
create canonical routes, operations, sectors or work centers.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Sequence


class PartialRouteState(StrEnum):
    INSUFFICIENT_ORDER_EVIDENCE = "INSUFFICIENT_ORDER_EVIDENCE"
    INVALID_FRAGMENT_ORDER = "INVALID_FRAGMENT_ORDER"
    CROSS_FRAGMENT_ORDER_UNPROVEN = "CROSS_FRAGMENT_ORDER_UNPROVEN"
    READY_FOR_ROUTE_PROPOSAL = "READY_FOR_ROUTE_PROPOSAL"


@dataclass(frozen=True, slots=True)
class OrderedOperationEvidence:
    fragment_id: str
    stage_code: str
    sector: str
    sequence: int
    operation: str
    source_ref: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.fragment_id, "fragment_id"),
            (self.stage_code, "stage_code"),
            (self.sector, "sector"),
            (self.operation, "operation"),
            (self.source_ref, "source_ref"),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if self.sequence < 1:
            raise ValueError("sequence must be positive")


@dataclass(frozen=True, slots=True)
class RouteFragmentLink:
    predecessor_fragment_id: str
    successor_fragment_id: str
    source_ref: str

    def __post_init__(self) -> None:
        if not self.predecessor_fragment_id.strip() or not self.successor_fragment_id.strip():
            raise ValueError("fragment link endpoints are required")
        if self.predecessor_fragment_id.strip() == self.successor_fragment_id.strip():
            raise ValueError("fragment cannot precede itself")
        if not self.source_ref.strip():
            raise ValueError("source_ref is required")


@dataclass(frozen=True, slots=True)
class PartialRouteAssessment:
    stage_code: str
    state: PartialRouteState
    ordered_fragments: tuple[tuple[str, tuple[str, ...]], ...]
    unresolved_fragment_pairs: tuple[tuple[str, str], ...]
    evidence_refs: tuple[str, ...]
    next_required_condition: str | None
    canonical_mutation: bool = False


def assess_partial_route(
    *,
    stage_code: str,
    operations: Sequence[OrderedOperationEvidence],
    fragment_links: Sequence[RouteFragmentLink] = (),
) -> PartialRouteAssessment:
    """Preserve proven local order and refuse to invent cross-fragment order."""
    stage = stage_code.strip().upper()
    if not stage:
        raise ValueError("stage_code is required")

    relevant = tuple(op for op in operations if op.stage_code.strip().upper() == stage)
    if len(relevant) < 2:
        refs = tuple(dict.fromkeys(op.source_ref for op in relevant))
        return PartialRouteAssessment(
            stage,
            PartialRouteState.INSUFFICIENT_ORDER_EVIDENCE,
            (),
            (),
            refs,
            "ordered_operational_evidence",
        )

    by_fragment: dict[str, list[OrderedOperationEvidence]] = {}
    for op in relevant:
        key = op.fragment_id.strip().upper()
        by_fragment.setdefault(key, []).append(op)

    ordered: list[tuple[str, tuple[str, ...]]] = []
    for fragment_id, items in sorted(by_fragment.items()):
        sequences = [item.sequence for item in items]
        if len(sequences) != len(set(sequences)):
            refs = tuple(dict.fromkeys(item.source_ref for item in relevant))
            return PartialRouteAssessment(
                stage,
                PartialRouteState.INVALID_FRAGMENT_ORDER,
                (),
                (),
                refs,
                "unique_sequence_within_fragment",
            )
        items_sorted = sorted(items, key=lambda item: item.sequence)
        ordered.append((fragment_id, tuple(item.operation for item in items_sorted)))

    fragment_ids = tuple(fragment_id for fragment_id, _ in ordered)
    link_pairs = {
        (link.predecessor_fragment_id.strip().upper(), link.successor_fragment_id.strip().upper())
        for link in fragment_links
        if link.predecessor_fragment_id.strip().upper() in fragment_ids
        and link.successor_fragment_id.strip().upper() in fragment_ids
    }
    unresolved: list[tuple[str, str]] = []
    if len(fragment_ids) > 1:
        for left, right in zip(fragment_ids, fragment_ids[1:]):
            if (left, right) not in link_pairs and (right, left) not in link_pairs:
                unresolved.append((left, right))

    refs = tuple(
        dict.fromkeys(
            [item.source_ref for item in relevant]
            + [link.source_ref for link in fragment_links]
        )
    )
    if unresolved:
        return PartialRouteAssessment(
            stage,
            PartialRouteState.CROSS_FRAGMENT_ORDER_UNPROVEN,
            tuple(ordered),
            tuple(unresolved),
            refs,
            "explicit_cross_fragment_precedence",
        )

    return PartialRouteAssessment(
        stage,
        PartialRouteState.READY_FOR_ROUTE_PROPOSAL,
        tuple(ordered),
        (),
        refs,
        "governed_route_registration",
    )


__all__ = [
    "OrderedOperationEvidence",
    "PartialRouteAssessment",
    "PartialRouteState",
    "RouteFragmentLink",
    "assess_partial_route",
]
