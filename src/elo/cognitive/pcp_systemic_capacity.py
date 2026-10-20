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


def _validate_non_negative(value: float, field: str) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{field} must be finite and non-negative")


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

    required = tuple(dict.fromkeys(
        name.strip().upper() for name in (required_constraints or normalized.keys()) if name.strip()
    ))
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

    minimum_capacity = min(float(value) for value in capacities.values() if value is not None)
    executable = min(demand_modules, minimum_capacity)
    limiting = tuple(
        name for name, value in capacities.items()
        if value is not None and float(value) == minimum_capacity and minimum_capacity < demand_modules
    )

    return SystemicCapacityAssessment(
        demand_modules=demand_modules,
        executable_modules=executable,
        limiting_constraints=limiting,
        missing_constraints=(),
        constraint_capacities=normalized,
        status="CAPACIDADE_SISTEMICA_CALCULADA",
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
    "SystemicCapacityAssessment",
    "assess_systemic_capacity",
    "project_el",
]
