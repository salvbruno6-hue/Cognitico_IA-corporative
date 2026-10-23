"""Route model-mix demand to applicable production constraints.

Owner: SKILL_PLANEJAMENTO_MULTITEINER / PCP cognitive control
Authority: implementation only

The canonical production route remains in Supabase. This module only consumes an
already-governed model -> applicable constraint mapping and turns a model mix
into per-constraint demand. It does not invent routes, capacities or model
aliases beyond the established ``MLT.Mxx``/``Mxx`` code normalization.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping, Sequence


@dataclass(frozen=True, slots=True)
class RoutedConstraintDemand:
    constraint: str
    demand_modules: float
    contributing_models: tuple[str, ...]
    excluded_models: tuple[str, ...]


def _normalize_model_code(raw_code: str) -> str:
    code = raw_code.strip().upper()
    if not code:
        raise ValueError("model code is required")
    if code.startswith("MLT.M"):
        return code[4:]
    return code


def _normalize_constraint(raw_constraint: str) -> str:
    constraint = raw_constraint.strip().upper()
    if not constraint:
        raise ValueError("constraint code is required")
    return constraint


def _validate_non_negative(value: float, field: str) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{field} must be finite and non-negative")


def route_mix_demand_by_constraint(
    demand_by_model: Mapping[str, float],
    applicable_constraints_by_model: Mapping[str, Sequence[str]],
    *,
    constraints: Sequence[str] | None = None,
) -> tuple[RoutedConstraintDemand, ...]:
    """Convert a model mix into demand for each applicable production constraint.

    Every demanded model must have an explicit route mapping. Missing route
    evidence fails closed instead of assuming the standard route. This is what
    prevents a special model such as M16 from silently consuming CHASSI capacity.

    ``constraints`` may be supplied when the caller needs zero-demand rows for a
    known stage that no demanded model uses. Without it, the result contains the
    union of constraints explicitly present in the supplied route mappings.
    """
    normalized_demand: dict[str, float] = {}
    for raw_model, quantity in demand_by_model.items():
        model = _normalize_model_code(raw_model)
        _validate_non_negative(quantity, f"demand {model}")
        normalized_demand[model] = normalized_demand.get(model, 0.0) + float(quantity)

    normalized_routes: dict[str, tuple[str, ...]] = {}
    for raw_model, route in applicable_constraints_by_model.items():
        model = _normalize_model_code(raw_model)
        normalized_routes[model] = tuple(dict.fromkeys(_normalize_constraint(item) for item in route))

    missing_routes = tuple(
        sorted(model for model, quantity in normalized_demand.items() if quantity > 0 and model not in normalized_routes)
    )
    if missing_routes:
        raise ValueError(f"missing governed route for demanded models: {', '.join(missing_routes)}")

    if constraints is None:
        constraint_set = {
            constraint
            for model in normalized_demand
            for constraint in normalized_routes.get(model, ())
        }
    else:
        constraint_set = {_normalize_constraint(item) for item in constraints}

    result: list[RoutedConstraintDemand] = []
    demanded_models = tuple(sorted(model for model, quantity in normalized_demand.items() if quantity > 0))
    for constraint in sorted(constraint_set):
        total = 0.0
        contributing: list[str] = []
        excluded: list[str] = []
        for model in demanded_models:
            quantity = normalized_demand[model]
            if constraint in normalized_routes[model]:
                total += quantity
                contributing.append(model)
            else:
                excluded.append(model)
        result.append(
            RoutedConstraintDemand(
                constraint=constraint,
                demand_modules=total,
                contributing_models=tuple(contributing),
                excluded_models=tuple(excluded),
            )
        )
    return tuple(result)


__all__ = ["RoutedConstraintDemand", "route_mix_demand_by_constraint"]
