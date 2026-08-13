"""Intent-driven context resolution for ELO.

The resolver bridges the canonical source-discovery planner and the context
pack consumed by ELO/GPT. Retrieval remains adapter-owned; this layer decides
what context is required, applies scope rules, and records evidence without
promoting it to canonical knowledge.
"""

from dataclasses import dataclass, field
from typing import Mapping

from .source_discovery import DiscoveryPlan, SourceCandidate, SourceDiscoveryEngine


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
    discovery_plan: DiscoveryPlan | None = None
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

    def requires_specialist(self) -> bool:
        """GPT may be used as specialist only after context discovery."""
        return bool(self.discovery_plan and self.sufficient_evidence())


class ContextResolutionEngine:
    """Resolve context requirements without requiring user-supplied paths."""

    def __init__(self, discovery: SourceDiscoveryEngine | None = None) -> None:
        self._discovery = discovery or SourceDiscoveryEngine()

    def resolve(self, query: ContextQuery) -> ContextPack:
        if not query.question.strip():
            raise ValueError("question is required")

        plan = self._discovery.plan(
            query.question,
            known_entities=((query.entity,) if query.entity else ()),
        )
        return ContextPack(
            query=query,
            discovery_plan=plan,
            uncertainties=(
                "retrieval pending: authorized source adapters must execute the discovery plan",
            ),
        )

    @staticmethod
    def candidate_sources(pack: ContextPack) -> tuple[SourceCandidate, ...]:
        if not pack.discovery_plan:
            return ()
        return pack.discovery_plan.candidates
