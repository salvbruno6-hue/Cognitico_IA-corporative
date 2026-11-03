"""PCP staffing evidence adapter for governed capacity-expansion decisions.

Owner: ``pcp_capacity_expansion`` / SKILL_PLANEJAMENTO_MULTITEINER.
Authority: implementation/read model only.

This module does not own HR data and does not create a staffing registry. It
translates missing operational context into explicit evidence gaps that the
Orchestrator can prioritize through the canonical critical-gap reasoning
capability. A historical throughput observation remains useful, but hiring is
never recommended until labor is proven to be the causal constraint and a
marginal productivity increment has been measured.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Mapping

from elo.cognitive.reasoning.critical_gap_reasoning import (
    CriticalEvidenceGap,
    CriticalGapPlan,
    GapCriticality,
    ObservationBoundary,
    prioritize_evidence_gaps,
    qualify_observation,
)


class StaffingEvidenceState(StrEnum):
    EVIDENCE_COLLECTION_REQUIRED = "EVIDENCE_COLLECTION_REQUIRED"
    CAUSE_NOT_ESTABLISHED = "CAUSE_NOT_ESTABLISHED"
    NON_LABOR_CONSTRAINT = "NON_LABOR_CONSTRAINT"
    MARGINAL_PRODUCTIVITY_REQUIRED = "MARGINAL_PRODUCTIVITY_REQUIRED"
    STAFFING_EVIDENCE_READY = "STAFFING_EVIDENCE_READY"


_CONTEXT_REQUIREMENTS = (
    ("periodo_observado", "delimitar o período que produziu a taxa observada", "sem período não é possível avaliar estabilidade ou vigência", GapCriticality.CRITICAL),
    ("equipe_por_setor_funcao", "registrar quantidade de colaboradores por setor e função no período", "sem composição da equipe não é possível relacionar carga, função e saída", GapCriticality.CRITICAL),
    ("turnos_jornada", "registrar turnos e jornada efetivamente trabalhada", "sem jornada a taxa diária pode esconder diferenças de horas disponíveis", GapCriticality.HIGH),
    ("horas_extras", "registrar horas extras do período", "sem horas extras não se distingue capacidade sustentável de esforço extraordinário", GapCriticality.HIGH),
    ("absenteismo", "registrar faltas, férias e afastamentos que afetaram a equipe", "sem disponibilidade real não se conhece a capacidade humana efetiva", GapCriticality.HIGH),
    ("mix_modelos", "registrar mix M01, M02 e demais modelos efetivamente montados", "sem mix não se separa produtividade de complexidade do produto", GapCriticality.CRITICAL),
    ("el_disponivel", "registrar EL disponível antes do consumo de montagem", "sem EL não se sabe se a oficina esteve limitada por alimentação e não por pessoas", GapCriticality.CRITICAL),
    ("esperas_material", "registrar esperas e paradas por material/componente", "sem esperas não se separa ociosidade induzida de falta de mão de obra", GapCriticality.HIGH),
    ("retrabalho_reprovacao", "registrar retrabalho e reprovação", "sem qualidade não se conhece a produção líquida boa", GapCriticality.HIGH),
    ("wip", "registrar módulos em processo no início e fim do período", "sem WIP a saída pode consumir trabalho acumulado anteriormente", GapCriticality.MEDIUM),
    ("equipamentos_indisponibilidades", "registrar equipamentos relevantes e indisponibilidades", "sem disponibilidade física mão de obra pode ser falsamente identificada como gargalo", GapCriticality.HIGH),
    ("producao_realizada", "registrar módulos concluídos/liberados por dia no período", "sem realizado não existe base empírica para relacionar recursos e resultado", GapCriticality.CRITICAL),
)


@dataclass(frozen=True, slots=True)
class StaffingEvidenceAssessment:
    state: StaffingEvidenceState
    gap_plan: CriticalGapPlan
    observation: ObservationBoundary | None
    causal_constraint: str | None
    marginal_productivity_per_worker: float | None
    can_calculate_headcount: bool
    canonical_mutation: bool = False


def _is_missing_evidence(parameter: str, value: object | None) -> bool:
    """Separate an absent observation from an explicitly observed zero/none state.

    For equipment downtime, ``[]`` is a valid observation meaning that no
    indisponibility was recorded in the observed period. Structural evidence
    such as mix/team mappings still requires a non-empty payload.
    """
    if value is None or value == "":
        return True
    if parameter == "equipamentos_indisponibilidades":
        return False
    return value == () or value == [] or value == {}


def assess_staffing_evidence(
    evidence: Mapping[str, object | None],
    *,
    observed_modules_per_day: float | None = None,
    observation_source: str = "OPERACAO_CAMPO",
    causal_constraint: str | None = None,
    marginal_productivity_per_worker: float | None = None,
    decision: str = "CONTRATACAO_MONTAGEM",
) -> StaffingEvidenceAssessment:
    """Assess whether staffing evidence is sufficient for a hiring calculation."""
    gaps: list[CriticalEvidenceGap] = []
    missing_context: list[str] = []
    for parameter, action, impact, criticality in _CONTEXT_REQUIREMENTS:
        value = evidence.get(parameter)
        if not _is_missing_evidence(parameter, value):
            continue
        missing_context.append(parameter)
        gaps.append(
            CriticalEvidenceGap(
                gap_id=f"PCP.STAFFING.{parameter.upper()}",
                parameter=parameter,
                decision=decision,
                missing_condition=f"{parameter} não evidenciado",
                operational_impact=impact,
                collection_action=action,
                owner="PCP/PRODUCAO",
                criticality=criticality,
                decision_sensitivity=5 if criticality is GapCriticality.CRITICAL else 4,
                collection_effort=2,
                blocks_decision=True,
            )
        )

    observation: ObservationBoundary | None = None
    if observed_modules_per_day is not None:
        if not isfinite(observed_modules_per_day) or observed_modules_per_day <= 0:
            raise ValueError("observed_modules_per_day must be finite and greater than zero")
        observation = qualify_observation(
            observation_id="PCP.MONTAGEM.THROUGHPUT.OBSERVADO",
            statement=f"montagem observada em {observed_modules_per_day:g} módulos/dia",
            source_ref=observation_source,
            missing_context=tuple(missing_context),
            allow_scenario=True,
            authorize_canonical_rule=False,
        )

    plan = prioritize_evidence_gaps(gaps)
    if gaps:
        return StaffingEvidenceAssessment(
            state=StaffingEvidenceState.EVIDENCE_COLLECTION_REQUIRED,
            gap_plan=plan,
            observation=observation,
            causal_constraint=causal_constraint,
            marginal_productivity_per_worker=marginal_productivity_per_worker,
            can_calculate_headcount=False,
        )

    normalized_constraint = causal_constraint.strip().upper() if causal_constraint else None
    if normalized_constraint is None:
        return StaffingEvidenceAssessment(
            state=StaffingEvidenceState.CAUSE_NOT_ESTABLISHED,
            gap_plan=plan,
            observation=observation,
            causal_constraint=None,
            marginal_productivity_per_worker=marginal_productivity_per_worker,
            can_calculate_headcount=False,
        )
    if normalized_constraint not in {"MAO_DE_OBRA", "MÃO_DE_OBRA", "LABOR", "STAFFING"}:
        return StaffingEvidenceAssessment(
            state=StaffingEvidenceState.NON_LABOR_CONSTRAINT,
            gap_plan=plan,
            observation=observation,
            causal_constraint=normalized_constraint,
            marginal_productivity_per_worker=marginal_productivity_per_worker,
            can_calculate_headcount=False,
        )

    if marginal_productivity_per_worker is None:
        return StaffingEvidenceAssessment(
            state=StaffingEvidenceState.MARGINAL_PRODUCTIVITY_REQUIRED,
            gap_plan=plan,
            observation=observation,
            causal_constraint=normalized_constraint,
            marginal_productivity_per_worker=None,
            can_calculate_headcount=False,
        )
    if not isfinite(marginal_productivity_per_worker) or marginal_productivity_per_worker <= 0:
        raise ValueError("marginal_productivity_per_worker must be finite and greater than zero")

    return StaffingEvidenceAssessment(
        state=StaffingEvidenceState.STAFFING_EVIDENCE_READY,
        gap_plan=plan,
        observation=observation,
        causal_constraint=normalized_constraint,
        marginal_productivity_per_worker=marginal_productivity_per_worker,
        can_calculate_headcount=True,
    )


__all__ = [
    "StaffingEvidenceAssessment",
    "StaffingEvidenceState",
    "assess_staffing_evidence",
]
