from __future__ import annotations

from dataclasses import dataclass

from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.elo_provider import ELOKnowledgeProvider, ELORequestContext
from elo.agentic.runtime_context import ELORuntimeContext
from elo.core.source_resolver import SourceResolutionRequest, SourceResolver
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
