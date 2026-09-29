"""Governed bridge from Simbiont memory routing into learning handoff.

The bridge is intentionally non-authoritative: it consumes the read-only
LearningMemoryRouter decision and produces a handoff contract for existing
learning/lab owners. It never writes memory, creates an owner, or promotes.
"""

from __future__ import annotations

from dataclasses import dataclass

from .learning_memory_router import LearningMemoryRouter, LearningRequest, MemoryEntry, RouteAction, RoutingDecision


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


__all__ = ["LearningHandoff", "SymbiontMemoryLearningBridge"]
