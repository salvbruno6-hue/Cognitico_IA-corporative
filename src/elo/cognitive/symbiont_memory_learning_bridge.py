"""Governed bridge from Simbiont memory routing into learning handoff.

The bridge is intentionally non-authoritative: it consumes the read-only
LearningMemoryRouter decision and produces a handoff contract for existing
learning/lab owners. It never writes memory, creates an owner, or promotes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .learning_memory_router import (
    LearningMemoryRouter,
    LearningRequest,
    MemoryEntry,
    RouteAction,
    RoutingDecision,
)

if TYPE_CHECKING:
    from .symbionte_lab import SymbiontLabAdapter, SymbiontLabEvaluation, SymbiontLabObservation


@dataclass(frozen=True, slots=True)
class LearningHandoff:
    action: RouteAction
    destination_id: str | None
    related_memory_ids: tuple[str, ...]
    duplicate_memory_ids: tuple[str, ...]
    legacy_evidence_refs: tuple[str, ...]
    reasons: tuple[str, ...]
    learning_admission: str
    requires_lab: bool
    canonical_mutation: bool = False


@dataclass(frozen=True, slots=True)
class LearningLabHandoff:
    """Result of routing plus an optional handoff to the existing Lab."""

    routing: LearningHandoff
    evaluation: "SymbiontLabEvaluation | None" = None

    @property
    def entered_lab(self) -> bool:
        return self.evaluation is not None


class SymbiontMemoryLearningBridge:
    """Translate routing into an existing governed learning handoff."""

    def __init__(self, router: LearningMemoryRouter | None = None) -> None:
        self.router = router or LearningMemoryRouter()

    def route(
        self,
        request: LearningRequest,
        memories: tuple[MemoryEntry, ...] | list[MemoryEntry],
    ) -> LearningHandoff:
        decision = self.router.investigate(request, memories)
        return self._handoff(decision)

    def route_to_lab(
        self,
        request: LearningRequest,
        memories: tuple[MemoryEntry, ...] | list[MemoryEntry],
        *,
        observation: "SymbiontLabObservation",
        laboratory: "SymbiontLabAdapter",
        principal_id: str,
        dataset_version: str,
    ) -> LearningLabHandoff:
        """Route first; only a CANDIDATE may enter the canonical Lab.

        REUSE, AGGREGATE, BLOCKED and NO_OWNER terminate at the routing
        boundary. CANDIDATE is delegated to the existing SymbiontLabAdapter,
        which remains responsible for Evolution Gate and Governed Learning.
        """
        routing = self.route(request, memories)
        if routing.action is not RouteAction.CANDIDATE:
            return LearningLabHandoff(routing=routing)

        if observation.tenant_id != request.tenant_scope:
            raise ValueError("laboratory observation tenant does not match learning request")
        if observation.domain != request.domain:
            raise ValueError("laboratory observation domain does not match learning request")

        evaluation = laboratory.evaluate(
            observation,
            principal_id=principal_id,
            dataset_version=dataset_version,
        )
        return LearningLabHandoff(routing=routing, evaluation=evaluation)

    @staticmethod
    def _handoff(decision: RoutingDecision) -> LearningHandoff:
        if decision.action is RouteAction.REUSE:
            admission, lab = "REUSE_EXISTING", False
        elif decision.action is RouteAction.AGGREGATE:
            admission, lab = "AGGREGATE_EXISTING", False
        elif decision.action is RouteAction.CANDIDATE:
            admission, lab = "CANDIDATE_FOR_GOVERNED_LEARNING", True
        elif decision.action is RouteAction.BLOCKED:
            admission, lab = "BLOCKED", False
        else:
            admission, lab = "NO_OWNER", False

        return LearningHandoff(
            action=decision.action,
            destination_id=decision.destination.destination_id if decision.destination else None,
            related_memory_ids=decision.related_memory_ids,
            duplicate_memory_ids=decision.duplicate_memory_ids,
            legacy_evidence_refs=decision.legacy_evidence_refs,
            reasons=decision.reasons,
            learning_admission=admission,
            requires_lab=lab,
        )


__all__ = [
    "LearningHandoff",
    "LearningLabHandoff",
    "SymbiontMemoryLearningBridge",
]
