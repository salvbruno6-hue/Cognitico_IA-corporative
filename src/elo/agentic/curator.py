"""Context-aware deterministic curation for GPT↔ELO retrieval."""

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


class KnowledgeCurator:
    """Rank and deduplicate candidates without changing their asserted truth."""

    def curate(
        self,
        candidates: tuple[KnowledgeCandidate, ...],
        *,
        active_context: str | None = None,
        limit: int = 50,
    ) -> tuple[KnowledgeCandidate, ...]:
        if limit <= 0:
            return ()
        unique: dict[str, KnowledgeCandidate] = {}
        for item in candidates:
            current = unique.get(item.source_id)
            if current is None or self._rank(item, active_context) > self._rank(current, active_context):
                unique[item.source_id] = item
        return tuple(
            sorted(
                unique.values(),
                key=lambda item: self._rank(item, active_context),
                reverse=True,
            )[:limit]
        )

    @staticmethod
    def _rank(
        item: KnowledgeCandidate,
        active_context: str | None,
    ) -> tuple[float, float, float, float, float, str]:
        context = item.context_match
        metadata_context = item.metadata.get("active_context")
        if active_context and metadata_context:
            context = 1.0 if metadata_context == active_context else min(context, 0.25)
        return (
            float(_STATUS_RANK.get(item.status, 0)),
            context,
            item.relevance,
            item.confidence,
            -len(item.content),
            item.source_id,
        )
