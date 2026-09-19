"""Bridge an established AI entry session into the canonical ELO read context.

The bridge does not create a new runtime or authorization authority. It converts
an already accepted ELOAIEntrySession into the existing ELORequestContext and
ELOKnowledgeProvider so the connected AI can continue through the canonical
agentic retrieval path.
"""

from __future__ import annotations

from dataclasses import dataclass

from .elo_provider import ELOKnowledgeProvider, ELORequestContext
from .entry_contract import (
    ELOAIEntryError,
    ELOAIEntrySession,
    ELOAIEntryState,
)
from .runtime_context import ELORuntimeContext


@dataclass(frozen=True)
class ELOAIEntryRuntimeBinding:
    """Canonical read/runtime binding produced after entry validation."""

    session: ELOAIEntrySession
    request_context: ELORequestContext
    knowledge_provider: ELOKnowledgeProvider


def bind_to_elo_runtime(
    session: ELOAIEntrySession,
    *,
    conversation_id: str,
    runtime_context: ELORuntimeContext | None = None,
) -> ELOAIEntryRuntimeBinding:
    """Bind an accepted entry session to existing ELO agentic runtime services.

    Authorization remains owned by the canonical authorization system. This
    function only establishes the identity/correlation context required by the
    existing read provider. It never grants write access.
    """

    if session.state is not ELOAIEntryState.READY:
        raise ELOAIEntryError("blocked entry session cannot bind to ELO runtime")

    if not conversation_id.strip():
        raise ELOAIEntryError("conversation_id is required")

    if not (
        session.tenant_id
        and session.principal_id
        and session.request_id
        and session.correlation_id
        and session.authorization_scope
    ):
        raise ELOAIEntryError(
            "runtime binding requires tenant, principal, request, "
            "correlation and authorization scope"
        )

    request_context = ELORequestContext(
        tenant_id=session.tenant_id,
        principal_id=session.principal_id,
        session_id=session.session_id,
        request_id=session.request_id,
        correlation_id=session.correlation_id,
        conversation_id=conversation_id,
        authorization_scope=session.authorization_scope,
    )

    provider = ELOKnowledgeProvider(
        request_context=request_context,
        runtime_context=runtime_context,
        allow_temporal_trace=False,
    )

    return ELOAIEntryRuntimeBinding(
        session=session,
        request_context=request_context,
        knowledge_provider=provider,
    )
