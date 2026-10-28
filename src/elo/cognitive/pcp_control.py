"""PCP control and evidence utilities.

This module closes domain-side capabilities that can be developed without
operational PCP records: planned-vs-actual comparison, data-readiness checks,
demand/capacity confrontation, material lead-time constraints, empirical
capacity learning candidates, governed mix/component explosion, systemic
capacity reasoning, EL projection, staffing ramp candidates, evidence packaging,
and canonical Evolution Gate evaluation.

It does not create a lifecycle, memory, router, learning service, hiring
authority, or Evolution Gate. It only composes existing authorities and produces
deterministic domain evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from math import ceil
from statistics import fmean
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
class DemandCapacityAssessment:
    required_quantity: float
    capacity_per_day: float | None
    productive_days: float | None
    period_capacity: float | None
    deficit: float | None
    surplus: float | None
    utilization_pct: float | None
    spillover_quantity: float | None
    status: str


def assess_demand_capacity(
    required_quantity: float,
    *,
    capacity_per_day: float | None,
    productive_days: float | None,
) -> DemandCapacityAssessment:
    """Confront required production with period capacity without inventing inputs."""
    if required_quantity < 0:
        raise ValueError("required_quantity cannot be negative")
    if capacity_per_day is None or productive_days is None:
        return DemandCapacityAssessment(
            required_quantity=required_quantity,
            capacity_per_day=capacity_per_day,
            productive_days=productive_days,
            period_capacity=None,
            deficit=None,
            surplus=None,
            utilization_pct=None,
            spillover_quantity=None,
            status="CAPACIDADE_NAO_LOCALIZADA",
        )
    if capacity_per_day < 0 or productive_days < 0:
        raise ValueError("capacity_per_day and productive_days cannot be negative")

    period_capacity = capacity_per_day * productive_days
    deficit = max(required_quantity - period_capacity, 0.0)
    surplus = max(period_capacity - required_quantity, 0.0)
    if period_capacity == 0:
        utilization = 0.0 if required_quantity == 0 else None
        status = "SEM_CAPACIDADE" if required_quantity > 0 else "SEM_DEMANDA"
    else:
        utilization = required_quantity / period_capacity * 100.0
        status = "CAPACIDADE_INSUFICIENTE" if deficit > 0 else "CAPACIDADE_SUFICIENTE"

    return DemandCapacityAssessment(
        required_quantity=required_quantity,
        capacity_per_day=capacity_per_day,
        productive_days=productive_days,
        period_capacity=period_capacity,
        deficit=deficit,
        surplus=surplus,
        utilization_pct=utilization,
        spillover_quantity=deficit,
        status=status,
    )


@dataclass(frozen=True)
class MixRequirementAssessment:
    requirements: Mapping[str, float]
    missing_bom_models: tuple[str, ...]
    status: str


def calculate_mix_component_requirements(
    model_quantities: Mapping[str, float],
    bom_by_model: Mapping[str, Mapping[str, float]],
) -> MixRequirementAssessment:
    """Explode a model mix into component demand without filling missing BOMs."""
    requirements: dict[str, float] = {}
    missing: list[str] = []

    for model, quantity in model_quantities.items():
        if quantity < 0:
            raise ValueError("model quantities cannot be negative")
        if quantity == 0:
            continue
        bom = bom_by_model.get(model)
        if bom is None:
            missing.append(model)
            continue
        for component, consumption in bom.items():
            if consumption < 0:
                raise ValueError("BOM consumption cannot be negative")
            requirements[component] = requirements.get(component, 0.0) + quantity * consumption

    missing_tuple = tuple(dict.fromkeys(missing))
    if missing_tuple and requirements:
        status = "RESPOSTA_PARCIAL"
    elif missing_tuple:
        status = "ANALISE_BLOQUEADA"
    else:
        status = "CALCULADO"
    return MixRequirementAssessment(requirements, missing_tuple, status)


@dataclass(frozen=True)
class SystemicCapacityAssessment:
    demanded_units: float
    executable_units: float | None
    limiting_constraints: tuple[str, ...]
    unknown_constraints: tuple[str, ...]
    status: str


def assess_systemic_capacity(
    demanded_units: float,
    constraint_capacities: Mapping[str, float | None],
    *,
    required_constraints: Sequence[str] | None = None,
) -> SystemicCapacityAssessment:
    """Apply the system bottleneck principle using only supplied constraints.

    Unknown required constraints are preserved as unknown. A known bottleneck can
    still establish an upper bound, but the result remains partial while any
    required constraint is unknown.
    """
    if demanded_units < 0:
        raise ValueError("demanded_units cannot be negative")

    required = tuple(dict.fromkeys(required_constraints or constraint_capacities.keys()))
    unknown: list[str] = []
    known: dict[str, float] = {}
    for name in required:
        capacity = constraint_capacities.get(name)
        if capacity is None:
            unknown.append(name)
            continue
        if capacity < 0:
            raise ValueError("constraint capacities cannot be negative")
        known[name] = capacity

    if not known:
        return SystemicCapacityAssessment(
            demanded_units, None, (), tuple(unknown), "ANALISE_BLOQUEADA"
        )

    min_capacity = min(known.values())
    executable = min(demanded_units, min_capacity)
    limiting = tuple(name for name, capacity in known.items() if capacity == min_capacity)

    if unknown:
        status = (
            "LIMITADO_COM_EVIDENCIA_PARCIAL"
            if executable < demanded_units
            else "RESPOSTA_PARCIAL"
        )
    elif executable < demanded_units:
        status = "CAPACIDADE_SISTEMICA_INSUFICIENTE"
    else:
        status = "CAPACIDADE_SISTEMICA_SUFICIENTE"

    return SystemicCapacityAssessment(
        demanded_units,
        executable,
        limiting,
        tuple(unknown),
        status,
    )


@dataclass(frozen=True)
class StaffingRampAssessment:
    required_units_per_day: float
    output_per_team_per_day: float | None
    current_teams: int
    required_teams: int | None
    additional_teams: int | None
    workers_per_team: int | None
    additional_workers: int | None
    status: str


def assess_staffing_ramp(
    required_units_per_day: float,
    *,
    output_per_team_per_day: float | None,
    current_teams: int,
    workers_per_team: int | None = None,
) -> StaffingRampAssessment:
    """Calculate an evidence-bound staffing capacity candidate, not a hiring order."""
    if required_units_per_day < 0:
        raise ValueError("required_units_per_day cannot be negative")
    if current_teams < 0:
        raise ValueError("current_teams cannot be negative")
    if workers_per_team is not None and workers_per_team <= 0:
        raise ValueError("workers_per_team must be greater than zero")
    if output_per_team_per_day is None:
        return StaffingRampAssessment(
            required_units_per_day,
            None,
            current_teams,
            None,
            None,
            workers_per_team,
            None,
            "PRODUTIVIDADE_EQUIPE_NAO_LOCALIZADA",
        )
    if output_per_team_per_day <= 0:
        raise ValueError("output_per_team_per_day must be greater than zero")

    required_teams = ceil(required_units_per_day / output_per_team_per_day)
    additional_teams = max(required_teams - current_teams, 0)
    additional_workers = (
        additional_teams * workers_per_team if workers_per_team is not None else None
    )
    status = "CAPACITY_RAMP_CANDIDATE" if additional_teams > 0 else "EQUIPE_ATUAL_SUFICIENTE"
    return StaffingRampAssessment(
        required_units_per_day,
        output_per_team_per_day,
        current_teams,
        required_teams,
        additional_teams,
        workers_per_team,
        additional_workers,
        status,
    )


@dataclass(frozen=True)
class ELDayProjection:
    day_index: int
    opening_el: float
    releases: float
    available_before_consumption: float
    planned_assembly: float
    realizable_assembly: float
    closing_el: float
    status: str


@dataclass(frozen=True)
class ELProjectionAssessment:
    days: tuple[ELDayProjection, ...]
    first_constraint_day: int | None
    status: str


def project_el_balance(
    initial_el: float,
    daily_releases: Sequence[float],
    daily_assembly_plan: Sequence[float],
    *,
    minimum_el: float = 3.0,
    target_el: float = 4.0,
    maximum_el: float = 5.0,
) -> ELProjectionAssessment:
    """Project cumulative EL and cap assembly by structures available before use."""
    if initial_el < 0:
        raise ValueError("initial_el cannot be negative")
    if len(daily_releases) != len(daily_assembly_plan):
        raise ValueError("daily_releases and daily_assembly_plan must have equal length")
    if not (0 <= minimum_el <= target_el <= maximum_el):
        raise ValueError("EL thresholds must satisfy 0 <= minimum <= target <= maximum")
    if any(v < 0 for v in daily_releases) or any(v < 0 for v in daily_assembly_plan):
        raise ValueError("EL releases and assembly plan cannot be negative")

    opening = initial_el
    rows: list[ELDayProjection] = []
    first_constraint: int | None = None
    for index, (releases, planned) in enumerate(
        zip(daily_releases, daily_assembly_plan), start=1
    ):
        available = opening + releases
        realizable = min(planned, available)
        closing = available - realizable
        if realizable < planned:
            status = "MONTAGEM_LIMITADA_POR_EL"
            if first_constraint is None:
                first_constraint = index
        elif closing < minimum_el:
            status = "EL_ABAIXO_MINIMO"
            if first_constraint is None:
                first_constraint = index
        elif closing > maximum_el:
            status = "EL_ACIMA_MAXIMO"
        elif closing == target_el:
            status = "EL_NO_ALVO"
        else:
            status = "EL_DENTRO_FAIXA"
        rows.append(
            ELDayProjection(
                index,
                opening,
                releases,
                available,
                planned,
                realizable,
                closing,
                status,
            )
        )
        opening = closing

    return ELProjectionAssessment(
        tuple(rows),
        first_constraint,
        "RESTRICAO_LOCALIZADA" if first_constraint is not None else "SEM_RESTRICAO_EL",
    )


@dataclass(frozen=True)
class MaterialAvailabilityAssessment:
    required_quantity: float
    available_quantity: float
    shortage_quantity: float
    lead_time_days: int | None
    reference_date: date
    available_on: date | None
    status: str


def assess_material_availability(
    required_quantity: float,
    available_quantity: float,
    *,
    lead_time_days: int | None,
    reference_date: date,
) -> MaterialAvailabilityAssessment:
    """Translate warehouse availability and purchase lead time into a PCP constraint.

    PCP consumes the quantity made available by Almoxarifado and the lead time
    informed for replenishment. It does not model purchase receiving, invoices,
    lots, or physical warehouse movements.
    """
    if required_quantity < 0 or available_quantity < 0:
        raise ValueError("material quantities cannot be negative")
    if lead_time_days is not None and lead_time_days < 0:
        raise ValueError("lead_time_days cannot be negative")

    shortage = max(required_quantity - available_quantity, 0.0)
    if shortage == 0:
        return MaterialAvailabilityAssessment(
            required_quantity,
            available_quantity,
            shortage,
            lead_time_days,
            reference_date,
            reference_date,
            "DISPONIVEL",
        )
    if lead_time_days is None:
        return MaterialAvailabilityAssessment(
            required_quantity,
            available_quantity,
            shortage,
            None,
            reference_date,
            None,
            "LEAD_TIME_NAO_LOCALIZADO",
        )
    return MaterialAvailabilityAssessment(
        required_quantity,
        available_quantity,
        shortage,
        lead_time_days,
        reference_date,
        reference_date + timedelta(days=lead_time_days),
        "REPOSICAO_NECESSARIA",
    )


@dataclass(frozen=True)
class CapacityLearningAssessment:
    declared_capacity: float
    observed_capacity: float | None
    sample_count: int
    deviation_pct: float | None
    direction: str | None
    confidence: float
    status: str


def assess_empirical_capacity_learning(
    declared_capacity: float,
    observed_samples: Sequence[float],
    *,
    min_samples: int = 3,
    tolerance_pct: float = 10.0,
) -> CapacityLearningAssessment:
    """Identify a governed learning candidate from repeated observed capacity.

    The result never replaces the declared baseline. A recurrent material
    deviation becomes only a candidate for evidence, testing, and Evolution Gate.
    """
    if declared_capacity <= 0:
        raise ValueError("declared_capacity must be greater than zero")
    if min_samples <= 0:
        raise ValueError("min_samples must be greater than zero")
    if tolerance_pct < 0:
        raise ValueError("tolerance_pct cannot be negative")
    if any(sample < 0 for sample in observed_samples):
        raise ValueError("observed capacity samples cannot be negative")

    sample_count = len(observed_samples)
    confidence = min(sample_count / min_samples, 1.0)
    if not observed_samples:
        return CapacityLearningAssessment(
            declared_capacity, None, 0, None, None, 0.0, "NAO_LOCALIZADO",
        )

    observed = fmean(observed_samples)
    deviation_pct = (observed - declared_capacity) / declared_capacity * 100.0
    direction = "ACIMA" if deviation_pct > 0 else "ABAIXO" if deviation_pct < 0 else "IGUAL"

    if sample_count < min_samples:
        status = "EVIDENCIA_INSUFICIENTE"
    elif abs(deviation_pct) > tolerance_pct:
        status = "CANDIDATO_AJUSTE"
    else:
        status = "ESTAVEL"

    return CapacityLearningAssessment(
        declared_capacity=declared_capacity,
        observed_capacity=observed,
        sample_count=sample_count,
        deviation_pct=deviation_pct,
        direction=direction,
        confidence=confidence,
        status=status,
    )


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
