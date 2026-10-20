"""Governed deterministic PCP reasoning for systemic flow constraints.

This module does not persist data, invent business inputs, or create a new
planning authority. It composes explicitly supplied evidence to answer bounded
questions about systemic capacity, EL availability, assembly realizability,
model-mix requirements, aliases, and the first date at which a plan becomes
unprovable or infeasible.

All business values (capacity, EL thresholds, BOM consumption, release times)
are inputs. Callers must source them from governed evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Mapping, Sequence


@dataclass(frozen=True)
class SystemicCapacityAssessment:
    demand: float
    systemic_capacity: float | None
    executable_quantity: float | None
    deficit: float | None
    limiting_constraints: tuple[str, ...]
    missing_constraints: tuple[str, ...]
    status: str


def assess_systemic_capacity(
    demand: float,
    constraints: Mapping[str, float | None],
) -> SystemicCapacityAssessment:
    """Return the minimum confirmed constraint without filling missing evidence."""
    if demand < 0:
        raise ValueError("demand cannot be negative")
    if not constraints:
        return SystemicCapacityAssessment(
            demand, None, None, None, (), (), "RESTRICOES_NAO_LOCALIZADAS"
        )

    missing = tuple(name for name, value in constraints.items() if value is None)
    for value in constraints.values():
        if value is not None and value < 0:
            raise ValueError("constraint values cannot be negative")

    known = {name: value for name, value in constraints.items() if value is not None}
    if missing:
        return SystemicCapacityAssessment(
            demand=demand,
            systemic_capacity=None,
            executable_quantity=None,
            deficit=None,
            limiting_constraints=(),
            missing_constraints=missing,
            status="EVIDENCIA_INSUFICIENTE",
        )

    minimum = min(known.values()) if known else None
    assert minimum is not None
    limiting = tuple(name for name, value in known.items() if value == minimum)
    executable = min(demand, minimum)
    deficit = max(demand - executable, 0.0)
    return SystemicCapacityAssessment(
        demand=demand,
        systemic_capacity=minimum,
        executable_quantity=executable,
        deficit=deficit,
        limiting_constraints=limiting,
        missing_constraints=(),
        status="RESTRICAO_CONFIRMADA" if deficit > 0 else "EXECUTAVEL",
    )


@dataclass(frozen=True)
class AssemblyRealizabilityAssessment:
    planned_quantity: float
    el_before_consumption: float
    releases_before_consumption: float
    capacity_ceiling: float
    upper_bound: float
    realizable_quantity: float | None
    missing_constraints: tuple[str, ...]
    status: str


def assess_assembly_realizability(
    planned_quantity: float,
    *,
    el_before_consumption: float,
    nominal_capacity: float,
    recovery: bool = False,
    recovery_capacity: float | None = None,
    releases_before_consumption: float = 0.0,
    other_constraints: Mapping[str, float | None] | None = None,
) -> AssemblyRealizabilityAssessment:
    """Bound assembly by EL, declared mode capacity, and supplied constraints.

    Releases count only when the caller confirms they occur before consumption.
    Recovery capacity is never inferred from nominal capacity.
    """
    values = (planned_quantity, el_before_consumption, nominal_capacity, releases_before_consumption)
    if any(value < 0 for value in values):
        raise ValueError("assembly quantities and capacities cannot be negative")
    if recovery_capacity is not None and recovery_capacity < 0:
        raise ValueError("recovery_capacity cannot be negative")
    if recovery and recovery_capacity is None:
        return AssemblyRealizabilityAssessment(
            planned_quantity,
            el_before_consumption,
            releases_before_consumption,
            nominal_capacity,
            min(planned_quantity, el_before_consumption + releases_before_consumption, nominal_capacity),
            None,
            ("recovery_capacity",),
            "EVIDENCIA_INSUFICIENTE",
        )

    capacity_ceiling = recovery_capacity if recovery else nominal_capacity
    assert capacity_ceiling is not None
    el_available = el_before_consumption + releases_before_consumption
    base_upper = min(planned_quantity, el_available, capacity_ceiling)

    extra = dict(other_constraints or {})
    for value in extra.values():
        if value is not None and value < 0:
            raise ValueError("other constraint values cannot be negative")
    missing = tuple(name for name, value in extra.items() if value is None)
    known_limits = [value for value in extra.values() if value is not None]
    upper = min([base_upper, *known_limits]) if known_limits else base_upper

    if missing:
        return AssemblyRealizabilityAssessment(
            planned_quantity,
            el_before_consumption,
            releases_before_consumption,
            capacity_ceiling,
            upper,
            None,
            missing,
            "EVIDENCIA_INSUFICIENTE",
        )

    return AssemblyRealizabilityAssessment(
        planned_quantity,
        el_before_consumption,
        releases_before_consumption,
        capacity_ceiling,
        upper,
        upper,
        (),
        "LIMITADA" if upper < planned_quantity else "EXECUTAVEL",
    )


@dataclass(frozen=True)
class ELDayInput:
    day: date
    releases_before_consumption: float
    planned_consumption: float


@dataclass(frozen=True)
class ELDayProjection:
    day: date
    opening_balance: float
    releases_before_consumption: float
    available_before_consumption: float
    planned_consumption: float
    realizable_consumption: float
    closing_balance: float
    status: str


def project_el_cumulative(
    initial_el: float,
    days: Sequence[ELDayInput],
    *,
    minimum: float,
    target: float,
    maximum: float,
) -> tuple[ELDayProjection, ...]:
    """Project EL cumulatively; never make same-day unconfirmed releases available."""
    if min(initial_el, minimum, target, maximum) < 0:
        raise ValueError("EL values cannot be negative")
    if not (minimum <= target <= maximum):
        raise ValueError("EL thresholds must satisfy minimum <= target <= maximum")

    balance = initial_el
    result: list[ELDayProjection] = []
    for item in sorted(days, key=lambda value: value.day):
        if item.releases_before_consumption < 0 or item.planned_consumption < 0:
            raise ValueError("EL releases and consumption cannot be negative")
        opening = balance
        available = opening + item.releases_before_consumption
        realizable = min(item.planned_consumption, available)
        balance = available - realizable
        if balance < minimum:
            status = "ABAIXO_MINIMO"
        elif balance > maximum:
            status = "ACIMA_MAXIMO"
        elif balance == target:
            status = "ALVO"
        else:
            status = "FAIXA_OPERACIONAL"
        result.append(
            ELDayProjection(
                day=item.day,
                opening_balance=opening,
                releases_before_consumption=item.releases_before_consumption,
                available_before_consumption=available,
                planned_consumption=item.planned_consumption,
                realizable_consumption=realizable,
                closing_balance=balance,
                status=status,
            )
        )
    return tuple(result)


@dataclass(frozen=True)
class ELAvailabilityAssessment:
    completed_at: datetime | None
    released_at: datetime | None
    reference_at: datetime
    available_in_el: bool | None
    status: str


def assess_el_availability(
    *,
    completed_at: datetime | None,
    released_at: datetime | None,
    reference_at: datetime,
) -> ELAvailabilityAssessment:
    """Treat the release event, not production completion, as EL availability."""
    if released_at is None:
        return ELAvailabilityAssessment(
            completed_at, released_at, reference_at, None, "LIBERACAO_NAO_CONFIRMADA"
        )
    available = released_at <= reference_at
    return ELAvailabilityAssessment(
        completed_at,
        released_at,
        reference_at,
        available,
        "DISPONIVEL" if available else "AGUARDANDO_LIBERACAO",
    )


@dataclass(frozen=True)
class MixRequirementAssessment:
    component_code: str
    total_requirement: float | None
    missing_models: tuple[str, ...]
    contributions: tuple[tuple[str, float], ...]
    status: str


def assess_mix_component_requirement(
    component_code: str,
    mix: Mapping[str, float],
    consumption_by_model: Mapping[str, float | None],
) -> MixRequirementAssessment:
    """Calculate a component only for the model mix with explicit consumption evidence.

    A zero consumption explicitly means the component does not apply to the model.
    Missing/None evidence blocks a definitive total for demanded models.
    """
    if any(quantity < 0 for quantity in mix.values()):
        raise ValueError("mix quantities cannot be negative")
    if any(value is not None and value < 0 for value in consumption_by_model.values()):
        raise ValueError("component consumption cannot be negative")

    missing = tuple(
        model
        for model, quantity in mix.items()
        if quantity > 0 and (model not in consumption_by_model or consumption_by_model[model] is None)
    )
    contributions = tuple(
        (model, quantity * float(consumption_by_model[model]))
        for model, quantity in mix.items()
        if quantity > 0
        and model in consumption_by_model
        and consumption_by_model[model] is not None
    )
    if missing:
        return MixRequirementAssessment(
            component_code, None, missing, contributions, "EVIDENCIA_INSUFICIENTE"
        )
    return MixRequirementAssessment(
        component_code,
        sum(value for _, value in contributions),
        (),
        contributions,
        "CALCULADO",
    )


@dataclass(frozen=True)
class MaterialRequirement:
    code: str
    quantity: float
    unit: str


@dataclass(frozen=True)
class ConsolidatedMaterialRequirement:
    canonical_code: str
    quantity: float | None
    unit: str | None
    source_codes: tuple[str, ...]
    status: str


def consolidate_material_aliases(
    requirements: Sequence[MaterialRequirement],
    alias_to_canonical: Mapping[str, str],
) -> tuple[ConsolidatedMaterialRequirement, ...]:
    """Consolidate only aliases explicitly mapped by a governed caller."""
    groups: dict[str, list[MaterialRequirement]] = {}
    for item in requirements:
        if item.quantity < 0:
            raise ValueError("material requirement cannot be negative")
        canonical = alias_to_canonical.get(item.code, item.code)
        groups.setdefault(canonical, []).append(item)

    result: list[ConsolidatedMaterialRequirement] = []
    for canonical, items in groups.items():
        units = {item.unit for item in items}
        sources = tuple(dict.fromkeys(item.code for item in items))
        if len(units) != 1:
            result.append(
                ConsolidatedMaterialRequirement(
                    canonical, None, None, sources, "CONFLITO_UNIDADE"
                )
            )
            continue
        result.append(
            ConsolidatedMaterialRequirement(
                canonical,
                sum(item.quantity for item in items),
                next(iter(units)),
                sources,
                "CONSOLIDADO",
            )
        )
    return tuple(result)


@dataclass(frozen=True)
class DailyConstraintSnapshot:
    day: date
    demand: float
    constraints: Mapping[str, float | None]


@dataclass(frozen=True)
class FirstConstraintAssessment:
    day: date | None
    resource: str | None
    need: float | None
    available: float | None
    deficit: float | None
    missing_constraints: tuple[str, ...]
    status: str


def find_first_constraint_date(
    snapshots: Sequence[DailyConstraintSnapshot],
) -> FirstConstraintAssessment:
    """Return the earliest confirmed rupture, or stop at earlier missing evidence."""
    for snapshot in sorted(snapshots, key=lambda value: value.day):
        assessment = assess_systemic_capacity(snapshot.demand, snapshot.constraints)
        if assessment.status == "EVIDENCIA_INSUFICIENTE":
            return FirstConstraintAssessment(
                snapshot.day,
                None,
                snapshot.demand,
                None,
                None,
                assessment.missing_constraints,
                "EVIDENCIA_INSUFICIENTE",
            )
        if assessment.deficit and assessment.deficit > 0:
            resource = assessment.limiting_constraints[0]
            available = snapshot.constraints[resource]
            return FirstConstraintAssessment(
                snapshot.day,
                resource,
                snapshot.demand,
                available,
                assessment.deficit,
                (),
                "FIRST_CONSTRAINT_DATE",
            )
    return FirstConstraintAssessment(None, None, None, None, None, (), "SEM_RUPTURA_CONFIRMADA")
