"""Governed reuse of validated learning in future Symbiont decisions.

This module is deliberately read-only. It converts already-routed, validated
learning memories into decision context. It does not create memory, approve
learning, authorize execution, or mutate Core.

The source of truth remains the existing LearningMemoryRouter and its canonical
owners.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .learning_memory_router import LearningRequest, MemoryEntry, RouteAction


@dataclass(frozen=True, slots=True)
class DecisionLearningSignal:
    memory_id: str
    destination_id: str
    tenant_scope: str
    domain: str
    concept_key: str
    source_ref: str
    reason: str
    confidence: float


@dataclass(frozen=True, slots=True)
class DecisionLearningContext:
    signals: tuple[DecisionLearningSignal, ...]
    source_memory_ids: tuple[str, ...]
    reusable: bool
    canonical_mutation: bool = False
    authorization_granted: bool = False


def build_decision_learning_context(
    request: LearningRequest,
    memories: Iterable[MemoryEntry],
    *,
    routing_action: RouteAction,
    destination_id: str | None,
) -> DecisionLearningContext:
    """Return only validated, tenant/domain-aligned learning for reuse.

    CANDIDATE is intentionally excluded: candidate learning must first pass
    the existing laboratory/evolution process. REUSE/AGGREGATE may contribute
    existing canonical learning context.
    """
    if routing_action not in {RouteAction.REUSE, RouteAction.AGGREGATE}:
        return DecisionLearningContext((), (), False)

    if not request.validated or not destination_id:
        return DecisionLearningContext((), (), False)

    signals: list[DecisionLearningSignal] = []
    for memory in memories:
        if memory.tenant_scope != request.tenant_scope:
            continue
        if memory.domain != request.domain:
            continue
        if memory.destination_id != destination_id:
            continue
        if memory.status.upper() not in {"VALIDATED", "APPROVED", "PROMOTABLE_KNOWLEDGE"}:
            continue
        if memory.concept_key.strip().lower() != request.concept_key.strip().lower():
            continue
        signals.append(
            DecisionLearningSignal(
                memory_id=memory.memory_id,
                destination_id=destination_id,
                tenant_scope=memory.tenant_scope,
                domain=memory.domain,
                concept_key=memory.concept_key,
                source_ref=memory.source_ref,
                reason="validated canonical learning matches current decision context",
                confidence=1.0,
            )
        )

    unique = tuple({signal.memory_id: signal for signal in signals}.values())
    return DecisionLearningContext(
        signals=unique,
        source_memory_ids=tuple(signal.memory_id for signal in unique),
        reusable=bool(unique),
    )


__all__ = ["DecisionLearningContext", "DecisionLearningSignal", "build_decision_learning_context"]
