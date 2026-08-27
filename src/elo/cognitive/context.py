from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ContextItem:
    """Evidence or state item admitted into a cognitive context."""

    key: str
    value: str
    source: str
    confidence: float = 1.0
    scope: str = "session"

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("key cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class CognitiveContext:
    """Normalized context passed to reasoning without exposing tenant internals."""

    task: str
    tenant_id: str | None = None
    constraints: tuple[str, ...] = ()
    evidence: tuple[ContextItem, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def high_confidence_evidence(self, threshold: float = 0.7) -> tuple[ContextItem, ...]:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1")
        return tuple(item for item in self.evidence if item.confidence >= threshold)
