from __future__ import annotations

from dataclasses import dataclass

from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.elo_provider import ELOKnowledgeProvider, ELORequestContext
from elo.core.source_resolver import SourceResolutionRequest, SourceResolver
from elo.core.temporal_memory import TemporalConversationMemory


@dataclass(frozen=True)
class _Retrieved:
    source_id: str = "source-1"
    source_type: str = "ELO_MEMORY"
    content: str = "current governed result"
    provenance: dict[str, str] = None  # type: ignore[assignment]
    metadata: dict[str, str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        object.__setattr__(self, "provenance", self.provenance or {"origin": "test"})
        object.__setattr__(self, "metadata", self.metadata or {})


class _Adapter:
    kind = "ELO_MEMORY"
    capability = "source.elo_memory.read"

    def available(self) -> bool:
        return True

    def retrieve(self, candidate, request: SourceResolutionRequest):
        return (_Retrieved(),)


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


def test_provider_preserves_context_and_provenance() -> None:
    provider, _ = _provider()
    intent, req = _inputs()

    found = provider.retrieve(intent, req)

    assert len(found) == 1
    assert found[0].source_id == "source-1"
    assert found[0].content == "current governed result"
    assert found[0].provenance["origin"] == "test"
    assert found[0].metadata["agentic_requirement"] == "materials"


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
