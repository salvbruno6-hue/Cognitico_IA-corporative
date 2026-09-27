"""Read-only provider bridge from agentic orchestration to canonical ELO runtime.

This module is deliberately outside canonical Core/Cognitive/Forge authority.
It adapts existing ELO discovery/context/source-resolution components to the
framework-neutral KnowledgeProvider contract. Retrieval tracing is explicit:
agentic reads never append to canonical temporal memory unless the caller opts
in with ``allow_temporal_trace=True``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.agent_intake.hermes_context_plugin_adapter import ContextPluginAdapter
from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal
from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_execution_id,
    create_runtime_evidence,
)

from elo.core.context_resolution import ContextQuery, ContextResolutionEngine
from elo.core.source_resolver import (
    SourceResolutionRequest,
    SourceResolver,
    SourceResolverAdapter,
)

from .contracts import IntentSpec, KnowledgeCandidate, KnowledgeRequirement
from .orchestrator import KnowledgeProvider
from .runtime_context import ELORuntimeContext, resolve_runtime_context


@dataclass(frozen=True)
class ELORequestContext:
    tenant_id: str
    principal_id: str
    session_id: str
    request_id: str
    correlation_id: str
    conversation_id: str
    authorization_scope: str


class _NullTemporalMemory:
    """Discard temporal traces for observational agentic reads."""

    def append(self, **_: object) -> None:
        return None


class ELOKnowledgeProvider(KnowledgeProvider):
    """Translate agentic requirements into governed ELO retrieval calls."""

    def __init__(
        self,
        *,
        context_engine: ContextResolutionEngine | None = None,
        source_resolver: SourceResolver | None = None,
        context_factory: Callable[[IntentSpec, KnowledgeRequirement], ContextQuery] | None = None,
        request_context: ELORequestContext | None = None,
        runtime_context: ELORuntimeContext | None = None,
        allow_temporal_trace: bool = False,
        context_plugin_signal: ContextEnginePluginSignal | None = None,
        operational_evidence_sink: Callable[[RuntimeOperationalEvidence], None] | None = None,
        runtime_commit: str = "UNSPECIFIED",
    ) -> None:
        self.context_engine = context_engine or ContextResolutionEngine()
        self.source_resolver = source_resolver or SourceResolver()
        self.context_factory = context_factory or self._default_context_query
        self.request_context = request_context
        self.runtime_context = runtime_context or resolve_runtime_context()
        self.allow_temporal_trace = allow_temporal_trace
        self.context_plugin_signal = context_plugin_signal
        self.operational_evidence_sink = operational_evidence_sink
        self.runtime_commit = runtime_commit

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
        if self.context_plugin_signal is not None:
            execution_id = create_execution_id("EXT-CONTEXT-PLUGIN-HERMES")
            adapted = ContextPluginAdapter(self.context_engine).adapt(pack, self.context_plugin_signal)
            pack = adapted.pack
            if adapted.adapted and self.operational_evidence_sink is not None:
                trace = request_context.correlation_id or request_context.request_id
                evidence = create_runtime_evidence(
                    execution_id=execution_id,
                    candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
                    owner="HERMES-CONTEXT",
                    runtime_entrypoint="ELOKnowledgeProvider.retrieve",
                    action_observed=True,
                    metric="context_plugin_activation_success_rate",
                    direction="maximize",
                    baseline=0.0,
                    observed_value=1.0,
                    attribution="candidate",
                    provenance=RuntimeProvenance(
                        commit=self.runtime_commit,
                        runtime_trace=trace,
                        test_run=request_context.request_id,
                    ),
                    regression=False,
                    repeatability=RepeatabilityEvidence(2, 2, 1.0),
                )
                self.operational_evidence_sink(evidence)
        if pack.discovery_plan is None:
            return ()

        resolver = self._resolver_for_mode()
        candidates: list[KnowledgeCandidate] = []
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
                        "elo_forge_project_ref": self.runtime_context.project_ref,
                        "elo_forge_source": self.runtime_context.source_name,
                    },
                ),
            )
            for item in resolution.retrieved:
                metadata = dict(item.metadata)
                metadata.setdefault("agentic_requirement", requirement.key)
                product_code = (
                    metadata.get("cod_produt")
                    or metadata.get("produto_codigo")
                    or metadata.get("product_code")
                )
                candidates.append(
                    KnowledgeCandidate(
                        source_id=item.source_id,
                        content=item.content,
                        source_type=item.source_type,
                        status="REFERENCE",
                        relevance=0.0,
                        confidence=0.0,
                        context_match=0.0,
                        product_code=product_code,
                        provenance=item.provenance,
                        metadata=metadata,
                    )
                )
        return tuple(candidates)

    def _resolver_for_mode(self) -> SourceResolver:
        if self.allow_temporal_trace:
            return self.source_resolver

        adapters: tuple[SourceResolverAdapter, ...] = tuple(
            self.source_resolver._adapters.values()
        )
        return SourceResolver(adapters=adapters, temporal_memory=_NullTemporalMemory())

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
