"""Human-facing read models for ELO orchestration.

The orchestrator may explain the ELO system to administrators/developers and
expose governed operational analysis to corporate interfaces, but it does not
own any of the authorities it describes.

This module is deliberately read-only.  It consumes explicit visibility and
Forge context supplied by canonical components and produces presentation-ready
structures, including chart data.  It never authorizes execution, promotes
learning, mutates canonical data, or infers missing operational facts.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping, Sequence

from elo.cognitive.symbiont_capability_governance import (
    CapabilityVisibilityState,
    GlobalCapabilityVisibility,
)


class OrchestrationAudience(StrEnum):
    ELO_ADMIN = "ELO_ADMIN"
    ELO_DEVELOPER = "ELO_DEVELOPER"
    CORPORATE_OPERATOR = "CORPORATE_OPERATOR"
    CORPORATE_INTERFACE = "CORPORATE_INTERFACE"


class OrchestrationView(StrEnum):
    SYSTEMIC = "SYSTEMIC"
    OPERATIONAL = "OPERATIONAL"


@dataclass(frozen=True, slots=True)
class DiagnosticItem:
    code: str
    title: str
    state: str
    explanation: str
    impact: str
    recommendation: str
    evidence_refs: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "title": self.title,
            "state": self.state,
            "explanation": self.explanation,
            "impact": self.impact,
            "recommendation": self.recommendation,
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class ChartDatum:
    label: str
    value: float
    state: str = "OBSERVED"

    def as_dict(self) -> dict[str, object]:
        return {"label": self.label, "value": self.value, "state": self.state}


@dataclass(frozen=True, slots=True)
class ChartSpec:
    chart_id: str
    title: str
    kind: str
    unit: str
    data: tuple[ChartDatum, ...]
    note: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "chart_id": self.chart_id,
            "title": self.title,
            "kind": self.kind,
            "unit": self.unit,
            "data": [item.as_dict() for item in self.data],
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class OrchestrationViewResult:
    audience: OrchestrationAudience
    view: OrchestrationView
    status: str
    summary: str
    diagnostics: tuple[DiagnosticItem, ...] = ()
    operational_sections: Mapping[str, Any] | None = None
    charts: tuple[ChartSpec, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    read_only: bool = True
    canonical_mutation: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "audience": self.audience.value,
            "view": self.view.value,
            "status": self.status,
            "summary": self.summary,
            "diagnostics": [item.as_dict() for item in self.diagnostics],
            "operational_sections": dict(self.operational_sections or {}),
            "charts": [item.as_dict() for item in self.charts],
            "evidence_refs": list(self.evidence_refs),
            "read_only": self.read_only,
            "canonical_mutation": self.canonical_mutation,
        }


_SYSTEMIC_AUDIENCES = {
    OrchestrationAudience.ELO_ADMIN,
    OrchestrationAudience.ELO_DEVELOPER,
}
_OPERATIONAL_AUDIENCES = {
    OrchestrationAudience.ELO_ADMIN,
    OrchestrationAudience.ELO_DEVELOPER,
    OrchestrationAudience.CORPORATE_OPERATOR,
    OrchestrationAudience.CORPORATE_INTERFACE,
}


class OrchestrationViewComposer:
    """Compose bounded humanized ELO views from explicit governed inputs."""

    def systemic_view(
        self,
        *,
        audience: OrchestrationAudience,
        visibility: GlobalCapabilityVisibility,
        skill_statuses: Sequence[Mapping[str, Any]] = (),
        operational_context: Mapping[str, Any] | None = None,
    ) -> OrchestrationViewResult:
        if audience not in _SYSTEMIC_AUDIENCES:
            raise PermissionError("systemic ELO view is restricted to administrator/developer audiences")

        diagnostics: list[DiagnosticItem] = []
        evidence_refs: list[str] = []
        counts: dict[str, int] = {state.value: 0 for state in CapabilityVisibilityState}

        for record in visibility.records:
            counts[record.state.value] = counts.get(record.state.value, 0) + 1
            evidence_refs.extend(record.evidence_refs)
            if record.state is CapabilityVisibilityState.REGISTERED_VISIBLE:
                continue

            recommendation = {
                CapabilityVisibilityState.EXISTING_BUT_UNWIRED: "Conectar a implementação à rota canônica existente e provar o consumo em runtime.",
                CapabilityVisibilityState.IMPLEMENTED_NOT_REGISTERED: "Registrar a capability no CapabilityRegistry antes de permitir seleção canônica.",
                CapabilityVisibilityState.REGISTERED_WITHOUT_IMPLEMENTATION_VIEW: "Produzir a visão de implementação/evidência antes de tratá-la como funcionalmente comprovada.",
                CapabilityVisibilityState.UNRESOLVED_OWNER: "Resolver ownership antes de evolução, delegação ou manutenção operacional.",
            }.get(record.state, "Investigar a capability sem criar nova autoridade.")
            positive = (
                "Quando funcional e conectada, a capability pode ser selecionada, roteada e observada pelo fluxo canônico, "
                "reduzindo pontos cegos de governança e aumentando a capacidade do ELO de responder ou executar com evidência."
            )
            diagnostics.append(
                DiagnosticItem(
                    code=record.capability_id,
                    title=f"Capability {record.capability_id}",
                    state=record.state.value,
                    explanation=(
                        f"registry_visible={record.registry_visible}; implementation_visible={record.implementation_visible}; "
                        f"runtime_status={record.runtime_status or 'NAO_COMPROVADO'}; owner={record.owner or 'NAO_RESOLVIDO'}."
                    ),
                    impact=positive,
                    recommendation=recommendation,
                    evidence_refs=record.evidence_refs,
                )
            )

        for raw in skill_statuses:
            skill_id = str(raw.get("skill_id") or raw.get("id") or raw.get("name") or "skill:unknown")
            state = str(raw.get("state") or raw.get("status") or "INDETERMINADO")
            refs = tuple(str(item) for item in raw.get("evidence_refs", ()) if item)
            evidence_refs.extend(refs)
            if state.upper() in {"FUNCTIONAL", "COMPROVADO", "AVAILABLE", "HEALTHY"}:
                continue
            diagnostics.append(
                DiagnosticItem(
                    code=skill_id,
                    title=f"Skill {skill_id}",
                    state=state,
                    explanation=str(raw.get("reason") or "A skill não possui prova suficiente de funcionamento saudável."),
                    impact=str(raw.get("positive_impact") or "A funcionalidade deve ser comprovada para que o ELO possa usá-la sem criar lacunas no fluxo cognitivo ou operacional."),
                    recommendation=str(raw.get("recommendation") or "Investigar evidência, wiring, runtime e ownership antes de promover ou depender desta skill."),
                    evidence_refs=refs,
                )
            )

        charts = (
            ChartSpec(
                chart_id="capability_visibility",
                title="Visibilidade das capacidades do ELO",
                kind="bar",
                unit="capabilities",
                data=tuple(ChartDatum(label=state, value=float(value)) for state, value in counts.items()),
                note="Contagem por estado de visibilidade; não representa performance sem evidência de runtime.",
            ),
            ChartSpec(
                chart_id="systemic_gaps",
                title="Gaps sistêmicos que exigem orientação",
                kind="bar",
                unit="items",
                data=(
                    ChartDatum("capabilities", float(len(visibility.isolated))),
                    ChartDatum("skills", float(sum(1 for item in skill_statuses if str(item.get('state') or item.get('status') or '').upper() not in {'FUNCTIONAL','COMPROVADO','AVAILABLE','HEALTHY'}))),
                ),
                note="Somente gaps explicitamente fornecidos/observados entram no gráfico.",
            ),
        )

        operational_summary = self._operational_impact_summary(operational_context or {})
        if operational_summary:
            diagnostics.append(
                DiagnosticItem(
                    code="OPERATIONAL_IMPACT",
                    title="Impacto operacional observado",
                    state="OBSERVED",
                    explanation=operational_summary,
                    impact="Mostra ao ADM/desenvolvedor como lacunas ou capacidades do ELO repercutem no processo corporativo sem transferir autoridade do Forge ao Orquestrador.",
                    recommendation="Usar a evidência operacional para priorizar capacidade, skill ou integração; manter a decisão de negócio no domínio operacional correspondente.",
                )
            )

        status = "ATTENTION" if diagnostics else "HEALTHY"
        summary = (
            f"Visão sistêmica do ELO: {visibility.capability_count} capabilities observadas; "
            f"{len(visibility.isolated)} com gap de visibilidade/integração; {len(diagnostics)} orientações produzidas."
        )
        return OrchestrationViewResult(
            audience=audience,
            view=OrchestrationView.SYSTEMIC,
            status=status,
            summary=summary,
            diagnostics=tuple(diagnostics),
            operational_sections={"impact_summary": operational_summary} if operational_summary else {},
            charts=charts,
            evidence_refs=tuple(dict.fromkeys(evidence_refs)),
        )

    def operational_view(
        self,
        *,
        audience: OrchestrationAudience,
        forge_context: Mapping[str, Any],
    ) -> OrchestrationViewResult:
        if audience not in _OPERATIONAL_AUDIENCES:
            raise PermissionError("operational view is not available to this audience")

        discovery = forge_context.get("governed_discovery") or {}
        linked = discovery.get("linked_records") or {}
        evidence_by_source = forge_context.get("evidence_by_source") or {}
        evidence_refs = tuple(
            dict.fromkeys(
                str(ref)
                for refs in evidence_by_source.values()
                for ref in (refs or ())
                if ref
            )
        )

        sections: dict[str, Any] = {
            "scope": discovery.get("scope"),
            "demand": linked.get("elo_sim_demanda", []),
            "materials": linked.get("elo_sim_demanda_materiais", []),
            "resources": linked.get("elo_sim_demanda_recursos", []),
            "coverage": linked.get("v_elo_pcp_cobertura_demanda_externa", []),
            "capacity": linked.get("v_elo_pcp_carga_capacidade_periodo", []),
            "external_operations": linked.get("v_elo_pcp_indicadores_montagem_externa", []),
            "decision": linked.get("v_elo_pcp_decisao_externa_resumo", []),
            "budget_learning": linked.get("elo_orcamento_decisoes", []),
            "budget_associations": linked.get("elo_orcamento_associacoes", []),
            "missing_data": linked.get("v_elo_pcp_dados_pendentes", []),
            "not_scoped": discovery.get("not_linked") or discovery.get("not_scoped") or [],
        }

        diagnostics: list[DiagnosticItem] = []
        for item in sections["missing_data"] if isinstance(sections["missing_data"], list) else []:
            diagnostics.append(
                DiagnosticItem(
                    code=str(item.get("codigo") or "DADO_PENDENTE"),
                    title="Informação operacional pendente",
                    state="BLOQUEADO_POR_DADOS" if item.get("bloqueia_execucao") else "PENDENTE",
                    explanation=str(item.get("motivo") or item.get("pergunta_gpt") or "Dado necessário ainda não foi comprovado."),
                    impact="Sem esse dado, o ELO deve limitar cálculo, recomendação ou fechamento que dependa dele.",
                    recommendation=str(item.get("pergunta_gpt") or "Consultar a fonte autorizada indicada pelo Forge."),
                )
            )

        charts = self._operational_charts(sections)
        observed_sections = sum(1 for value in sections.values() if isinstance(value, list) and value)
        status = "OBSERVED" if observed_sections else "SEM_DADO_OPERACIONAL"
        summary = (
            f"Visão operacional governada: {observed_sections} seções com registros observados. "
            "A saída relaciona demanda, recursos, cobertura, capacidade, decisões e aprendizado de orçamento somente quando as fontes governadas fornecem evidência."
        )
        return OrchestrationViewResult(
            audience=audience,
            view=OrchestrationView.OPERATIONAL,
            status=status,
            summary=summary,
            diagnostics=tuple(diagnostics),
            operational_sections=sections,
            charts=charts,
            evidence_refs=evidence_refs,
        )

    @staticmethod
    def _operational_impact_summary(context: Mapping[str, Any]) -> str:
        discovery = context.get("governed_discovery") or {}
        linked = discovery.get("linked_records") or {}
        if not linked:
            return ""
        available = [name for name, rows in linked.items() if isinstance(rows, list) and rows]
        if not available:
            return "As fontes operacionais foram consultadas, mas não há registros observados suficientes para quantificar impacto."
        return "Fontes operacionais com evidência observada: " + ", ".join(sorted(available)) + "."

    @staticmethod
    def _operational_charts(sections: Mapping[str, Any]) -> tuple[ChartSpec, ...]:
        data = []
        for key in ("demand", "materials", "resources", "coverage", "capacity", "external_operations", "decision", "budget_learning"):
            rows = sections.get(key)
            if isinstance(rows, list):
                data.append(ChartDatum(key, float(len(rows)), "OBSERVED" if rows else "NO_RECORD"))
        return (
            ChartSpec(
                chart_id="operational_evidence_coverage",
                title="Cobertura de evidência operacional",
                kind="bar",
                unit="records",
                data=tuple(data),
                note="Contagem de registros por domínio; não converte ausência de registro em desempenho zero.",
            ),
        )


__all__ = [
    "ChartDatum",
    "ChartSpec",
    "DiagnosticItem",
    "OrchestrationAudience",
    "OrchestrationView",
    "OrchestrationViewComposer",
    "OrchestrationViewResult",
]
