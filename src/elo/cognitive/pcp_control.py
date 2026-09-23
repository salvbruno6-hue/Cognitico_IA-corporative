"""PCP control and evidence utilities.

This module closes the domain-side capabilities that can be developed without
operational PCP records: planned-vs-actual comparison, data-readiness checks,
evidence packaging, and canonical Evolution Gate evaluation.

It does not create a lifecycle, memory, router, learning service, or Evolution
Gate. It only composes existing authorities.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Mapping, Sequence

from elo.core.evolution_gate import EvolutionDecision, EvolutionGate, EvolutionProposal


@dataclass(frozen=True)
class PlannedActualMetric:
    code: str
    planned: float | date | datetime | None
    actual: float | date | datetime | None
    variance: float | int | None
    status: str
    unit: str | None = None
    note: str | None = None


def compare_quantity(
    planned: float | None,
    actual: float | None,
    *,
    unit: str | None = None,
) -> PlannedActualMetric:
    if planned is None or actual is None:
        return PlannedActualMetric(
            "PA_QTD", planned, actual, None, "NAO_LOCALIZADO", unit,
            "planejado ou realizado ausente",
        )
    return PlannedActualMetric(
        "PA_QTD", planned, actual, actual - planned, "CALCULADO", unit,
    )


def compare_duration(
    planned_hours: float | None,
    actual_hours: float | None,
) -> PlannedActualMetric:
    if planned_hours is None or actual_hours is None:
        return PlannedActualMetric(
            "PA_TEMPO", planned_hours, actual_hours, None, "NAO_LOCALIZADO",
            "horas", "tempo planejado ou realizado ausente",
        )
    return PlannedActualMetric(
        "PA_TEMPO", planned_hours, actual_hours,
        actual_hours - planned_hours, "CALCULADO", "horas",
    )


def compare_date(
    planned: date | datetime | None,
    actual: date | datetime | None,
    *,
    code: str = "PA_DATA",
) -> PlannedActualMetric:
    if planned is None or actual is None:
        return PlannedActualMetric(
            code, planned, actual, None, "NAO_LOCALIZADO",
            "dias", "data planejada ou realizada ausente",
        )
    p = planned.date() if isinstance(planned, datetime) else planned
    a = actual.date() if isinstance(actual, datetime) else actual
    return PlannedActualMetric(code, planned, actual, (a - p).days, "CALCULADO", "dias")


@dataclass(frozen=True)
class PCPDataReadiness:
    required: tuple[str, ...]
    available: tuple[str, ...]
    missing: tuple[str, ...]
    status: str


def assess_data_readiness(
    available_sources: Sequence[str],
    *,
    required_sources: Sequence[str] = (
        "mt_planos_pcp",
        "mt_linhas_plano_pcp",
        "mt_ordens_producao",
        "mt_operacoes_ordem_producao",
        "mt_capacidade_diaria",
        "mt_necessidades_materiais",
        "mt_lotes_estoque",
        "mt_eventos_fluxo_modular",
    ),
) -> PCPDataReadiness:
    available = tuple(dict.fromkeys(available_sources))
    required = tuple(dict.fromkeys(required_sources))
    missing = tuple(source for source in required if source not in available)
    return PCPDataReadiness(
        required=required,
        available=available,
        missing=missing,
        status="PRONTO" if not missing else "PENDENTE_DADOS",
    )


@dataclass(frozen=True)
class PCPEvidencePackage:
    observation_id: str
    source_ref: str
    source_commit: str
    evidence_ids: tuple[str, ...]
    baseline: str
    experiment: str
    expected_outcome: str
    observed_outcome: str
    result: str
    regression_status: str
    generalization_status: str
    risk: str
    existing_owner: str | None
    scope: str
    metrics: Mapping[str, object]


def build_pcp_evidence(
    *,
    observation_id: str,
    source_ref: str,
    source_commit: str,
    evidence_ids: Sequence[str],
    baseline: str,
    experiment: str,
    expected_outcome: str,
    observed_outcome: str,
    result: str,
    regression_status: str,
    generalization_status: str,
    risk: str,
    existing_owner: str | None,
    scope: str,
    metrics: Mapping[str, object] | None = None,
) -> PCPEvidencePackage:
    """Package domain evidence; it does not persist or promote anything."""
    if not evidence_ids:
        raise ValueError("PCP evidence requires at least one evidence id")
    if not source_ref or not source_commit:
        raise ValueError("PCP evidence requires source provenance")
    return PCPEvidencePackage(
        observation_id=observation_id,
        source_ref=source_ref,
        source_commit=source_commit,
        evidence_ids=tuple(dict.fromkeys(evidence_ids)),
        baseline=baseline,
        experiment=experiment,
        expected_outcome=expected_outcome,
        observed_outcome=observed_outcome,
        result=result,
        regression_status=regression_status,
        generalization_status=generalization_status,
        risk=risk,
        existing_owner=existing_owner,
        scope=scope,
        metrics=dict(metrics or {}),
    )


def evaluate_pcp_evolution(
    *,
    proposal_id: str,
    tenant_id: str,
    source_id: str,
    summary: str,
    purpose_alignment: bool,
    identity_compatible: bool,
    architecture_compatible: bool,
    governance_compatible: bool,
    evidence_ids: Sequence[str],
    maturity_score: float,
    existing_owner: str | None,
    provenance: Mapping[str, str],
) -> EvolutionDecision:
    """Delegate classification to the canonical Evolution Gate."""
    proposal = EvolutionProposal(
        proposal_id=proposal_id,
        tenant_id=tenant_id,
        source_id=source_id,
        summary=summary,
        purpose_alignment=purpose_alignment,
        identity_compatible=identity_compatible,
        architecture_compatible=architecture_compatible,
        governance_compatible=governance_compatible,
        evidence_ids=tuple(dict.fromkeys(evidence_ids)),
        maturity_score=maturity_score,
        existing_owner=existing_owner,
        provenance=provenance,
    )
    return EvolutionGate().evaluate(proposal)
