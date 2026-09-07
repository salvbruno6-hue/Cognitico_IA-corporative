from __future__ import annotations

from dataclasses import dataclass

from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.elo_provider import ELOKnowledgeProvider, ELORequestContext
from elo.core.source_resolver import SourceResolutionRequest, SourceResolutionResult


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


class _Resolver:
    def __init__(self):
        from elo.core.source_resolver import SourceResolver

        self._inner = SourceResolver(adapters=(_Adapter(),))

    def resolve(self, candidate, request):
        return self._inner.resolve(candidate, request)


def test_provider_preserves_read_only_boundary_and_context() -> None:
    context = ELORequestContext(
        tenant_id="tenant",
        principal_id="principal",
        session_id="session",
        request_id="request",
        correlation_id="correlation",
        conversation_id="conversation",
        authorization_scope="scope.read",
    )
    provider = ELOKnowledgeProvider(request_context=context, source_resolver=_Resolver())
    intent = IntentSpec(
        question="preciso fechar a elétrica externa",
        intent="close_budget",
        domain="orçamento",
        task="fechamento",
        entity="SO 157.26",
        active_context="SO 157.26",
    )
    req = KnowledgeRequirement("materials", "materials required by task")

    found = provider.retrieve(intent, req)

    assert len(found) == 1
    assert found[0].source_id == "source-1"
    assert found[0].content == "current governed result"
    assert found[0].provenance["origin"] == "test"
    assert provider.request_context == context


def test_provider_fails_closed_without_request_context() -> None:
    provider = ELOKnowledgeProvider()
    intent = IntentSpec(question="what do I need?", intent="general", domain="orçamento")
    req = KnowledgeRequirement("requirements", "requirements")

    assert provider.retrieve(intent, req) == ()
