"""Handoff from the governed AI entry boundary to the existing ELO agentic runtime.

This adapter composes the entry contract with ELORequestContext and
ELOKnowledgeProvider. It does not authenticate GitHub, grant authorization,
create memory, or execute operations.
"""

from __future__ import annotations

from dataclasses import dataclass

from .elo_provider import ELOKnowledgeProvider, ELORequestContext
from .entry_contract import ELOAIEntryMode, ELOAIEntrySession
from .runtime_context import ELORuntimeContext, resolve_runtime_context


class ELOAIEntryHandoffError(ValueError):
    """Raised when an established entry cannot be handed to ELO Cognitive."""


@dataclass(frozen=True)
class ELOCognitiveSession:
    entry: ELOAIEntrySession
    request_context: ELORequestContext
    runtime_context: ELORuntimeContext

    def knowledge_provider(self) -> ELOKnowledgeProvider:
        """Return the existing read-only ELO knowledge provider."""
        return ELOKnowledgeProvider(
            request_context=self.request_context,
            runtime_context=self.runtime_context,
        )


class ELOAIEntryHandoff:
    """Bind an established AI entry to existing ELO Cognitive read/query context."""

    def __init__(self, *, runtime_context: ELORuntimeContext | None = None) -> None:
        self.runtime_context = runtime_context or resolve_runtime_context()

    def bind(self, entry: ELOAIEntrySession) -> ELOCognitiveSession:
        if entry.state.value != "READY":
            raise ELOAIEntryHandoffError("blocked entry cannot become an ELO Cognitive session")

        if not entry.tenant_id:
            raise ELOAIEntryHandoffError("tenant_id is required for ELO Cognitive handoff")
        if not entry.principal_id:
            raise ELOAIEntryHandoffError("principal_id is required for ELO Cognitive handoff")
        if not entry.request_id:
            raise ELOAIEntryHandoffError("request_id is required for ELO Cognitive handoff")
        if not entry.correlation_id:
            raise ELOAIEntryHandoffError("correlation_id is required for ELO Cognitive handoff")
        if not entry.authorization_scope:
            raise ELOAIEntryHandoffError("authorization_scope is required for ELO Cognitive handoff")

        context = ELORequestContext(
            tenant_id=entry.tenant_id,
            principal_id=entry.principal_id,
            session_id=entry.session_id,
            request_id=entry.request_id,
            correlation_id=entry.correlation_id,
            conversation_id=entry.session_id,
            authorization_scope=entry.authorization_scope,
        )
        return ELOCognitiveSession(
            entry=entry,
            request_context=context,
            runtime_context=self.runtime_context,
        )

    @staticmethod
    def can_query(entry: ELOAIEntrySession) -> bool:
        """Indicate whether the entry carries enough identity to query ELO.

        A read-only connection is allowed to query governed ELO knowledge.
        This is a capability precondition, not an authorization decision.
        """
        return (
            entry.state.value == "READY"
            and bool(
                entry.tenant_id
                and entry.principal_id
                and entry.request_id
                and entry.correlation_id
                and entry.authorization_scope
            )
        )
