"""Precedent retrieval over closed, evidence-backed decision cycles."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .decision_outcome_loop import DecisionLifecycle, DecisionState


@dataclass(frozen=True)
class Precedent:
    decision_id: str
    domain: str
    context_keys: tuple[str, ...]
    outcome_summary: str
    evidence_ids: tuple[str, ...]


class PrecedentIndex:
    """Deterministic contextual index; closed cycles only."""

    def __init__(self) -> None:
        self._items: dict[str, Precedent] = {}

    def add(self, lifecycle: DecisionLifecycle, *, domain: str, context_keys: Iterable[str], outcome_summary: str) -> Precedent:
        if lifecycle.state != DecisionState.CLOSED:
            raise ValueError("only closed decision cycles can become precedents")
        if lifecycle.outcome is None:
            raise ValueError("precedent requires an outcome")
        evidence_ids = tuple(dict.fromkeys(lifecycle.outcome.evidence_ids))
        if not evidence_ids:
            raise ValueError("precedent requires evidence")
        precedent = Precedent(
            decision_id=lifecycle.decision.decision_id,
            domain=domain,
            context_keys=tuple(dict.fromkeys(context_keys)),
            outcome_summary=outcome_summary,
            evidence_ids=evidence_ids,
        )
        self._items[precedent.decision_id] = precedent
        return precedent

    def find(self, *, domain: str, context_keys: Iterable[str], limit: int = 10) -> tuple[Precedent, ...]:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        wanted = set(context_keys)
        scored = []
        for item in self._items.values():
            if item.domain != domain:
                continue
            overlap = len(wanted.intersection(item.context_keys))
            if overlap:
                scored.append((overlap, item))
        scored.sort(key=lambda pair: (-pair[0], pair[1].decision_id))
        return tuple(item for _, item in scored[:limit])
