"""Intent-driven context resolution for ELO.

The resolver bridges canonical source discovery and the context pack consumed
by ELO/GPT. Retrieval remains adapter-owned; this layer decides what context is
required, applies tenant/entity/scope rules, and records evidence without
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
    tenant_id: str | None = None
    domain: str | None = None
    principal_id: str | None = None
    session_id: str | None = None
    request_id: str | None = None
    correlation_id: str | None = None


@dataclass(frozen=True)
class ContextSource:
    source_id: str
    source_type: str
    authority: str
    scope: str | None = None
    tenant_id: str | None = None
    domain: str | None = None
    principal_id: str | None = None
    provenance: Mapping[str, str] = field(default_factory=dict)
    temporal_validity: str | None = None


@dataclass(frozen=True)
class ContextEvidence:
    source_id: str
    fact: str
    confidence: float
    observed_at: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)
    tenant_id: str | None = None
    scope: str | None = None
    domain: str | None = None
    provenance: Mapping[str, str] = field(default_factory=dict)
    temporal_validity: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id or not self.fact:
            raise ValueError("source_id and fact are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class ContextPack:
    query: ContextQuery
    discovery_plan: DiscoveryPlan | None = None
    sources: tuple[ContextSource, ...] = ()
    evidence: tuple[ContextEvidence, ...] = ()
    uncertainties: tuple[str, ...] = ()
    gaps: tuple[str, ...] = ()

    def scoped_sources(self) -> tuple[ContextSource, ...]:
        return tuple(
            source for source in self.sources
            if (not self.query.tenant_id or source.tenant_id in (None, self.query.tenant_id))
            and (not self.query.domain or source.domain in (None, self.query.domain))
            and (not self.query.scope or source.scope in (None, self.query.scope))
            and (not self.query.principal_id or source.principal_id in (None, self.query.principal_id))
        )

    def scoped_evidence(self) -> tuple[ContextEvidence, ...]:
        source_map = {source.source_id: source for source in self.scoped_sources()}
        candidates = self.evidence
        if source_map:
            candidates = tuple(evidence for evidence in candidates if evidence.source_id in source_map)

        scoped: list[ContextEvidence] = []
        for evidence in candidates:
            source = source_map.get(evidence.source_id)
            effective_tenant = evidence.tenant_id or (source.tenant_id if source else None)
            effective_domain = evidence.domain or (source.domain if source else None)
            effective_scope = evidence.scope or (source.scope if source else None)
            effective_principal = evidence.provenance.get("principal_id") or (
                source.principal_id if source else None
            )
            if self.query.tenant_id and effective_tenant != self.query.tenant_id:
                continue
            if self.query.domain and effective_domain != self.query.domain:
                continue
            if self.query.scope and effective_scope != self.query.scope:
                continue
            if self.query.principal_id and effective_principal not in (None, self.query.principal_id):
                continue
            if evidence.tenant_id and source and source.tenant_id and evidence.tenant_id != source.tenant_id:
                continue
            if evidence.domain and source and source.domain and evidence.domain != source.domain:
                continue
            if evidence.scope and source and source.scope and evidence.scope != source.scope:
                continue
            scoped.append(evidence)
        return tuple(scoped)

    def sufficient_evidence(self, minimum_confidence: float = 0.6) -> bool:
        return any(evidence.confidence >= minimum_confidence for evidence in self.scoped_evidence())

    def requires_specialist(self) -> bool:
        """GPT may be used as specialist only after discovery and scoped evidence."""
        return bool(self.discovery_plan and self.sufficient_evidence())

    def evidence_ids(self) -> tuple[str, ...]:
        return tuple(evidence.source_id for evidence in self.scoped_evidence())

    def integrity_gaps(self) -> tuple[str, ...]:
        gaps = list(self.gaps)
        if self.query.tenant_id and not self.scoped_sources():
            gaps.append("no authorized source in requested tenant")
        if self.query.domain and self.sources and not any(
            source.domain in (None, self.query.domain) for source in self.sources
        ):
            gaps.append("source domain does not match requested domain")
        if self.query.principal_id and self.evidence and not self.scoped_evidence():
            gaps.append("evidence is not authorized for requested principal")
        return tuple(dict.fromkeys(gaps))

    def consultation_payload(self) -> Mapping[str, object]:
        """Produce a bounded handoff payload; it contains no private reasoning trace."""
        gaps = self.integrity_gaps()
        return {
            "question": self.query.question,
            "entity": self.query.entity,
            "scope": self.query.scope,
            "tenant_id": self.query.tenant_id,
            "domain": self.query.domain,
            "principal_id": self.query.principal_id,
            "request_id": self.query.request_id,
            "correlation_id": self.query.correlation_id,
            "evidence_ids": self.evidence_ids(),
            "evidence": tuple(self.scoped_evidence()),
            "uncertainties": self.uncertainties,
            "gaps": gaps,
            "requires_human_decision": bool(gaps),
        }


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
            gaps=("retrieval pending",),
        )

    def enrich(
        self,
        pack: ContextPack,
        *,
        sources: tuple[ContextSource, ...] = (),
        evidence: tuple[ContextEvidence, ...] = (),
        uncertainties: tuple[str, ...] = (),
        gaps: tuple[str, ...] = (),
    ) -> ContextPack:
        """Attach adapter results while preserving immutable context and scope."""
        merged_sources = {source.source_id: source for source in pack.sources}
        merged_sources.update({source.source_id: source for source in sources})
        merged_evidence = {item.source_id: item for item in pack.evidence}
        merged_evidence.update({item.source_id: item for item in evidence})
        inherited_gaps = tuple(gap for gap in pack.gaps if gap != "retrieval pending")
        return ContextPack(
            query=pack.query,
            discovery_plan=pack.discovery_plan,
            sources=tuple(merged_sources.values()),
            evidence=tuple(merged_evidence.values()),
            uncertainties=tuple(dict.fromkeys(pack.uncertainties + uncertainties)),
            gaps=tuple(dict.fromkeys(inherited_gaps + gaps)),
        )

    @staticmethod
    def candidate_sources(pack: ContextPack) -> tuple[SourceCandidate, ...]:
        if not pack.discovery_plan:
            return ()
        return pack.discovery_plan.candidates
