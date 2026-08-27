from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Iterable

from .types import MemoryItem, MemoryKind


@dataclass(frozen=True, slots=True)
class MemoryMatch:
    item: MemoryItem
    score: float


class CognitiveMemoryStore:
    """Small deterministic memory substrate; providers can later replace retrieval."""

    def __init__(self) -> None:
        self._items: dict[str, MemoryItem] = {}

    def put(self, item: MemoryItem) -> None:
        if item.kind is MemoryKind.CANONICAL and item.tenant_id:
            raise ValueError("canonical memory cannot carry tenant_id")
        self._items[item.id] = item

    def get(self, item_id: str) -> MemoryItem | None:
        return self._items.get(item_id)

    def search(
        self,
        query: str,
        *,
        tenant_id: str | None = None,
        kinds: frozenset[MemoryKind] = frozenset(),
        limit: int = 8,
    ) -> tuple[MemoryMatch, ...]:
        if limit < 1:
            raise ValueError("limit must be positive")
        tokens = {token.lower() for token in query.split() if token.strip()}
        matches: list[MemoryMatch] = []
        for item in self._items.values():
            if item.kind is MemoryKind.TENANT and item.tenant_id != tenant_id:
                continue
            if item.kind is not MemoryKind.TENANT and tenant_id is not None:
                # Non-tenant memory remains eligible; tenant memory is isolated.
                pass
            if kinds and item.kind not in kinds:
                continue
            haystack = f"{item.content} {item.source}".lower()
            overlap = sum(1 for token in tokens if token in haystack)
            if overlap:
                score = overlap / max(1, len(tokens))
                # Older/less-confident memories are naturally down-ranked without deletion.
                score *= max(0.0, min(1.0, item.confidence))
                matches.append(MemoryMatch(item, score))
        matches.sort(key=lambda match: (-match.score, match.item.id))
        return tuple(matches[:limit])

    def all(self) -> tuple[MemoryItem, ...]:
        return tuple(self._items.values())
