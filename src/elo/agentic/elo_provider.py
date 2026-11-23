"""Read-only provider bridge from agentic orchestration to canonical ELO runtime.

This module is deliberately outside canonical Core/Cognitive/Forge authority.
It adapts existing ELO discovery/context/source-resolution components to the
framework-neutral KnowledgeProvider contract. Retrieval tracing is explicit:
agentic reads never append to canonical temporal memory unless the caller opts
in with ``allow_temporal_trace=True``.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Mapping

from elo.agent_intake.hermes_context_plugin_adapter import ContextPluginAdapter
from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal
from elo.agent_intake.hermes_memory_provider_adapter import adapt_memory_provider
from elo.agent_intake.hermes_memory_provider_boundary import MemoryProviderSignal
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
from elo.observability.cognitive_timing import (
    CognitiveTimingObservation,
    CognitiveTimingSink,
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


_LOW_CRITICALITY_MINIMUM_SIGNAL = 0.60
_LOW_CRITICALITY_EARLY_STOP_STATUSES = frozenset({
    "CANONICAL", "GOVERNED", "APPLICABLE", "CURRENT",
})


_KNOWLEDGE_STATUSES = frozenset({
    "APPLICABLE", "CANONICAL", "GOVERNED", "CURRENT", "REFERENCE",
    "HISTORICAL", "CONFLICTING", "OUTDATED", "UNVERIFIED", "INSUFFICIENT",
})


def _explicit_value(
    metadata: Mapping[str, str],
    provenance: Mapping[str, str],
    *keys: str,
) -> str | None:
    """Return the first explicitly supplied signal without synthesizing one."""
    for mapping in (metadata, provenance):
        for key in keys:
            if key not in mapping:
                continue
            value = str(mapping[key]).strip()
            return value or None
    return None


def _bounded_signal(
    metadata: Mapping[str, str],
    provenance: Mapping[str, str],
    key: str,
) -> float:
    """Preserve a declared 0..1 score; malformed/out-of-range stays neutral."""
    value = _explicit_value(metadata, provenance, key)
    if value is None:
        return 0.0
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return 0.0
    return parsed if 0.0 <= parsed <= 1.0 else 0.0


def _knowledge_status(
    metadata: Mapping[str, str],
    provenance: Mapping[str, str],
) -> str:
    """Generic RetrievedSource cannot self-promote canonical/governed status."""
    return "REFERENCE"


def _authority(
    metadata: Mapping[str, str],
    provenance: Mapping[str, str],
) -> str | None:
    return _explicit_value(metadata, provenance, "authority")


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
        hermes_memory_provider_signal: MemoryProviderSignal | None = None,
        runtime_evidence_sink=None,
        timing_sink: CognitiveTimingSink | None = None,
        clock: Callable[[], float] = perf_counter,
    ) -> None:
        self.context_engine = context_engine or ContextResolutionEngine()
        self.source_resolver = source_resolver or SourceResolver()
        self.context_factory = context_factory or self._default_context_query
        self.request_context = request_context
        self.runtime_context = runtime_context or resolve_runtime_context()
        self.allow_temporal_trace = allow_temporal_trace
        self.context_plugin_signal = context_plugin_signal
        self.hermes_memory_provider_signal = hermes_memory_provider_signal
        self.runtime_evidence_sink = runtime_evidence_sink
        self.timing_sink = timing_sink
        self._clock = clock

    @staticmethod
    def _decision_criticality(intent: IntentSpec) -> str:
        value = str(intent.metadata.get("decision_criticality", "")).strip().upper()
        return value if value in {"LOW", "MEDIUM", "HIGH", "CRITICAL"} else "UNSPECIFIED"

    @staticmethod
    def _low_criticality_candidate_is_sufficient(item: KnowledgeCandidate) -> bool:
        return (
            item.status in _LOW_CRITICALITY_EARLY_STOP_STATUSES
            and item.relevance >= _LOW_CRITICALITY_MINIMUM_SIGNAL
            and item.confidence >= _LOW_CRITICALITY_MINIMUM_SIGNAL
            and item.context_match >= _LOW_CRITICALITY_MINIMUM_SIGNAL
            and bool(item.authority and item.authority.strip())
            and bool(item.provenance)
        )

    def _record_timing(
        self,
        *,
        intent: IntentSpec,
        requirement: KnowledgeRequirement,
        stage: str,
        duration_ms: float,
        candidate_count: int = 0,
        metadata: Mapping[str, str] | None = None,
    ) -> None:
        if self.timing_sink is None:
            return
        try:
            self.timing_sink.record(
                CognitiveTimingObservation(
                    stage=stage,
                    duration_ms=max(0.0, duration_ms),
                    correlation_id=str(intent.metadata.get("correlation_id", "")),
                    requirement_key=requirement.key,
                    candidate_count=candidate_count,
                    metadata=dict(metadata or {}),
                )
            )
        except Exception:
            # Observability must never alter retrieval or cognitive output.
            return

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
            adapted = ContextPluginAdapter(self.context_engine).adapt(pack, self.context_plugin_signal)
            pack = adapted.pack
            if adapted.adapted and self.runtime_evidence_sink is not None and self.runtime_context.runtime_commit:
                self.runtime_evidence_sink.append(create_runtime_evidence(
                    execution_id=create_execution_id("EXT-CONTEXT-PLUGIN-HERMES"),
                    candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
                    owner="ELO Context",
                    runtime_entrypoint="elo.context.resolve",
                    action_observed=True,
                    metric="context_plugin_activation_success_rate",
                    direction="maximize",
                    baseline=0.0,
                    observed_value=1.0,
                    attribution="candidate",
                    provenance=RuntimeProvenance(
                        commit=self.runtime_context.runtime_commit,
                        runtime_trace=(request_context.correlation_id or request_context.request_id),
                    ),
                    regression=False,
                    repeatability=RepeatabilityEvidence(1, 1, 1.0),
                ))
        if pack.discovery_plan is None:
            return ()

        resolver = self._resolver_for_mode()
        candidates: list[KnowledgeCandidate] = []
        memory_contract = None
        if self.hermes_memory_provider_signal is not None:
            memory_contract = adapt_memory_provider(self.hermes_memory_provider_signal)
            if memory_contract is None:
                raise PermissionError("Hermes memory-provider policy rejected retrieval")
            if memory_contract.tenant_scope != request_context.tenant_id:
                raise PermissionError("Hermes memory-provider tenant scope mismatch")

        provider_started = self._clock()
        source_attempts = 0
        early_stop_applied = False
        early_stop_eligible_detected = False
        first_sufficient_attempt = 0
        criticality = self._decision_criticality(intent)

        for source_candidate in self.context_engine.candidate_sources(pack):
            if memory_contract is not None and source_candidate.kind != memory_contract.provider_id:
                continue
            source_started = self._clock()
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
            source_attempts += 1
            source_candidates: list[KnowledgeCandidate] = []
            for item in resolution.retrieved:
                if memory_contract is not None:
                    provenance_refs = tuple(
                        ref for ref in (
                            item.source_id,
                            item.provenance.get("adapter_kind"),
                            item.provenance.get("adapter_capability"),
                        ) if ref
                    )
                    if not set(memory_contract.source_refs).intersection(provenance_refs):
                        raise PermissionError("retrieved evidence does not match Hermes memory-provider contract")
                    if self.runtime_evidence_sink is not None and self.runtime_context.runtime_commit:
                        self.runtime_evidence_sink.append(create_runtime_evidence(
                            execution_id=create_execution_id("EXT-MEMPROVIDER-HERMES"),
                            candidate_id="EXT-MEMPROVIDER-HERMES",
                            owner="ELO Memory Retrieval",
                            runtime_entrypoint="ELOKnowledgeProvider.retrieve",
                            action_observed=True,
                            metric="provider_identity_provenance_preservation_rate",
                            direction="maximize",
                            baseline=0.0,
                            observed_value=1.0,
                            attribution="candidate",
                            provenance=RuntimeProvenance(
                                commit=self.runtime_context.runtime_commit,
                                runtime_trace=(request_context.correlation_id or request_context.request_id),
                            ),
                            regression=False,
                            repeatability=RepeatabilityEvidence(1, 1, 1.0),
                        ))
                metadata = dict(item.metadata)
                provenance = dict(item.provenance)
                metadata.setdefault("agentic_requirement", requirement.key)
                product_code = (
                    metadata.get("cod_produt")
                    or metadata.get("produto_codigo")
                    or metadata.get("product_code")
                )
                candidate = KnowledgeCandidate(
                    source_id=item.source_id,
                    content=item.content,
                    source_type=item.source_type,
                    status=_knowledge_status(metadata, provenance),
                    relevance=_bounded_signal(metadata, provenance, "relevance"),
                    confidence=_bounded_signal(metadata, provenance, "confidence"),
                    context_match=_bounded_signal(metadata, provenance, "context_match"),
                    authority=_authority(metadata, provenance),
                    product_code=product_code,
                    provenance=provenance,
                    metadata=metadata,
                )
                candidates.append(candidate)
                source_candidates.append(candidate)

            source_sufficient = (
                criticality == "LOW"
                and any(
                    self._low_criticality_candidate_is_sufficient(item)
                    for item in source_candidates
                )
            )
            self._record_timing(
                intent=intent,
                requirement=requirement,
                stage="source.resolve",
                duration_ms=(self._clock() - source_started) * 1000.0,
                candidate_count=len(source_candidates),
                metadata={
                    "source_kind": str(source_candidate.kind),
                    "resolution_status": resolution.status,
                    "decision_criticality": criticality,
                    "low_criticality_sufficient": str(source_sufficient).lower(),
                },
            )
            if source_sufficient and not early_stop_eligible_detected:
                # Q6-C is in shadow/baseline mode: measure when LOW retrieval
                # *could* stop, but do not reduce evidence before a real baseline
                # proves quality is preserved.
                early_stop_eligible_detected = True
                first_sufficient_attempt = source_attempts

        shadow_attempts_after_sufficient = (
            source_attempts - first_sufficient_attempt
            if early_stop_eligible_detected
            else 0
        )
        self._record_timing(
            intent=intent,
            requirement=requirement,
            stage="knowledge.provider.retrieve",
            duration_ms=(self._clock() - provider_started) * 1000.0,
            candidate_count=len(candidates),
            metadata={
                "source_attempts": str(source_attempts),
                "early_stop_applied": str(early_stop_applied).lower(),
                "early_stop_eligible_detected": str(
                    early_stop_eligible_detected
                ).lower(),
                "shadow_attempts_after_sufficient": str(
                    shadow_attempts_after_sufficient
                ),
                "early_stop_mode": "SHADOW_BASELINE",
                "decision_criticality": criticality,
            },
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
