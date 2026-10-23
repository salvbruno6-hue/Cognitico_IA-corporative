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
from datetime import date, datetime
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
class ELOperationalEvent:
    """Provider-neutral projection of one canonical ``mt_eventos_el`` row."""

    event_type: str
    quantity: float
    occurred_at: datetime
    evidence_ref: str | None = None


@dataclass(frozen=True, slots=True)
class ELBalanceAssessment:
    """Actual EL balance derived only from explicit operational events."""

    available_quantity: float
    blocked_quantity: float
    entered_quantity: float
    exited_quantity: float
    blocked_total: float
    unblocked_total: float
    event_count: int
    evidence_refs: tuple[str, ...]
    status: str


@dataclass(frozen=True, slots=True)
class DailyConstraintSnapshot:
    day: date
    constraint_capacities: Mapping[str, float | None]
    required_constraints: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class FirstConstraint:
    day: date | None
    resource_codes: tuple[str, ...]
    requested_quantity: float
    executable_quantity: float | None
    status: str


_EL_EVENT_TYPES = frozenset({"ENTRADA_EL", "SAIDA_EL", "BLOQUEIO", "DESBLOQUEIO"})


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


def assess_el_event_balance(
    events: Sequence[ELOperationalEvent],
    *,
    as_of: datetime | None = None,
) -> ELBalanceAssessment:
    """Derive actual available/blocked EL solely from canonical EL events.

    Supported event types mirror the existing database contract exactly:
    ``ENTRADA_EL``, ``SAIDA_EL``, ``BLOQUEIO`` and ``DESBLOQUEIO``.

    The calculation is intentionally strict. A withdrawal cannot exceed available
    EL, a block cannot exceed available EL, and an unblock cannot exceed blocked
    EL. Invalid event sequences are rejected instead of being normalized or
    inferred. Structure completion, painting, curing, quality or any other event
    never enters EL unless an explicit ``ENTRADA_EL`` is supplied.
    """
    available = 0.0
    blocked = 0.0
    entered = 0.0
    exited = 0.0
    blocked_total = 0.0
    unblocked_total = 0.0
    evidence_refs: list[str] = []
    processed = 0

    for event in sorted(events, key=lambda item: item.occurred_at):
        if as_of is not None and event.occurred_at > as_of:
            continue
        event_type = event.event_type.strip().upper()
        if event_type not in _EL_EVENT_TYPES:
            raise ValueError(f"unsupported EL event type: {event.event_type}")
        _validate_non_negative(event.quantity, f"EL event {event_type} quantity")
        quantity = float(event.quantity)

        if event_type == "ENTRADA_EL":
            available += quantity
            entered += quantity
        elif event_type == "SAIDA_EL":
            if quantity > available:
                raise ValueError("SAIDA_EL cannot exceed available EL")
            available -= quantity
            exited += quantity
        elif event_type == "BLOQUEIO":
            if quantity > available:
                raise ValueError("BLOQUEIO cannot exceed available EL")
            available -= quantity
            blocked += quantity
            blocked_total += quantity
        else:  # DESBLOQUEIO
            if quantity > blocked:
                raise ValueError("DESBLOQUEIO cannot exceed blocked EL")
            blocked -= quantity
            available += quantity
            unblocked_total += quantity

        processed += 1
        if event.evidence_ref and event.evidence_ref.strip():
            evidence_refs.append(event.evidence_ref.strip())

    return ELBalanceAssessment(
        available_quantity=available,
        blocked_quantity=blocked,
        entered_quantity=entered,
        exited_quantity=exited,
        blocked_total=blocked_total,
        unblocked_total=unblocked_total,
        event_count=processed,
        evidence_refs=tuple(dict.fromkeys(evidence_refs)),
        status="SEM_EVENTOS_EL" if processed == 0 else "SALDO_EL_POR_EVENTOS",
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


def first_constraint_date(
    *,
    requested_by_day: Mapping[date, float],
    snapshots: Sequence[DailyConstraintSnapshot],
) -> FirstConstraint:
    """Return the first date where complete planned quantity is not executable.

    Missing daily evidence fails closed. The function reuses the canonical
    systemic-capacity calculation and does not introduce a second capacity model.
    """
    by_day = {snapshot.day: snapshot for snapshot in snapshots}
    for day in sorted(requested_by_day):
        requested = requested_by_day[day]
        _validate_non_negative(requested, f"requested {day.isoformat()}")
        snapshot = by_day.get(day)
        if snapshot is None:
            return FirstConstraint(day, (), requested, None, "EVIDENCIA_INSUFICIENTE")

        assessment = assess_systemic_capacity(
            requested,
            snapshot.constraint_capacities,
            required_constraints=snapshot.required_constraints or None,
        )
        if assessment.executable_modules is None:
            return FirstConstraint(
                day,
                assessment.missing_constraints,
                requested,
                None,
                "EVIDENCIA_INSUFICIENTE",
            )
        if assessment.executable_modules < requested:
            return FirstConstraint(
                day,
                assessment.limiting_constraints,
                requested,
                assessment.executable_modules,
                "PRIMEIRA_RESTRICAO",
            )

    return FirstConstraint(None, (), 0.0, None, "SEM_RUPTURA_IDENTIFICADA")


__all__ = [
    "DailyConstraintSnapshot",
    "ELBalanceAssessment",
    "ELDayProjection",
    "ELOperationalEvent",
    "FirstConstraint",
    "SystemicCapacityAssessment",
    "assess_el_event_balance",
    "assess_systemic_capacity",
    "first_constraint_date",
    "project_el",
]
