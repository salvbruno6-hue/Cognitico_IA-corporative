"""Read-only provider bridge from agentic orchestration to canonical ELO runtime.

This module is deliberately outside canonical Core/Cognitive/Forge authority.
It adapts existing ELO discovery/context/source-resolution components to the
framework-neutral KnowledgeProvider contract. Temporal retrieval tracing is
opt-in; the default agentic path does not append to canonical runtime memory.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.core.context_resolution import ContextQuery, ContextResolutionEngine
from elo.core.source_resolver import SourceResolutionRequest, SourceResolver

from .contracts import IntentSpec, KnowledgeCandidate, KnowledgeRequirement
from .orchestrator import KnowledgeProvider


@dataclass(frozen=True)
class ELORequestContext:
    tenant_id: str
    principal_id: str
    session_id: str
    request_id: str
    correlation_id: str
    conversation_id: str
    authorization_scope: str


class ELOKnowledgeProvider(KnowledgeProvider):
    """Translate agentic requirements into governed ELO retrieval calls."""

    def __init__(
        self,
        *,
        context_engine: ContextResolutionEngine | None = None,
        source_resolver: SourceResolver | None = None,
        context_factory: Callable[[IntentSpec, KnowledgeRequirement], ContextQuery] | None = None,
        request_context: ELORequestContext | None = None,
        allow_temporal_trace: bool = False,
    ) -> None:
        self.context_engine = context_engine or ContextResolutionEngine()
        self.source_resolver = source_resolver or SourceResolver()
        self.context_factory = context_factory or self._default_context_query
        self.request_context = request_context
        self.allow_temporal_trace = allow_temporal_trace

    def retrieve(
        self,
        intent: IntentSpec,
        requirement: KnowledgeRequirement,
    ) -> tuple[KnowledgeCandidate, ...]:
        request_context = self.request_context
        if request_context is None:
            return ()

        query = self.context_factory(intent, requirement)
        pack = self.context_engine.resolve(query)
        if pack.discovery_plan is None:
            return ()

        candidates: list[KnowledgeCandidate] = []
        resolver = self.source_resolver
        if not self.allow_temporal_trace:
            resolver = SourceResolver(
                adapters=tuple(resolver._adapters.values()),
                temporal_memory=_NullTemporalMemory(),
            )

        for source_candidate in self.context_engine.candidate_sources(pack):
            resolution = resolver.resolve(
                source_candidate,
                SourceResolutionRequest(
                    query=source_candidate.query,
                    tenant_id=request_context.tenant_id,
                    domain=query.domain or "general",
                    principal_id=request_context.principal_id,
                    session_id=request_context.session_id,
                    request_id=request_context.request_id,
                    correlation_id=request_context.correlation_id,
                    conversation_id=request_context.conversation_id,
                    authorization_scope=request_context.authorization_scope,
                    metadata={
                        "agentic_requirement": requirement.key,
                        "agentic_intent": intent.intent,
                    },
                ),
            )
            for item in resolution.retrieved:
                metadata = dict(item.metadata)
                metadata.setdefault("agentic_requirement", requirement.key)
                candidates.append(
                    KnowledgeCandidate(
                        source_id=item.source_id,
                        content=item.content,
                        source_type=item.source_type,
                        status="REFERENCE",
                        relevance=0.0,
                        confidence=0.0,
                        context_match=0.0,
                        provenance=item.provenance,
                        metadata=metadata,
                    )
                )
        return tuple(candidates)

    @staticmethod
    def _default_context_query(
        intent: IntentSpec,
        requirement: KnowledgeRequirement,
    ) -> ContextQuery:
        return ContextQuery(
            question=f"{intent.question}\nKnowledge requirement: {requirement.key} — {requirement.purpose}",
            entity=intent.entity,
            scope=intent.active_context,
            domain=intent.domain,
            request_id=intent.metadata.get("request_id"),
            correlation_id=intent.metadata.get("correlation_id"),
            session_id=intent.metadata.get("session_id"),
            tenant_id=intent.metadata.get("tenant_id"),
            principal_id=intent.metadata.get("principal_id"),
        )


class _NullTemporalMemory:
    """No-op memory sink for agentic reads that are not explicitly traced."""

    def append(self, **_: object) -> None:
        return None
