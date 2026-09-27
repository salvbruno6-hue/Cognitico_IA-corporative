from __future__ import annotations

from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal
from elo.agent_intake.runtime_operational_evidence_collector import (
    RuntimeEvidenceKey,
    RuntimeOperationalEvidenceCollector,
)
from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.elo_provider import ELOKnowledgeProvider, ELORequestContext
from elo.agentic.runtime_context import ELORuntimeContext
from elo.core.source_resolver import SourceResolutionRequest, SourceResolver
from elo.core.temporal_memory import TemporalConversationMemory


class _Retrieved:
    source_id = "source-1"
    source_type = "ELO_MEMORY"
    content = "runtime governed result"
    provenance = {"origin": "test"}
    metadata = {"cod_produt": "3300900009"}


class _Adapter:
    kind = "ELO_MEMORY"
    capability = "source.elo_memory.read"

    def available(self) -> bool:
        return True

    def retrieve(self, candidate, request: SourceResolutionRequest):
        return (_Retrieved(),)


def test_context_plugin_repeated_real_provider_invocations_produce_operational_outcome(monkeypatch):
    monkeypatch.setenv("ELO_RUNTIME_COMMIT", "runtime-repeatability-context-plugin-test")

    request_context = ELORequestContext(
        tenant_id="tenant",
        principal_id="principal",
        session_id="session",
        request_id="request-runtime",
        correlation_id="trace-runtime",
        conversation_id="conversation",
        authorization_scope="scope.read",
    )
    signal = ContextEnginePluginSignal(
        signal_id="signal-runtime",
        tenant_scope="tenant",
        plugin_id="plugin-runtime",
        engine_name="ELO Context",
        source_refs=("runtime:plugin-runtime",),
        explicit_activation=True,
        provenance_verified=True,
    )
    intent = IntentSpec(
        question="preciso fechar a elétrica externa",
        intent="close_budget",
        domain="orçamento",
        task="fechamento",
        entity="SO 157.26",
        active_context="SO 157.26",
    )
    requirement = KnowledgeRequirement("materials", "materials required by task")
    collector = RuntimeOperationalEvidenceCollector()

    for _ in range(2):
        resolver = SourceResolver(
            adapters=(_Adapter(),),
            temporal_memory=TemporalConversationMemory(),
        )
        emitted = []
        provider = ELOKnowledgeProvider(
            request_context=request_context,
            source_resolver=resolver,
            runtime_context=ELORuntimeContext(
                project_ref="fxbpevjrkwhbicpmecow",
                supabase_url="https://fxbpevjrkwhbicpmecow.supabase.co",
            ),
            context_plugin_signal=signal,
            runtime_evidence_sink=emitted,
        )

        found = provider.retrieve(intent, requirement)

        assert found
        assert len(emitted) == 1
        collector.append(emitted[0])

    key = RuntimeEvidenceKey(
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="ELO Context",
        runtime_entrypoint="elo.context.resolve",
        metric="context_plugin_activation_success_rate",
        direction="maximize",
    )

    outcome = collector.outcome(key)

    assert outcome.level == "OPERATIONAL_OUTCOME"
    assert outcome.repeatable is True
    assert outcome.production_proven is True
    assert len(outcome.provenance_refs) == 2
