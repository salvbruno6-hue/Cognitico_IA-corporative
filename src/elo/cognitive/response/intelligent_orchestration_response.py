"""Rich intelligent response composition for the governed orchestrator.

This module is presentation/composition only. It does not authorize, route,
execute, learn, promote, or create a new cognitive authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.cognitive.runtime.humanization.humanizer import Humanizer
from elo.evidence import EvidenceRepository


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
    orientation: Any | None = None


class OrchestrationResponseComposer:
    """Compose a useful response from already-produced orchestration facts."""

    def __init__(
        self,
        humanizer: Humanizer | None = None,
        evidence_repository: EvidenceRepository | None = None,
    ) -> None:
        self._humanizer = humanizer or Humanizer()
        self._evidence_repository = evidence_repository or EvidenceRepository()

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
            orientation = self._derive_orientation(
                request=request,
                selection=selection,
                outcome=outcome,
            )
            if orientation is not None:
                response = self._append_orientation(response, orientation)
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
                orientation=orientation,
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
        orientation = self._derive_orientation(
            request=request,
            selection=selection,
            outcome=outcome,
        )
        if orientation is not None:
            response = self._append_orientation(response, orientation)
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
            orientation=orientation,
        )

    def compose_forge(
        self,
        *,
        request: Any,
        forge_context: dict[str, Any],
        evidence_ids: tuple[str, ...] = (),
    ) -> IntelligentOrchestrationResponse:
        """Compose a read-only Forge consultation through the existing Humanizer."""
        response = self._humanizer.humanize({
            "intent": "forge_consulta",
            "forge_context": forge_context,
        })
        entity = forge_context.get("entity") or {}
        model = forge_context.get("model") or {}
        return IntelligentOrchestrationResponse(
            status="CONSULTED",
            stage="ANALYZE",
            headline=(
                f"Consulta governada do Forge para {model.get('codigo') or entity.get('requested_reference')}."
                if model or entity
                else "Consulta governada do Forge sobre demanda e impactos."
            ),
            response=response,
            capability="forge_operational_knowledge",
            provider="supabase_elo_forge",
            model=model.get("codigo"),
            execution_id=None,
            correlation_id=getattr(request, "correlation_id", ""),
            evidence_state="OBSERVED" if evidence_ids else "INSUFFICIENT",
            next_action="avaliar lacunas ou fornecer uma chave segura para aprofundar as fontes não vinculadas.",
            orientation=None,
        )

    @staticmethod
    def _append_orientation(response: str, orientation: Any) -> str:
        diagnosis = getattr(orientation, "diagnosis", "")
        next_step = getattr(orientation, "next_step", "")
        if not diagnosis and not next_step:
            return response
        return (
            f"{response}\n\n"
            "**Orientação observada:**\n"
            f"- {diagnosis}\n\n"
            "**Próximo passo orientado:**\n"
            f"- {next_step}"
        )

    def _derive_orientation(self, *, request: Any, selection: Any, outcome: Any) -> Any | None:
        """Invoke the optional read-only orientation hook without affecting composition."""
        try:
            from elo.cognitive.response.orchestration_orientation_hook import (
                derive_orientation,
            )

            evidence_ids = tuple(getattr(outcome, "evidence_ids", ()) or ())
            tenant_id = getattr(request, "tenant_id", "")
            source_facts = (
                tuple(
                    self._evidence_repository.list_for_refs(
                        evidence_ids,
                        tenant_id=tenant_id,
                    )
                )
                if evidence_ids and tenant_id
                else ()
            )
            return derive_orientation(
                capability=getattr(selection, "capability_name", None),
                context={},
                execution_outcome=outcome,
                source_facts=source_facts,
                routing_decision=None,
                capability_snapshot=None,
            )
        except Exception:
            return None


__all__ = ["IntelligentOrchestrationResponse", "OrchestrationResponseComposer"]
