"""Governed systemic PCP reasoning without inventing operational inputs.

This module extends the existing PCP cognitive layer with deterministic,
read-only reasoning for systemic capacity, EL projection, mix/BOM explosion,
first-constraint detection and cross-domain handoffs.

It does not own business data, persist records, change capacity, authorize
hiring or purchasing, or create a new operational source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Mapping, Sequence


@dataclass(frozen=True, slots=True)
class ConstraintEvidence:
    code: str
    required_quantity: float | None
    available_quantity: float | None
    unit: str
    evidence_ref: str | None
    applies: bool = True

    def validate(self) -> None:
        for name, value in (
            ("required_quantity", self.required_quantity),
            ("available_quantity", self.available_quantity),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{name} cannot be negative")


@dataclass(frozen=True, slots=True)
class SystemicCapacityAssessment:
    requested_quantity: float
    executable_quantity: float | None
    limiting_constraints: tuple[str, ...]
    missing_constraints: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    status: str


def assess_systemic_capacity(
    requested_quantity: float,
    constraints: Sequence[ConstraintEvidence],
) -> SystemicCapacityAssessment:
    """Assess complete executable quantity from simultaneous constraints.

    Any applicable constraint with missing required/available quantity or missing
    provenance keeps the complete capacity inconclusive. Known constraints are
    still inspected to identify an upper bound, but that upper bound is not
    promoted as complete capacity.
    """
    if requested_quantity < 0:
        raise ValueError("requested_quantity cannot be negative")

    applicable = [constraint for constraint in constraints if constraint.applies]
    missing: list[str] = []
    evidence_refs: list[str] = []
    known_limits: list[tuple[str, float]] = []

    for constraint in applicable:
        constraint.validate()
        if not constraint.evidence_ref or not constraint.evidence_ref.strip():
            missing.append(constraint.code)
            continue
        evidence_refs.append(constraint.evidence_ref.strip())
        if constraint.required_quantity is None or constraint.available_quantity is None:
            missing.append(constraint.code)
            continue
        known_limits.append(
            (
                constraint.code,
                min(constraint.required_quantity, constraint.available_quantity),
            )
        )

    if missing:
        return SystemicCapacityAssessment(
            requested_quantity=requested_quantity,
            executable_quantity=None,
            limiting_constraints=(),
            missing_constraints=tuple(dict.fromkeys(missing)),
            evidence_refs=tuple(dict.fromkeys(evidence_refs)),
            status="EVIDENCIA_INSUFICIENTE",
        )

    if not applicable:
        return SystemicCapacityAssessment(
            requested_quantity=requested_quantity,
            executable_quantity=None,
            limiting_constraints=(),
            missing_constraints=(),
            evidence_refs=(),
            status="SEM_RESTRICOES_APLICAVEIS",
        )

    if not known_limits:
        return SystemicCapacityAssessment(
            requested_quantity=requested_quantity,
            executable_quantity=None,
            limiting_constraints=(),
            missing_constraints=(),
            evidence_refs=tuple(dict.fromkeys(evidence_refs)),
            status="EVIDENCIA_INSUFICIENTE",
        )

    executable = min([requested_quantity, *(limit for _, limit in known_limits)])
    limiting = tuple(
        code for code, limit in known_limits if limit == executable and executable < requested_quantity
    )
    status = "LIMITADO" if executable < requested_quantity else "EXECUTAVEL"
    return SystemicCapacityAssessment(
        requested_quantity=requested_quantity,
        executable_quantity=executable,
        limiting_constraints=limiting,
        missing_constraints=(),
        evidence_refs=tuple(dict.fromkeys(evidence_refs)),
        status=status,
    )


@dataclass(frozen=True, slots=True)
class ELDayProjection:
    day: date
    el_initial: float
    releases: float
    planned_consumption: float
    realizable_consumption: float
    el_final: float
    state: str


@dataclass(frozen=True, slots=True)
class ELProjection:
    days: tuple[ELDayProjection, ...]
    min_level: float
    target_level: float
    max_level: float
    status: str


def project_el(
    *,
    initial_el: float,
    releases_by_day: Mapping[date, float],
    planned_consumption_by_day: Mapping[date, float],
    min_level: float,
    target_level: float,
    max_level: float,
) -> ELProjection:
    """Project EL cumulatively and cap consumption by stock available before use."""
    values = (initial_el, min_level, target_level, max_level)
    if any(value < 0 for value in values):
        raise ValueError("EL values cannot be negative")
    if not min_level <= target_level <= max_level:
        raise ValueError("EL levels must satisfy min <= target <= max")
    if any(value < 0 for value in releases_by_day.values()):
        raise ValueError("releases cannot be negative")
    if any(value < 0 for value in planned_consumption_by_day.values()):
        raise ValueError("planned consumption cannot be negative")

    days = sorted(set(releases_by_day) | set(planned_consumption_by_day))
    current = initial_el
    projected: list[ELDayProjection] = []

    for day in days:
        releases = float(releases_by_day.get(day, 0.0))
        planned = float(planned_consumption_by_day.get(day, 0.0))
        before_consumption = current + releases
        realizable = min(planned, before_consumption)
        final = before_consumption - realizable

        if final < min_level:
            state = "ABAIXO_MINIMO"
        elif final > max_level:
            state = "ACIMA_MAXIMO"
        elif final == target_level:
            state = "NO_ALVO"
        else:
            state = "DENTRO_FAIXA"

        projected.append(
            ELDayProjection(
                day=day,
                el_initial=current,
                releases=releases,
                planned_consumption=planned,
                realizable_consumption=realizable,
                el_final=final,
                state=state,
            )
        )
        current = final

    status = "RISCO_RUPTURA" if any(day.state == "ABAIXO_MINIMO" for day in projected) else "CONTROLADO"
    return ELProjection(
        days=tuple(projected),
        min_level=min_level,
        target_level=target_level,
        max_level=max_level,
        status=status,
    )


@dataclass(frozen=True, slots=True)
class MixRequirementAssessment:
    requirements: Mapping[str, float]
    missing_models: tuple[str, ...]
    status: str


def explode_mix_requirements(
    model_mix: Mapping[str, float],
    bom_by_model: Mapping[str, Mapping[str, float]],
) -> MixRequirementAssessment:
    """Explode component requirements by production mix without assuming missing BOMs."""
    requirements: dict[str, float] = {}
    missing_models: list[str] = []

    for model, quantity in model_mix.items():
        if quantity < 0:
            raise ValueError("model quantities cannot be negative")
        bom = bom_by_model.get(model)
        if bom is None:
            missing_models.append(model)
            continue
        for item, consumption in bom.items():
            if consumption < 0:
                raise ValueError("BOM consumption cannot be negative")
            requirements[item] = requirements.get(item, 0.0) + quantity * consumption

    return MixRequirementAssessment(
        requirements=requirements,
        missing_models=tuple(dict.fromkeys(missing_models)),
        status="COMPLETO" if not missing_models else "PARCIAL",
    )


@dataclass(frozen=True, slots=True)
class DailyConstraintSnapshot:
    day: date
    constraints: tuple[ConstraintEvidence, ...]


@dataclass(frozen=True, slots=True)
class FirstConstraint:
    day: date | None
    resource_codes: tuple[str, ...]
    requested_quantity: float
    executable_quantity: float | None
    status: str


def first_constraint_date(
    *,
    requested_by_day: Mapping[date, float],
    snapshots: Sequence[DailyConstraintSnapshot],
) -> FirstConstraint:
    """Return the first date where the requested complete quantity is not executable."""
    by_day = {snapshot.day: snapshot for snapshot in snapshots}
    for day in sorted(requested_by_day):
        requested = requested_by_day[day]
        snapshot = by_day.get(day)
        if snapshot is None:
            return FirstConstraint(day, (), requested, None, "EVIDENCIA_INSUFICIENTE")
        assessment = assess_systemic_capacity(requested, snapshot.constraints)
        if assessment.status == "EVIDENCIA_INSUFICIENTE":
            return FirstConstraint(
                day,
                assessment.missing_constraints,
                requested,
                None,
                "EVIDENCIA_INSUFICIENTE",
            )
        if assessment.executable_quantity is not None and assessment.executable_quantity < requested:
            return FirstConstraint(
                day,
                assessment.limiting_constraints,
                requested,
                assessment.executable_quantity,
                "PRIMEIRA_RESTRICAO",
            )
    return FirstConstraint(None, (), 0.0, None, "SEM_RUPTURA_IDENTIFICADA")


@dataclass(frozen=True, slots=True)
class DomainHandoff:
    domain: str
    action: str
    reason: str
    evidence_refs: tuple[str, ...]
    authorized: bool = False


def plan_cross_domain_handoffs(
    *,
    demand_increased: bool,
    material_shortage: bool | None,
    capacity_shortage: bool | None,
    labor_capacity_evidence: bool,
    parallel_flow_shortage: bool | None,
    evidence_refs: Sequence[str],
) -> tuple[DomainHandoff, ...]:
    """Create bounded handoffs; never authorizes buying, hiring or capacity changes."""
    refs = tuple(dict.fromkeys(ref.strip() for ref in evidence_refs if ref and ref.strip()))
    if not demand_increased:
        return ()

    handoffs: list[DomainHandoff] = [
        DomainHandoff(
            "PCP",
            "RECALCULATE_MIX_AND_SYSTEMIC_CAPACITY",
            "commercial demand increased; recompute mix, complete capacity and first constraint",
            refs,
        )
    ]

    if material_shortage is True:
        handoffs.append(
            DomainHandoff(
                "COMPRAS_ALMOXARIFADO",
                "RECALCULATE_NET_REQUIREMENTS_AND_PURCHASE_DEADLINES",
                "confirmed material shortage affects the increased production plan",
                refs,
            )
        )
    elif material_shortage is None:
        handoffs.append(
            DomainHandoff(
                "COMPRAS_ALMOXARIFADO",
                "COLLECT_STOCK_RESERVATION_OPEN_ORDER_AND_LEAD_TIME_EVIDENCE",
                "material sufficiency is not proven",
                refs,
            )
        )

    if capacity_shortage is True:
        action = (
            "EVALUATE_LABOR_AND_RESOURCE_SCENARIOS"
            if labor_capacity_evidence
            else "COLLECT_PRODUCTIVITY_AND_LABOR_EVIDENCE"
        )
        handoffs.append(
            DomainHandoff(
                "PRODUCAO_RH",
                action,
                "confirmed capacity deficit requires a governed recovery scenario; hiring is not auto-authorized",
                refs,
            )
        )
    elif capacity_shortage is None:
        handoffs.append(
            DomainHandoff(
                "PRODUCAO_RH",
                "COLLECT_CAPACITY_EVIDENCE",
                "capacity sufficiency is not proven",
                refs,
            )
        )

    if parallel_flow_shortage is True:
        handoffs.append(
            DomainHandoff(
                "FLUXOS_PARALELOS",
                "REPLAN_SYNCHRONIZATION",
                "a parallel component flow limits complete assembly",
                refs,
            )
        )
    elif parallel_flow_shortage is None:
        handoffs.append(
            DomainHandoff(
                "FLUXOS_PARALELOS",
                "COLLECT_COMPONENT_AVAILABILITY_EVIDENCE",
                "parallel-flow sufficiency is not proven",
                refs,
            )
        )

    return tuple(handoffs)
