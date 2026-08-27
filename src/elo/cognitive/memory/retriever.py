from __future__ import annotations

from dataclasses import dataclass

from ..memory.store import CognitiveMemoryStore, MemoryMatch


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    matches: tuple[MemoryMatch, ...]

    @property
    def confidence(self) -> float:
        if not self.matches:
            return 0.0
        return max(m.score for m in self.matches)


class CognitiveRetriever:
    def __init__(self, store: CognitiveMemoryStore) -> None:
        self.store = store

    def retrieve(self, query: str, *, tenant_id: str | None = None, limit: int = 8) -> RetrievalResult:
        return RetrievalResult(self.store.search(query, tenant_id=tenant_id, limit=limit))
