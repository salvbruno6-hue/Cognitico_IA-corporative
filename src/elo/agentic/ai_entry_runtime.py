"""Bridge a connected AI entry session into the existing ELO agentic context.

The bridge composes existing entry validation and ELORequestContext. It does
not authenticate GitHub, authorize operations, resolve canonical context, or
execute tools; those remain owned by their existing authorities.
"""

from __future__ import annotations

from dataclasses import dataclass

from .elo_provider import ELORequestContext
from .entry_contract import (
    ELOAIEntryError,
    ELOAIEntryGate,
    ELOAIEntryRequest,
    ELOAIEntrySession,
    ELOAIEntryState,
)


class ELOAICognitiveHandoffError(ELOAIEntryError):
    """Raised when an admitted AI session cannot be handed to ELO Cognitive."""


@dataclass(frozen=True)
class ELOAICognitiveHandoff:
    entry_session: ELOAIEntrySession
    request_context: ELORequestContext


class ELOAIEntryRuntime:
    """Compose AI entry validation with the existing ELO agentic context."""

    def __init__(self, *, entry_gate: ELOAIEntryGate | None = None) -> None:
        self.entry_gate = entry_gate or ELOAIEntryGate()

    def establish_and_bind(
        self,
        request: ELOAIEntryRequest,
        *,
        readable_artifacts: tuple[str, ...],
        access_scope_valid: bool = True,
        contract_conflict: bool = False,
        conversation_id: str | None = None,
    ) -> ELOAICognitiveHandoff:
        session = self.entry_gate.establish(
            request,
            readable_artifacts=readable_artifacts,
            access_scope_valid=access_scope_valid,
            contract_conflict=contract_conflict,
        )
        if session.state is not ELOAIEntryState.READY:
            raise ELOAICognitiveHandoffError(
                f"AI entry blocked: {session.block or 'BLOCKED'}"
            )

        context = self._request_context(request, conversation_id=conversation_id)
        return ELOAICognitiveHandoff(
            entry_session=session,
            request_context=context,
        )

    @staticmethod
    def _request_context(
        request: ELOAIEntryRequest,
        *,
        conversation_id: str | None,
    ) -> ELORequestContext:
        required = {
            "tenant_id": request.tenant_id,
            "principal_id": request.principal_id,
            "request_id": request.request_id,
            "correlation_id": request.correlation_id,
            "authorization_scope": request.authorization_scope,
            "conversation_id": conversation_id,
        }
        missing = tuple(name for name, value in required.items() if not value)
        if missing:
            raise ELOAICognitiveHandoffError(
                "ELO Cognitive handoff requires resolved context: "
                + ", ".join(missing)
            )

        return ELORequestContext(
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            session_id=request.session_id,
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            conversation_id=conversation_id,
            authorization_scope=request.authorization_scope,
        )
