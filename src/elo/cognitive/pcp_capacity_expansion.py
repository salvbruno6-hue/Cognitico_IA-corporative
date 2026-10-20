"""Governed PCP expansion reasoning for demand-driven capacity changes.

Owner: SKILL_PLANEJAMENTO_MULTITEINER / PCP cognitive control
Authority: implementation only

This module turns already-governed demand, BOM/component requirements, stock and
capacity evidence into bounded decision signals. It never creates BOM, invents
conversion factors, estimates marginal worker productivity, or mutates canonical
capacity. Missing evidence remains explicit.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil, isfinite
from typing import Mapping, Sequence

from elo.cognitive.pcp_systemic_capacity import (
    SystemicCapacityAssessment,
    assess_systemic_capacity,
)


@dataclass(frozen=True, slots=True)
class MixRequirement:
    component: str
    gross_required: float | None
    available: float | None
    net_required: float | None
    affected_models: tuple[str, ...]
    status: str


@dataclass(frozen=True, slots=True)
class CapacityExpansionAction:
    target: str
    action: str
    reason: str
    current: float | None
    required: float | None
    gap: float | None
    calculated_workers: int | None = None
    evidence_required: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CapacityExpansionAssessment:
    systemic: SystemicCapacityAssessment
    mix_requirements: tuple[MixRequirement, ...]
    actions: tuple[CapacityExpansionAction, ...]
    status: str
    canonical_mutation: bool = False


def _validate_non_negative(value: float, field: str) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{field} must be finite and non-negative")


def explode_mix_requirements(
    demand_by_model: Mapping[str, float],
    bom_by_model: Mapping[str, Mapping[str, float | None]],
    *,
    available_components: Mapping[str, float | None] | None = None,
) -> tuple[MixRequirement, ...]:
    """Explode model mix only from explicit per-model BOM quantities.

    A component becomes unresolved when any demanded model that references it has
    no proven quantity. This prevents a partial BOM from silently becoming a
    complete material requirement.
    """
    available_components = available_components or {}
    components: set[str] = set()
    normalized_demand: dict[str, float] = {}
    for raw_model, qty in demand_by_model.items():
        model = raw_model.strip().upper()
        if not model:
            raise ValueError("model code is required")
        _validate_non_negative(qty, f"demand {model}")
        normalized_demand[model] = qty
        for component in bom_by_model.get(model, {}):
            if component.strip():
                components.add(component.strip().upper())

    results: list[MixRequirement] = []
    for component in sorted(components):
        total = 0.0
        unresolved = False
        affected: list[str] = []
        for model, demand_qty in normalized_demand.items():
            if demand_qty == 0:
                continue
            model_bom = {
                key.strip().upper(): value
                for key, value in bom_by_model.get(model, {}).items()
                if key.strip()
            }
            if component not in model_bom:
                continue
            affected.append(model)
            unit_qty = model_bom[component]
            if unit_qty is None:
                unresolved = True
                continue
            _validate_non_negative(unit_qty, f"BOM {model}/{component}")
            total += demand_qty * unit_qty

        available = available_components.get(component)
        if available is not None:
            _validate_non_negative(available, f"available {component}")

        if unresolved:
            gross = None
            net = None
            status = "BOM_INCOMPLETA"
        else:
            gross = total
            net = None if available is None else max(total - available, 0.0)
            status = "ESTOQUE_NAO_LOCALIZADO" if available is None else (
                "COMPRA_NECESSARIA" if net > 0 else "COBERTO"
            )

        results.append(
            MixRequirement(
                component=component,
                gross_required=gross,
                available=available,
                net_required=net,
                affected_models=tuple(sorted(affected)),
                status=status,
            )
        )
    return tuple(results)


def assess_capacity_expansion(
    demand_modules: float,
    constraint_capacities: Mapping[str, float | None],
    *,
    required_constraints: Sequence[str] | None = None,
    demand_by_model: Mapping[str, float] | None = None,
    bom_by_model: Mapping[str, Mapping[str, float | None]] | None = None,
    available_components: Mapping[str, float | None] | None = None,
    worker_increment_capacity: Mapping[str, float | None] | None = None,
) -> CapacityExpansionAssessment:
    """Assess what must change before demand-driven capacity can increase safely.

    ``worker_increment_capacity`` is optional explicit evidence of additional
    module-equivalent capacity per added worker for a named constraint. Without
    it the function requests staffing measurement/review and does not invent a
    headcount.
    """
    systemic = assess_systemic_capacity(
        demand_modules,
        constraint_capacities,
        required_constraints=required_constraints,
    )
    mix = explode_mix_requirements(
        demand_by_model or {},
        bom_by_model or {},
        available_components=available_components,
    )

    actions: list[CapacityExpansionAction] = []
    worker_increment_capacity = {
        key.strip().upper(): value
        for key, value in (worker_increment_capacity or {}).items()
        if key.strip()
    }

    for requirement in mix:
        if requirement.status == "COMPRA_NECESSARIA":
            actions.append(
                CapacityExpansionAction(
                    target=requirement.component,
                    action="EMITIR_NECESSIDADE_COMPRAS",
                    reason="mix/BOM comprovado excede estoque disponível",
                    current=requirement.available,
                    required=requirement.gross_required,
                    gap=requirement.net_required,
                )
            )
        elif requirement.status == "BOM_INCOMPLETA":
            actions.append(
                CapacityExpansionAction(
                    target=requirement.component,
                    action="BLOQUEAR_QUANTIDADE_E_VALIDAR_BOM",
                    reason="ao menos um modelo demandado possui consumo não comprovado",
                    current=requirement.available,
                    required=None,
                    gap=None,
                    evidence_required=("consumo_unitario_validado",),
                )
            )
        elif requirement.status == "ESTOQUE_NAO_LOCALIZADO":
            actions.append(
                CapacityExpansionAction(
                    target=requirement.component,
                    action="CONSULTAR_ESTOQUE",
                    reason="necessidade bruta calculável, mas disponibilidade não localizada",
                    current=None,
                    required=requirement.gross_required,
                    gap=None,
                    evidence_required=("estoque_utilizavel",),
                )
            )

    if systemic.executable_modules is None:
        for missing in systemic.missing_constraints:
            actions.append(
                CapacityExpansionAction(
                    target=missing,
                    action="LOCALIZAR_CAPACIDADE",
                    reason="restrição obrigatória sem capacidade compatível comprovada",
                    current=None,
                    required=demand_modules,
                    gap=None,
                    evidence_required=("capacidade_compativel", "unidade_compativel"),
                )
            )
        status = "EXPANSAO_BLOQUEADA"
        return CapacityExpansionAssessment(systemic, mix, tuple(actions), status)

    capacity_gap = max(demand_modules - systemic.executable_modules, 0.0)
    for constraint in systemic.limiting_constraints:
        current = systemic.constraint_capacities.get(constraint)
        increment = worker_increment_capacity.get(constraint)
        calculated_workers: int | None = None
        evidence_required: tuple[str, ...] = ()
        action = "AUMENTAR_CAPACIDADE_RECURSO"
        if increment is None:
            action = "REVISAR_RECURSO_E_MEDIR_INCREMENTO"
            evidence_required = ("produtividade_marginal_por_colaborador",)
        else:
            _validate_non_negative(increment, f"worker increment {constraint}")
            if increment == 0:
                action = "REVISAR_RECURSO_SEM_GANHO_MARGINAL"
                evidence_required = ("alternativa_de_capacidade",)
            elif capacity_gap > 0:
                calculated_workers = ceil(capacity_gap / increment)

        actions.append(
            CapacityExpansionAction(
                target=constraint,
                action=action,
                reason="recurso limita a capacidade sistêmica frente à demanda",
                current=current,
                required=demand_modules,
                gap=capacity_gap,
                calculated_workers=calculated_workers,
                evidence_required=evidence_required,
            )
        )

    status = "SEM_EXPANSAO_NECESSARIA" if capacity_gap == 0 and not actions else "PLANO_EXPANSAO_GOVERNADO"
    return CapacityExpansionAssessment(systemic, mix, tuple(actions), status)


__all__ = [
    "CapacityExpansionAction",
    "CapacityExpansionAssessment",
    "MixRequirement",
    "assess_capacity_expansion",
    "explode_mix_requirements",
]
