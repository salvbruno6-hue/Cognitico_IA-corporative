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
    evidence_refs: tuple[str, ...] = ()


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
        """Compose a read-only Forge consultation through canonical orientation."""
        response = self._humanizer.humanize({
            "intent": "forge_consulta",
            "forge_context": forge_context,
        })
        response = self._append_indicator_context(response, forge_context)
        entity = forge_context.get("entity") or {}
        model = forge_context.get("model") or {}
        orientation = None
        try:
            from elo.cognitive.response.orchestration_orientation_hook import derive_orientation

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
            orientation = derive_orientation(
                capability="forge_operational_knowledge",
                context=forge_context,
                execution_outcome=None,
                source_facts=source_facts,
                routing_decision=None,
                capability_snapshot=None,
            )
            if orientation is not None:
                response = self._append_orientation(response, orientation)
        except Exception:
            orientation = None

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
            orientation=orientation,
            evidence_refs=tuple(evidence_ids),
        )

    @staticmethod
    def _append_indicator_context(response: str, forge_context: dict[str, Any]) -> str:
        indicator = forge_context.get("indicator_context") or {}
        if not indicator:
            return response

        discovery = forge_context.get("governed_discovery") or {}
        linked = discovery.get("linked_records") or {}
        capacity_rows = linked.get("v_elo_pcp_carga_capacidade_periodo") or []
        external_rows = linked.get("v_elo_pcp_indicadores_montagem_externa") or []
        kpi_definitions = linked.get("mt_definicoes_kpi") or []

        lines = [
            "",
            "**Indicadores governados — rastreabilidade operacional**",
        ]

        if capacity_rows:
            lines.append("- Fonte `v_elo_pcp_carga_capacidade_periodo`:")
            for row in capacity_rows[:10]:
                center = row.get("centro_trabalho_codigo") or row.get("centro_trabalho_nome") or "centro não informado"
                date = row.get("data_referencia") or "data não informada"
                lines.append(
                    "  - "
                    f"{date} / {center}: carga_h={row.get('carga_horas_planejada', 'não informada')}; "
                    f"capacidade_disponível={row.get('capacidade_disponivel', 'não informada')}; "
                    f"folga_h={row.get('folga_horas', 'não informada')}; "
                    f"utilização={row.get('utilizacao_pct', 'não informada')}%; "
                    f"excesso_carga={row.get('excesso_carga', 'não informado')}."
                )
        else:
            lines.append(
                "- `v_elo_pcp_carga_capacidade_periodo`: nenhuma linha operacional recuperada; "
                "não há evidência para declarar utilização ou folga de capacidade."
            )

        if external_rows:
            row = external_rows[0]
            lines.append(
                "- Fonte `v_elo_pcp_indicadores_montagem_externa`: "
                f"ordens={row.get('ordens_total', 'não informado')}; "
                f"abertas={row.get('ordens_abertas', 'não informado')}; "
                f"atrasadas={row.get('ordens_atrasadas', 'não informado')}; "
                f"módulos={row.get('modulos_total', 'não informado')}; "
                f"colaboradores={row.get('colaboradores_alocados', 'não informado')}; "
                f"horas_planejadas={row.get('horas_planejadas_ordens', 'não informado')}; "
                f"horas_realizadas={row.get('horas_realizadas_ordens', 'não informado')}; "
                f"aderência={row.get('aderencia_horas_pct', 'não informada')}%."
            )
            activity_fields = (
                "ordens_total",
                "ordens_abertas",
                "ordens_atrasadas",
                "modulos_total",
                "colaboradores_alocados",
                "funcoes_ativas",
                "horas_planejadas_ordens",
                "horas_realizadas_ordens",
                "horas_planejadas_equipe",
                "horas_mao_obra_realizadas",
            )
            has_activity = any(float(row.get(field) or 0) != 0 for field in activity_fields)
            if not has_activity and row.get("aderencia_horas_pct") is None:
                lines.append(
                    "  - Estado: registro estrutural presente, mas sem atividade operacional mensurável; "
                    "isso não equivale a KPI com valor zero."
                )
        else:
            lines.append(
                "- `v_elo_pcp_indicadores_montagem_externa`: nenhuma linha recuperada."
            )

        formal_state = indicator.get("formal_kpi_state")
        if formal_state == "SEM_KPI_FORMAL_REGISTRADO":
            lines.append(
                "- KPI formal: nenhum registro em `mt_definicoes_kpi`; os valores acima permanecem "
                "indicadores e não podem ser promovidos automaticamente a KPI."
            )
        elif formal_state == "KPI_FORMAL_REGISTRADO":
            lines.append(
                f"- KPI formal: {indicator.get('kpi_definition_count', len(kpi_definitions))} definição(ões) "
                "governada(s) localizada(s) em `mt_definicoes_kpi`."
            )
            for row in kpi_definitions[:10]:
                lines.append(
                    f"  - {row.get('codigo_kpi') or 'código não informado'} — "
                    f"{row.get('nome') or 'nome não informado'}; "
                    f"unidade={row.get('unidade', 'não informada')}; "
                    f"fórmula={row.get('formula', 'não informada')}."
                )
        else:
            lines.append(
                "- KPI formal: o registro de definições não está governado nesta consulta; "
                "não é permitido inferir existência de KPI."
            )

        lines.append(
            f"- Autoridade de fontes: `{indicator.get('catalog_authority', 'elo_aprendizado_fontes')}`; "
            "consulta somente leitura; promoção automática a KPI=false."
        )
        return f"{response}\n" + "\n".join(lines)

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
