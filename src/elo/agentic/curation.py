"""Deterministic, framework-neutral curation for retrieved ELO knowledge."""

from __future__ import annotations

from .contracts import IntentSpec, KnowledgeCandidate

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


def _context_score(item: KnowledgeCandidate, intent: IntentSpec) -> float:
    score = item.context_match
    active = intent.active_context
    if active:
        metadata = item.metadata
        for key in ("active_context", "orcamento_id", "so", "projeto"):
            value = metadata.get(key)
            if value:
                score = max(score, 1.0 if value == active else 0.0)
        provenance = item.provenance
        for key in ("active_context", "orcamento_id", "so", "projeto"):
            value = provenance.get(key)
            if value:
                score = max(score, 1.0 if value == active else 0.0)
    if intent.entity:
        for mapping in (item.metadata, item.provenance):
            for key in ("entity", "orcamento_id", "so", "projeto"):
                value = mapping.get(key)
                if value:
                    if value == intent.entity:
                        score = max(score, 1.0)
                    elif intent.entity.casefold() in value.casefold():
                        score = max(score, 0.75)
    return max(0.0, min(1.0, score))


def curate(
    candidates: tuple[KnowledgeCandidate, ...],
    limit: int,
    *,
    intent: IntentSpec | None = None,
) -> tuple[KnowledgeCandidate, ...]:
    """Deduplicate and deterministically rank candidates without changing truth."""
    if limit <= 0:
        return ()
    unique: dict[str, KnowledgeCandidate] = {}
    for item in candidates:
        current = unique.get(item.source_id)
        if current is None or _rank(item, intent) > _rank(current, intent):
            unique[item.source_id] = item

    return tuple(
        sorted(unique.values(), key=lambda item: _rank(item, intent), reverse=True)[:limit]
    )


def _rank(
    item: KnowledgeCandidate,
    intent: IntentSpec | None = None,
) -> tuple[float, float, float, float, float, int, str]:
    context = item.context_match if intent is None else _context_score(item, intent)
    return (
        float(_STATUS_RANK.get(item.status, 0)),
        context,
        item.relevance,
        item.confidence,
        _score(item.metadata.get("authority")),
        -len(item.content),
        item.source_id,
    )
