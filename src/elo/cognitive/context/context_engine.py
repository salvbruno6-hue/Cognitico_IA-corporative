from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContextSignal:
    name: str
    value: str
    weight: float = 1.0
    source: str = "runtime"


@dataclass(frozen=True, slots=True)
class CognitiveContext:
    query: str
    tenant_id: str | None
    signals: tuple[ContextSignal, ...]

    @property
    def evidence_score(self) -> float:
        if not self.signals:
            return 0.0
        weights = sum(max(0.0, s.weight) for s in self.signals)
        if weights == 0:
            return 0.0
        return min(1.0, weights / (len(self.signals) * max(1.0, weights)))


def resolve_context(query: str, *, tenant_id: str | None = None, signals: tuple[ContextSignal, ...] = ()) -> CognitiveContext:
    if not query.strip():
        raise ValueError("query must not be empty")
    return CognitiveContext(query=query.strip(), tenant_id=tenant_id, signals=signals)
