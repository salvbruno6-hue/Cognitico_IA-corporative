"""Rich intelligent response composition for the governed orchestrator.

This module is presentation/composition only. It does not authorize, route,
execute, learn, promote, or create a new cognitive authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.cognitive.runtime.humanization.humanizer import Humanizer


@dataclass(frozen=True)
class IntelligentOrchestrationResponse:
    """Human-facing response plus bounded machine-readable execution context."""

    status: str
    stage: str
    headline: str
    response: str
    capability: str | None
    provider: str | None
    model: str | None
    execution_id: str | None
    correlation_id: str
    evidence_state: str
    next_action: str


class OrchestrationResponseComposer:
    """Compose a useful response from already-produced orchestration facts."""

    def __init__(self, humanizer: Humanizer | None = None) -> None:
        self._humanizer = humanizer or Humanizer()

    def compose(
        self,
        *,
        request: Any,
        selection: Any,
        outcome: Any,
    ) -> IntelligentOrchestrationResponse:
        capability = getattr(selection, "capability_name", None)
        correlation_id = getattr(request, "correlation_id", "")
        if outcome is None:
            response = self._humanizer.humanize(
                {
                    "error": "execução não autorizada ou não concluída",
                    "suggestions": ["verificar autorização, evidências e rota selecionada"],
                }
            )
            return IntelligentOrchestrationResponse(
                status="NOT_EXECUTED",
                stage="HANDOFF",
                headline="A execução não foi realizada.",
                response=response,
                capability=capability,
                provider=None,
                model=None,
                execution_id=None,
                correlation_id=correlation_id,
                evidence_state="INSUFFICIENT",
                next_action="verificar os controles pendentes antes de executar.",
            )

        provider = getattr(outcome, "provider", None)
        model = getattr(outcome, "model", None)
        execution_id = getattr(outcome, "execution_id", None) or getattr(
            outcome, "request_id", None
        )
        executed = bool(getattr(outcome, "executed", False))
        status = "EXECUTED" if executed else "NOT_EXECUTED"
        evidence_state = "OBSERVED" if executed else "INSUFFICIENT"
        headline = (
            "A capacidade foi executada pelo fluxo governado."
            if executed
            else "A capacidade não concluiu a execução."
        )
        response = self._humanizer.humanize(
            {
                "error": None if executed else "execução não concluída",
                "suggestions": [] if executed else ["revisar os controles de execução"],
            }
        ) if not executed else (
            f"{headline}\n\n"
            "**O que funcionou:**\n"
            f"- A capacidade solicitada foi processada pelo fluxo governado.\n"
            f"- A execução foi associada à correlação da solicitação.\n\n"
            "**O que ainda pode evoluir:**\n"
            "- O resultado observado ainda deve ser avaliado conforme "
            "as evidências disponíveis.\n\n"
            "**Próximo passo:** avaliar o resultado e a evidência antes "
            "de qualquer conclusão de aprendizado ou evolução."
        )
        return IntelligentOrchestrationResponse(
            status=status,
            stage="EXECUTE" if executed else "HANDOFF",
            headline=headline,
            response=response,
            capability=capability,
            provider=provider,
            model=model,
            execution_id=execution_id,
            correlation_id=correlation_id,
            evidence_state=evidence_state,
            next_action=(
                "avaliar o resultado e a evidência antes de qualquer conclusão "
                "de aprendizado ou evolução."
                if executed
                else "verificar os controles pendentes antes de executar."
            ),
        )


__all__ = ["IntelligentOrchestrationResponse", "OrchestrationResponseComposer"]
