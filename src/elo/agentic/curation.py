"""Deterministic, framework-neutral curation for retrieved ELO knowledge."""

from __future__ import annotations

from .contracts import KnowledgeCandidate

_STATUS_RANK = {
    "CANONICAL": 100,
    "GOVERNED": 95,
    "APPLICABLE": 90,
    "CURRENT": 85,
    "REFERENCE": 50,
    "HISTORICAL": 35,
    "UNVERIFIED": 20,
    "INSUFFICIENT": 10,
    "OUTDATED": 5,
    "CONFLICTING": 0,
}


def _score(value: str | None) -> float:
    if value is None:
        return 0.0
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def curate(candidates: tuple[KnowledgeCandidate, ...], limit: int) -> tuple[KnowledgeCandidate, ...]:
    """Deduplicate and deterministically rank candidates without changing truth."""
    unique: dict[str, KnowledgeCandidate] = {}
    for item in candidates:
        current = unique.get(item.source_id)
        if current is None or _rank(item) > _rank(current):
            unique[item.source_id] = item

    return tuple(sorted(unique.values(), key=_rank, reverse=True)[:limit])


def _rank(item: KnowledgeCandidate) -> tuple[float, float, float, float, int, str]:
    return (
        float(_STATUS_RANK.get(item.status, 0)),
        item.context_match,
        item.relevance,
        item.confidence,
        -len(item.content),
        item.source_id,
    )
