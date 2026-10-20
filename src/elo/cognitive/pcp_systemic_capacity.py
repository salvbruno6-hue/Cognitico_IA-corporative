"""Deterministic systemic-capacity guards for Multiteiner PCP.

Owner: SKILL_PLANEJAMENTO_MULTITEINER / PCP cognitive control
Authority: implementation only

This module does not own BOM, stock, capacity baselines, routes, or operational
records. Callers must provide already-governed, already-compatible capacities in
module-equivalent units. It then computes the executable system capacity without
inventing conversions or silently ignoring required constraints.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import isfinite
from typing import Mapping, Sequence


@dataclass(frozen=True, slots=True)
class SystemicCapacityAssessment:
    demand_modules: float
    executable_modules: float | None
    limiting_constraints: tuple[str, ...]
    missing_constraints: tuple[str, ...]
    constraint_capacities: Mapping[str, float | None]
    status: str
    canonical_mutation: bool = False


@dataclass(frozen=True, slots=True)
class ELDayProjection:
    day_index: int
    opening_el: float
    releases_before_consumption: float
    available_before_consumption: float
    planned_assembly: float
    realizable_assembly: float
    closing_el: float


@dataclass(frozen=True, slots=True)
class SystemicCapacityDay:
    """Governed daily snapshot supplied to first-constraint reasoning."""

    reference_date: date
    demand_modules: float
    constraint_capacities: Mapping[str, float | None]


@dataclass(frozen=True, slots=True)
class FirstConstraintAssessment:
    """Earliest confirmed systemic constraint or an explicit evidence gap."""

    first_constraint_date: date | None
    limiting_constraints: tuple[str, ...]
    evidence_gap_date: date | None
    missing_constraints: tuple[str, ...]
    evaluated_dates: tuple[date, ...]
    status: str
    canonical_mutation: bool = False


def _validate_non_negative(value: float, field: str) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{field} must be finite and non-negative")


def _normalize_required_constraints(required_constraints: Sequence[str]) -> tuple[str, ...]:
    required = tuple(
        dict.fromkeys(
            name.strip().upper()
            for name in required_constraints
            if name and name.strip()
        )
    )
    if not required:
        raise ValueError("required_constraints must contain at least one constraint")
    return required


def _validate_capacity_day_order(days: Sequence[SystemicCapacityDay]) -> None:
    """Validate the complete chronology before any early-returning reasoning."""
    previous_date: date | None = None
    for day in days:
        if not isinstance(day.reference_date, date):
            raise TypeError("reference_date must be datetime.date")
        if previous_date is not None and day.reference_date <= previous_date:
            raise ValueError("days must be strictly ordered by unique reference_date")
        previous_date = day.reference_date


def assess_systemic_capacity(
    demand_modules: float,
    constraint_capacities: Mapping[str, float | None],
    *,
    required_constraints: Sequence[str] | None = None,
) -> SystemicCapacityAssessment:
    """Return the bottleneck capacity from already-normalized constraints.

    Capacities must already be expressed in compatible module-equivalent units.
    This function never converts telhas, cubas, hours, structures, or materials
    into modules. Such conversions belong upstream to governed BOM/mix/evidence.
    """
    _validate_non_negative(demand_modules, "demand_modules")

    normalized: dict[str, float | None] = {}
    for raw_name, value in constraint_capacities.items():
        name = raw_name.strip().upper()
        if not name:
            raise ValueError("constraint name is required")
        if value is not None:
            _validate_non_negative(value, f"constraint {name}")
        normalized[name] = value

    required = tuple(
        dict.fromkeys(
            name.strip().upper()
            for name in (required_constraints or normalized.keys())
            if name.strip()
        )
    )
    missing = tuple(name for name in required if normalized.get(name) is None)
    if missing:
        return SystemicCapacityAssessment(
            demand_modules=demand_modules,
            executable_modules=None,
            limiting_constraints=(),
            missing_constraints=missing,
            constraint_capacities=normalized,
            status="ANALISE_BLOQUEADA",
        )

    if demand_modules == 0:
        return SystemicCapacityAssessment(
            demand_modules=0.0,
            executable_modules=0.0,
            limiting_constraints=(),
            missing_constraints=(),
            constraint_capacities=normalized,
            status="SEM_DEMANDA",
        )

    capacities = {name: normalized[name] for name in required}
    if not capacities:
        return SystemicCapacityAssessment(
            demand_modules=demand_modules,
            executable_modules=demand_modules,
            limiting_constraints=(),
            missing_constraints=(),
            constraint_capacities=normalized,
            status="SEM_RESTRICAO_FORNECIDA",
        )

    minimum_capacity = min(
        float(value) for value in capacities.values() if value is not None
    )
    executable = min(demand_modules, minimum_capacity)
    limiting = tuple(
        name
        for name, value in capacities.items()
        if value is not None
        and float(value) == minimum_capacity
        and minimum_capacity < demand_modules
    )

    return SystemicCapacityAssessment(
        demand_modules=demand_modules,
        executable_modules=executable,
        limiting_constraints=limiting,
        missing_constraints=(),
        constraint_capacities=normalized,
        status="CAPACIDADE_SISTEMICA_CALCULADA",
    )


def find_first_constraint_date(
    days: Sequence[SystemicCapacityDay],
    *,
    required_constraints: Sequence[str],
) -> FirstConstraintAssessment:
    """Return the earliest confirmed systemic bottleneck in a governed series.

    The constraint universe must be explicit. The complete date sequence is
    validated before capacity reasoning so an early bottleneck/evidence gap
    cannot hide malformed later chronology. Missing or indeterminate required
    evidence on an earlier date blocks the answer instead of being interpreted
    as evidence that no constraint existed.
    """
    required = _normalize_required_constraints(required_constraints)
    _validate_capacity_day_order(days)
    if not days:
        return FirstConstraintAssessment(
            first_constraint_date=None,
            limiting_constraints=(),
            evidence_gap_date=None,
            missing_constraints=required,
            evaluated_dates=(),
            status="EVIDENCIA_INSUFICIENTE",
        )

    evaluated_dates: list[date] = []
    for day in days:
        assessment = assess_systemic_capacity(
            day.demand_modules,
            day.constraint_capacities,
            required_constraints=required,
        )
        evaluated_dates.append(day.reference_date)

        if (
            assessment.status == "ANALISE_BLOQUEADA"
            or assessment.executable_modules is None
        ):
            return FirstConstraintAssessment(
                first_constraint_date=None,
                limiting_constraints=(),
                evidence_gap_date=day.reference_date,
                missing_constraints=assessment.missing_constraints,
                evaluated_dates=tuple(evaluated_dates),
                status="EVIDENCIA_INSUFICIENTE",
            )

        if (
            assessment.executable_modules < day.demand_modules
            and assessment.limiting_constraints
        ):
            return FirstConstraintAssessment(
                first_constraint_date=day.reference_date,
                limiting_constraints=assessment.limiting_constraints,
                evidence_gap_date=None,
                missing_constraints=(),
                evaluated_dates=tuple(evaluated_dates),
                status="PRIMEIRA_RESTRICAO_CONFIRMADA",
            )

    return FirstConstraintAssessment(
        first_constraint_date=None,
        limiting_constraints=(),
        evidence_gap_date=None,
        missing_constraints=(),
        evaluated_dates=tuple(evaluated_dates),
        status="SEM_RESTRICAO_CONFIRMADA",
    )


def project_el(
    initial_el: float,
    releases_before_consumption: Sequence[float],
    planned_assembly: Sequence[float],
) -> tuple[ELDayProjection, ...]:
    """Project EL cumulatively and cap assembly by physical EL availability.

    Releases are counted only when explicitly supplied as occurring before that
    day's assembly consumption. No same-day release timing is inferred.
    """
    _validate_non_negative(initial_el, "initial_el")
    if len(releases_before_consumption) != len(planned_assembly):
        raise ValueError("release and assembly series must have the same length")

    opening = initial_el
    result: list[ELDayProjection] = []
    for index, (release, planned) in enumerate(
        zip(releases_before_consumption, planned_assembly, strict=True), start=1
    ):
        _validate_non_negative(release, "release")
        _validate_non_negative(planned, "planned_assembly")
        available = opening + release
        realizable = min(planned, available)
        closing = available - realizable
        result.append(
            ELDayProjection(
                day_index=index,
                opening_el=opening,
                releases_before_consumption=release,
                available_before_consumption=available,
                planned_assembly=planned,
                realizable_assembly=realizable,
                closing_el=closing,
            )
        )
        opening = closing
    return tuple(result)


__all__ = [
    "ELDayProjection",
    "FirstConstraintAssessment",
    "SystemicCapacityAssessment",
    "SystemicCapacityDay",
    "assess_systemic_capacity",
    "find_first_constraint_date",
    "project_el",
]
