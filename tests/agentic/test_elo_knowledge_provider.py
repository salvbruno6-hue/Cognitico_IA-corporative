from __future__ import annotations

from dataclasses import dataclass

from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.elo_provider import ELOKnowledgeProvider, ELORequestContext
from elo.agentic.runtime_context import ELORuntimeContext
from elo.core.context_resolution import ContextPack
from elo.core.source_discovery import CANONICAL_CAPABILITIES, DiscoveryPlan, SourceCandidate
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest, SourceResolver
from elo.observability.cognitive_timing import InMemoryCognitiveTimingSink
from elo.core.temporal_memory import TemporalConversationMemory


@dataclass(frozen=True)
class _Retrieved:
    source_id: str = "source-1"
    source_type: str = "ELO_MEMORY"
    content: str = "current governed result"
    provenance: dict[str, str] | None = None
    metadata: dict[str, str] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "provenance", self.provenance or {"origin": "test"})
        object.__setattr__(self, "metadata", self.metadata or {})


class _Adapter:
    kind = "ELO_MEMORY"
    capability = "source.elo_memory.read"

    def available(self) -> bool:
        return True

    def retrieve(self, candidate, request: SourceResolutionRequest):
        return (_Retrieved(metadata={"cod_produt": "3300900009"}),)


def _provider(*, allow_temporal_trace: bool = False):
    context = ELORequestContext(
        tenant_id="tenant",
        principal_id="principal",
        session_id="session",
        request_id="request",
        correlation_id="correlation",
        conversation_id="conversation",
        authorization_scope="scope.read",
    )
    memory = TemporalConversationMemory()
    resolver = SourceResolver(adapters=(_Adapter(),), temporal_memory=memory)
    provider = ELOKnowledgeProvider(
        request_context=context,
        source_resolver=resolver,
        allow_temporal_trace=allow_temporal_trace,
        runtime_context=ELORuntimeContext(
            project_ref="fxbpevjrkwhbicpmecow",
            supabase_url="https://fxbpevjrkwhbicpmecow.supabase.co",
        ),
    )
    return provider, memory


def _inputs():
    return (
        IntentSpec(
            question="preciso fechar a elétrica externa",
            intent="close_budget",
            domain="orçamento",
            task="fechamento",
            entity="SO 157.26",
            active_context="SO 157.26",
        ),
        KnowledgeRequirement("materials", "materials required by task"),
    )


def test_provider_preserves_context_provenance_and_product_code() -> None:
    provider, _ = _provider()
    intent, req = _inputs()

    found = provider.retrieve(intent, req)

    assert len(found) == 1
    assert found[0].source_id == "source-1"
    assert found[0].content == "current governed result"
    assert found[0].provenance["origin"] == "test"
    assert found[0].metadata["agentic_requirement"] == "materials"
    assert found[0].product_code == "3300900009"


def test_provider_binds_resolved_forge_context_to_read_request() -> None:
    provider, _ = _provider()
    intent, req = _inputs()
    found = provider.retrieve(intent, req)

    assert provider.runtime_context.project_ref == "fxbpevjrkwhbicpmecow"
    assert provider.runtime_context.read_only is True
    assert found


def test_provider_fails_closed_without_request_context() -> None:
    provider = ELOKnowledgeProvider()
    intent = IntentSpec(question="what do I need?", intent="general", domain="orçamento")
    req = KnowledgeRequirement("requirements", "requirements")

    assert provider.retrieve(intent, req) == ()


def test_provider_does_not_write_temporal_memory_by_default() -> None:
    provider, memory = _provider()
    intent, req = _inputs()

    assert provider.retrieve(intent, req)
    assert memory.list("conversation") == ()


def test_provider_can_explicitly_enable_temporal_trace() -> None:
    provider, memory = _provider(allow_temporal_trace=True)
    intent, req = _inputs()

    assert provider.retrieve(intent, req)
    assert len(memory.list("conversation")) == 1


def test_provider_emits_runtime_evidence_only_after_real_context_plugin_adaptation(monkeypatch) -> None:
    from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal
    from elo.agent_intake.runtime_operational_evidence import InMemoryRuntimeEvidenceSink

    monkeypatch.setenv("ELO_RUNTIME_COMMIT", "runtime-test-commit")
    context = ELORequestContext(
        tenant_id="tenant", principal_id="principal", session_id="session",
        request_id="request-runtime", correlation_id="trace-runtime",
        conversation_id="conversation", authorization_scope="scope.read",
    )
    resolver = SourceResolver(adapters=(_Adapter(),), temporal_memory=TemporalConversationMemory())
    signal = ContextEnginePluginSignal(
        signal_id="signal-runtime", tenant_scope="tenant", plugin_id="plugin-runtime",
        engine_name="ELO Context", source_refs=("runtime:plugin-runtime",),
        explicit_activation=True, provenance_verified=True,
    )
    sink = InMemoryRuntimeEvidenceSink()
    provider = ELOKnowledgeProvider(
        request_context=context, source_resolver=resolver,
        context_plugin_signal=signal, runtime_evidence_sink=sink,
    )
    intent, req = _inputs()
    assert provider.retrieve(intent, req)
    assert len(sink.list()) == 1
    item = sink.list()[0]
    assert item.candidate_id == "EXT-CONTEXT-PLUGIN-HERMES"
    assert item.action_observed is True
    assert item.provenance.commit == "runtime-test-commit"


def test_provider_does_not_claim_operational_evidence_from_single_runtime_invocation() -> None:
    from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal

    context = ELORequestContext(
        tenant_id="tenant",
        principal_id="principal",
        session_id="session",
        request_id="request-runtime",
        correlation_id="trace-runtime",
        conversation_id="conversation",
        authorization_scope="scope.read",
    )
    resolver = SourceResolver(adapters=(_Adapter(),), temporal_memory=TemporalConversationMemory())
    signal = ContextEnginePluginSignal(
        signal_id="signal-runtime",
        tenant_scope="tenant",
        plugin_id="plugin-runtime",
        engine_name="ELO Context",
        source_refs=("runtime:plugin-runtime",),
        explicit_activation=True,
        provenance_verified=True,
    )
    provider = ELOKnowledgeProvider(
        request_context=context,
        source_resolver=resolver,
        context_plugin_signal=signal,
    )

    intent, req = _inputs()
    found = provider.retrieve(intent, req)

    assert found
    # Operational evidence requires repeatability across at least two real
    # executions; one provider invocation must not manufacture that outcome.
    assert provider.runtime_evidence_sink is None

def test_memory_provider_runtime_evidence_requires_real_retrieval_and_repeats() -> None:
    from elo.agent_intake.hermes_memory_provider_boundary import MemoryProviderSignal
    from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector

    signal = MemoryProviderSignal(
        provider_id="ELO_MEMORY",
        tenant_scope="tenant",
        source_refs=("source-1",),
        operation="retrieve",
        evidence_digest="sha256:runtime-memory",
        provenance_verified=True,
        explicit_activation=True,
    )
    collector = RuntimeOperationalEvidenceCollector()
    intent, req = _inputs()
    provider = ELOKnowledgeProvider(
        request_context=ELORequestContext(
            tenant_id="tenant",
            principal_id="principal",
            session_id="session",
            request_id="request-memory-runtime",
            correlation_id="trace-memory-runtime",
            conversation_id="conversation",
            authorization_scope="scope.read",
        ),
        source_resolver=SourceResolver(
            adapters=(_Adapter(),),
            temporal_memory=TemporalConversationMemory(),
        ),
        hermes_memory_provider_signal=signal,
        runtime_context=ELORuntimeContext(
            project_ref="fxbpevjrkwhbicpmecow",
            supabase_url="https://fxbpevjrkwhbicpmecow.supabase.co",
            runtime_commit="runtime-memory-commit",
        ),
        runtime_evidence_sink=collector,
    )

    assert provider.retrieve(intent, req)
    assert provider.retrieve(intent, req)

    groups = collector.ready_groups()
    assert len(groups) == 1
    group = groups[0]
    assert group.candidate_id == "EXT-MEMPROVIDER-HERMES"
    assert group.repeatable is True
    outcome = group.to_operational_outcome()
    assert outcome.candidate_id == "EXT-MEMPROVIDER-HERMES"
    assert outcome.production_proven is False
    assert outcome.repeatable is True



class _SignalAdapter:
    kind = "ELO_MEMORY"
    capability = "source.elo_memory.read"

    def __init__(self, retrieved):
        self.retrieved = retrieved

    def available(self) -> bool:
        return True

    def retrieve(self, candidate, request: SourceResolutionRequest):
        return (self.retrieved,)


def _signal_provider(retrieved):
    context = ELORequestContext(
        tenant_id="tenant",
        principal_id="principal",
        session_id="session",
        request_id="request-signals",
        correlation_id="correlation-signals",
        conversation_id="conversation",
        authorization_scope="scope.read",
    )
    return ELOKnowledgeProvider(
        request_context=context,
        source_resolver=SourceResolver(
            adapters=(_SignalAdapter(retrieved),),
            temporal_memory=TemporalConversationMemory(),
        ),
    )


def test_provider_preserves_explicit_quality_signals_without_inference() -> None:
    retrieved = _Retrieved(
        metadata={
            "knowledge_status": "GOVERNED",
            "relevance": "0.85",
            "confidence": "0.72",
            "context_match": "0.90",
        },
        provenance={"origin": "test", "authority": "external_source_evidence"},
    )
    provider = _signal_provider(retrieved)
    intent, req = _inputs()

    item = provider.retrieve(intent, req)[0]

    assert item.status == "REFERENCE"
    assert item.relevance == 0.85
    assert item.confidence == 0.72
    assert item.context_match == 0.90
    assert item.authority == "external_source_evidence"
    assert item.provenance["origin"] == "test"


def test_provider_keeps_neutral_scores_when_signals_are_absent() -> None:
    provider = _signal_provider(_Retrieved(provenance={"origin": "test"}))
    intent, req = _inputs()

    item = provider.retrieve(intent, req)[0]

    assert item.status == "REFERENCE"
    assert item.relevance == 0.0
    assert item.confidence == 0.0
    assert item.context_match == 0.0
    assert item.authority is None


def test_provider_does_not_promote_domain_status_or_invalid_scores() -> None:
    retrieved = _Retrieved(
        metadata={
            "status": "VALIDADO",
            "relevance": "1.2",
            "confidence": "not-a-number",
            "context_match": "-0.1",
            "authority": "",
        },
        provenance={
            "knowledge_status": "CANONICAL",
            "relevance": "0.99",
            "confidence": "0.99",
            "context_match": "0.99",
            "authority": "fallback-authority",
        },
    )
    provider = _signal_provider(retrieved)
    intent, req = _inputs()

    item = provider.retrieve(intent, req)[0]

    # Explicit metadata wins; invalid/foreign signals do not fall through to
    # stronger provenance values and are never promoted implicitly.
    assert item.status == "REFERENCE"
    assert item.relevance == 0.0
    assert item.confidence == 0.0
    assert item.context_match == 0.0
    assert item.authority is None


def test_provider_uses_provenance_signals_when_metadata_does_not_supply_them() -> None:
    retrieved = _Retrieved(
        metadata={"cod_produt": "3300900009"},
        provenance={
            "origin": "test",
            "knowledge_status": "CURRENT",
            "relevance": "0.7",
            "confidence": "0.6",
            "context_match": "0.5",
            "authority": "governed-source",
        },
    )
    provider = _signal_provider(retrieved)
    intent, req = _inputs()

    item = provider.retrieve(intent, req)[0]

    assert item.status == "REFERENCE"
    assert item.relevance == 0.7
    assert item.confidence == 0.6
    assert item.context_match == 0.5
    assert item.authority == "governed-source"
    assert item.product_code == "3300900009"
    assert item.metadata["agentic_requirement"] == "materials"



class _StaticContextEngine:
    def __init__(self, candidates):
        self.candidates = tuple(candidates)

    def resolve(self, query):
        return ContextPack(
            query=query,
            discovery_plan=DiscoveryPlan(
                intent="test",
                entities=(),
                questions=(query.question,),
                candidates=self.candidates,
            ),
        )

    @staticmethod
    def candidate_sources(pack):
        return pack.discovery_plan.candidates


class _CountingSourceAdapter:
    def __init__(self, *, kind, retrieved):
        self.kind = kind
        self.capability = CANONICAL_CAPABILITIES[kind]
        self.retrieved = retrieved
        self.calls = 0

    def available(self):
        return True

    def retrieve(self, candidate, request):
        self.calls += 1
        return (self.retrieved,)


def _multi_source_provider(*, first, second, timing_sink=None):
    first_adapter = _CountingSourceAdapter(kind="ELO_MEMORY", retrieved=first)
    second_adapter = _CountingSourceAdapter(kind="GITHUB", retrieved=second)
    context = ELORequestContext(
        tenant_id="tenant",
        principal_id="principal",
        session_id="session",
        request_id="request-multi",
        correlation_id="correlation-multi",
        conversation_id="conversation",
        authorization_scope="scope.read",
    )
    candidates = (
        SourceCandidate(
            kind="ELO_MEMORY",
            reason="preferred",
            priority=5,
            query="q",
            required_capability=CANONICAL_CAPABILITIES["ELO_MEMORY"],
        ),
        SourceCandidate(
            kind="GITHUB",
            reason="confirmation",
            priority=4,
            query="q",
            required_capability=CANONICAL_CAPABILITIES["GITHUB"],
        ),
    )
    provider = ELOKnowledgeProvider(
        request_context=context,
        context_engine=_StaticContextEngine(candidates),
        source_resolver=SourceResolver(
            adapters=(first_adapter, second_adapter),
            temporal_memory=TemporalConversationMemory(),
        ),
        timing_sink=timing_sink,
    )
    return provider, first_adapter, second_adapter


def _retrieved_quality(source_id, *, status="CURRENT", relevance="0.8",
                       confidence="0.8", context_match="0.8",
                       authority="governed-source"):
    return RetrievedSource(
        source_id=source_id,
        source_type="TEST",
        content=f"evidence:{source_id}",
        metadata={
            "knowledge_status": status,
            "relevance": relevance,
            "confidence": confidence,
            "context_match": context_match,
            "authority": authority,
        },
        provenance={"origin": source_id, "authority": authority},
    )


def test_low_criticality_shadow_mode_does_not_treat_generic_reference_as_sufficient():
    sink = InMemoryCognitiveTimingSink()
    provider, first, second = _multi_source_provider(
        first=_retrieved_quality("first"),
        second=_retrieved_quality("second"),
        timing_sink=sink,
    )
    intent, req = _inputs()
    intent = IntentSpec(
        question=intent.question,
        intent=intent.intent,
        domain=intent.domain,
        task=intent.task,
        entity=intent.entity,
        active_context=intent.active_context,
        metadata={"decision_criticality": "LOW", "correlation_id": "corr-low"},
    )

    found = provider.retrieve(intent, req)

    assert [item.source_id for item in found] == ["first", "second"]
    assert first.calls == 1
    assert second.calls == 1
    total = [x for x in sink.observations if x.stage == "knowledge.provider.retrieve"][-1]
    assert total.metadata["source_attempts"] == "2"
    assert total.metadata["early_stop_applied"] == "false"
    assert total.metadata["early_stop_eligible_detected"] == "false"
    assert total.metadata["shadow_attempts_after_sufficient"] == "0"
    assert total.metadata["early_stop_mode"] == "SHADOW_BASELINE"
    assert total.metadata["decision_criticality"] == "LOW"
    assert all(item.status == "REFERENCE" for item in found)


def test_low_criticality_continues_when_first_source_is_not_sufficient():
    provider, first, second = _multi_source_provider(
        first=_retrieved_quality(
            "first",
            status="REFERENCE",
            relevance="0.9",
            confidence="0.9",
            context_match="0.9",
        ),
        second=_retrieved_quality("second"),
    )
    intent, req = _inputs()
    intent = IntentSpec(
        question=intent.question,
        intent=intent.intent,
        domain=intent.domain,
        metadata={"decision_criticality": "LOW"},
    )

    found = provider.retrieve(intent, req)

    assert [item.source_id for item in found] == ["first", "second"]
    assert first.calls == 1
    assert second.calls == 1


def test_low_criticality_does_not_stop_without_explicit_authority():
    first_item = _retrieved_quality("first", authority="")
    provider, first, second = _multi_source_provider(
        first=first_item,
        second=_retrieved_quality("second"),
    )
    intent, req = _inputs()
    intent = IntentSpec(
        question=intent.question,
        intent=intent.intent,
        domain=intent.domain,
        metadata={"decision_criticality": "LOW"},
    )

    provider.retrieve(intent, req)

    assert first.calls == 1
    assert second.calls == 1


def test_non_low_criticality_never_early_stops_in_this_cycle():
    for criticality in ("MEDIUM", "HIGH", "CRITICAL", ""):
        provider, first, second = _multi_source_provider(
            first=_retrieved_quality(f"first-{criticality or 'unknown'}"),
            second=_retrieved_quality(f"second-{criticality or 'unknown'}"),
        )
        intent, req = _inputs()
        metadata = {"decision_criticality": criticality} if criticality else {}
        scoped_intent = IntentSpec(
            question=intent.question,
            intent=intent.intent,
            domain=intent.domain,
            metadata=metadata,
        )

        found = provider.retrieve(scoped_intent, req)

        assert len(found) == 2
        assert first.calls == 1
        assert second.calls == 1


def test_low_criticality_minimum_signal_is_exactly_sixty_percent():
    provider, first, second = _multi_source_provider(
        first=_retrieved_quality(
            "first",
            relevance="0.60",
            confidence="0.60",
            context_match="0.60",
        ),
        second=_retrieved_quality("second"),
    )
    intent, req = _inputs()
    intent = IntentSpec(
        question=intent.question,
        intent=intent.intent,
        domain=intent.domain,
        metadata={"decision_criticality": "LOW"},
    )

    found = provider.retrieve(intent, req)

    assert [item.source_id for item in found] == ["first", "second"]
    assert first.calls == 1
    assert second.calls == 1



def test_generic_provider_never_accepts_source_claimed_canonical_status() -> None:
    retrieved = _Retrieved(
        metadata={
            "knowledge_status": "CANONICAL",
            "relevance": "1.0",
            "confidence": "1.0",
            "context_match": "1.0",
        },
        provenance={
            "origin": "untrusted-source",
            "authority": "external_source_evidence",
        },
    )
    provider = _signal_provider(retrieved)
    intent, req = _inputs()

    item = provider.retrieve(intent, req)[0]

    assert item.status == "REFERENCE"
    assert item.authority == "external_source_evidence"
