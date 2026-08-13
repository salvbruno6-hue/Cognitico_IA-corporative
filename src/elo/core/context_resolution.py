"""Intent-driven context resolution for ELO.

Resolves an entity and scope before specialist handoff, allowing ELO to
assemble an evidence-oriented Context Pack from authorized sources without
requiring the user to provide repository/project paths.
"""

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class ContextQuery:
    question: str
    entity: str | None = None
    scope: str | None = None
    dimensions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContextSource:
    source_id: str
    source_type: str
    authority: str
    scope: str | None = None


@dataclass(frozen=True)
class ContextEvidence:
    source_id: str
    fact: str
    confidence: float
    observed_at: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ContextPack:
    query: ContextQuery
    sources: tuple[ContextSource, ...] = ()
    evidence: tuple[ContextEvidence, ...] = ()
    uncertainties: tuple[str, ...] = ()

    def scoped_sources(self) -> tuple[ContextSource, ...]:
        if not self.query.scope:
            return self.sources
        return tuple(
            source for source in self.sources
            if source.scope in (None, self.query.scope)
        )

    def sufficient_evidence(self, minimum_confidence: float = 0.6) -> bool:
        return any(
            evidence.confidence >= minimum_confidence
            for evidence in self.evidence
        )
