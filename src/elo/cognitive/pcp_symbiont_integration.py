"""PCP analytical integration with the existing Symbiont boundary.

This module does not create a new loop, memory, router, registry or evolution gate.
It integrates the PCP Skill's unique analytical knowledge with existing ELO mechanisms:
- existing virtual diagnosis is reused, not reimplemented;
- existing Supabase PCP views/tables remain data authorities;
- existing Symbiont runtime remains the governed handoff;
- formulas from the PCP Skill are implemented here because they were not found as
  an equivalent executable analytical kernel in the existing runtime.

All functions are deterministic and side-effect free.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from math import inf
from typing import Mapping, Sequence

from elo.core.decision_outcome_loop import DecisionLifecycle
from .symbiont_skill_runtime import SymbiontSkillRuntime
from .symbionte_lab import SymbiontLabObservation


@dataclass(frozen=True)
class CalculationResult:
    code: str
    value: float | bool | int | None
    status: str
    inputs: Mapping[str, object]
    unit: str | None = None
    formula: str | None = None
    note: str | None = None


def _missing(**values: object) -> tuple[str, ...]:
    return tuple(name for name, value in values.items() if value is None)


def net_requirement(demand: float | None, stock_available: float | None,
                    safety_stock: float | None) -> CalculationResult:
    missing = _missing(demand=demand, stock_available=stock_available, safety_stock=safety_stock)
    if missing:
        return CalculationResult("NL", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="NL = D - (EA - ES)")
    value = demand - (stock_available - safety_stock)
    return CalculationResult("NL", max(0.0, value), "CALCULADO",
                             {"D": demand, "EA": stock_available, "ES": safety_stock},
                             formula="NL = D - (EA - ES)")


def material_requirement(product_need: float | None,
                         unit_consumption: float | None) -> CalculationResult:
    missing = _missing(product_need=product_need, unit_consumption=unit_consumption)
    if missing:
        return CalculationResult("NM", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="NM = NecessidadeProduto x ConsumoUnitario")
    value = product_need * unit_consumption
    return CalculationResult("NM", value, "CALCULADO",
                             {"NecessidadeProduto": product_need, "ConsumoUnitario": unit_consumption},
                             formula="NM = NecessidadeProduto x ConsumoUnitario")


def net_material_requirement(gross_need: float | None, material_stock: float | None,
                             material_safety_stock: float | None) -> CalculationResult:
    missing = _missing(NM=gross_need, EM=material_stock, ESM=material_safety_stock)
    if missing:
        return CalculationResult("NLM", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="NLM = NM - (EM - ESM)")
    value = gross_need - (material_stock - material_safety_stock)
    return CalculationResult("NLM", max(0.0, value), "CALCULADO",
                             {"NM": gross_need, "EM": material_stock, "ESM": material_safety_stock},
                             formula="NLM = NM - (EM - ESM)")


def coverage(stock_available: float | None,
             consumption_per_period: float | None) -> CalculationResult:
    missing = _missing(EstoqueDisponivel=stock_available, ConsumoPorPeriodo=consumption_per_period)
    if missing or consumption_per_period == 0:
        return CalculationResult("COB", None, "NAO_LOCALIZADO",
                                 {"missing": missing, "division_by_zero": consumption_per_period == 0},
                                 formula="COB = EstoqueDisponivel / ConsumoPorPeriodo")
    value = stock_available / consumption_per_period
    return CalculationResult("COB", value, "CALCULADO",
                             {"EstoqueDisponivel": stock_available,
                              "ConsumoPorPeriodo": consumption_per_period},
                             unit="periodos",
                             formula="COB = EstoqueDisponivel / ConsumoPorPeriodo")


def coverage_vs_lead_time(coverage_periods: float | None,
                          lead_time_periods: float | None) -> CalculationResult:
    missing = _missing(COB=coverage_periods, LeadTime=lead_time_periods)
    if missing or lead_time_periods == 0:
        return CalculationResult("ICL", None, "NAO_LOCALIZADO",
                                 {"missing": missing, "division_by_zero": lead_time_periods == 0},
                                 formula="ICL = COB / LeadTime")
    value = coverage_periods / lead_time_periods
    return CalculationResult("ICL", value, "CALCULADO",
                             {"COB": coverage_periods, "LeadTime": lead_time_periods},
                             formula="ICL = COB / LeadTime")


def order_date(need_date: date | None, lead_time_days: int | None) -> CalculationResult:
    missing = _missing(DataNecessidade=need_date, LeadTime=lead_time_days)
    if missing:
        return CalculationResult("DP", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="DP = DN - LeadTime")
    value = need_date - timedelta(days=lead_time_days)
    return CalculationResult("DP", value.isoformat(), "CALCULADO",
                             {"DN": need_date.isoformat(), "LeadTime": lead_time_days},
                             unit="data", formula="DP = DN - LeadTime")


def delivery_date(order: date | None, lead_time_days: int | None) -> CalculationResult:
    missing = _missing(DataPedido=order, LeadTime=lead_time_days)
    if missing:
        return CalculationResult("DE", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="DE = DP + LeadTime")
    value = order + timedelta(days=lead_time_days)
    return CalculationResult("DE", value.isoformat(), "CALCULADO",
                             {"DP": order.isoformat(), "LeadTime": lead_time_days},
                             unit="data", formula="DE = DP + LeadTime")


def rupture_risk(projected_delivery: date | None,
                 need_date: date | None) -> CalculationResult:
    missing = _missing(DataEntrega=projected_delivery, DataNecessidade=need_date)
    if missing:
        return CalculationResult("RUP", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="RUP = DE > DN")
    value = projected_delivery > need_date
    return CalculationResult("RUP", value, "CALCULADO",
                             {"DE": projected_delivery.isoformat(), "DN": need_date.isoformat()},
                             formula="RUP = DE > DN")


def potential_delay(projected_delivery: date | None,
                    need_date: date | None) -> CalculationResult:
    missing = _missing(DataEntrega=projected_delivery, DataNecessidade=need_date)
    if missing:
        return CalculationResult("ATR", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="ATR = DE - DN")
    value = (projected_delivery - need_date).days
    return CalculationResult("ATR", value, "CALCULADO",
                             {"DE": projected_delivery.isoformat(), "DN": need_date.isoformat()},
                             unit="dias", formula="ATR = DE - DN")


def capacity(available_time: float | None,
             cycle_time: float | None) -> CalculationResult:
    missing = _missing(TDA=available_time, CT=cycle_time)
    if missing or cycle_time == 0:
        return CalculationResult("CAP", None, "NAO_LOCALIZADO",
                                 {"missing": missing, "division_by_zero": cycle_time == 0},
                                 formula="CAP = TDA / CT")
    value = available_time / cycle_time
    return CalculationResult("CAP", value, "CALCULADO",
                             {"TDA": available_time, "CT": cycle_time},
                             unit="unidades", formula="CAP = TDA / CT")


def utilization(demand: float | None, capacity_value: float | None) -> CalculationResult:
    missing = _missing(Demanda=demand, Capacidade=capacity_value)
    if missing or capacity_value == 0:
        return CalculationResult("UTI", None, "NAO_LOCALIZADO",
                                 {"missing": missing, "division_by_zero": capacity_value == 0},
                                 formula="UTI = Demanda / Capacidade")
    value = demand / capacity_value
    return CalculationResult("UTI", value, "CALCULADO",
                             {"Demanda": demand, "Capacidade": capacity_value},
                             unit="razao", formula="UTI = Demanda / Capacidade")


def bottleneck(resources: Sequence[Mapping[str, float]]) -> CalculationResult:
    if not resources:
        return CalculationResult("GARG", None, "NAO_LOCALIZADO", {"missing": ("recursos",)},
                                 formula="GARG = argmax(Carga_i / Capacidade_i)")
    ratios: list[tuple[str, float]] = []
    for resource in resources:
        name = resource.get("id")
        load = resource.get("carga")
        cap = resource.get("capacidade")
        if name is None or load is None or cap is None or cap == 0:
            continue
        ratios.append((str(name), load / cap))
    if not ratios:
        return CalculationResult("GARG", None, "NAO_LOCALIZADO",
                                 {"missing": ("carga/capacidade",)},
                                 formula="GARG = argmax(Carga_i / Capacidade_i)")
    selected, ratio = max(ratios, key=lambda item: item[1])
    return CalculationResult("GARG", ratio, "CALCULADO",
                             {"recurso": selected, "utilizacao": ratio},
                             unit="razao", formula="GARG = argmax(Carga_i / Capacidade_i)")


def wip_delta(entry: float | None, output: float | None) -> CalculationResult:
    missing = _missing(Entrada=entry, Saida=output)
    if missing:
        return CalculationResult("WIP", None, "NAO_LOCALIZADO", {"missing": missing},
                                 formula="DeltaWIP = Entrada - Saida")
    return CalculationResult("WIP", entry - output, "CALCULADO",
                             {"Entrada": entry, "Saida": output},
                             formula="DeltaWIP = Entrada - Saida")


def setup_total(setups: Sequence[float] | None) -> CalculationResult:
    if setups is None:
        return CalculationResult("SETUP", None, "NAO_LOCALIZADO", {"missing": ("Tsetup_j",)},
                                 formula="TsetupTotal = soma(Tsetup_j)")
    value = sum(setups)
    return CalculationResult("SETUP", value, "CALCULADO",
                             {"Tsetup_j": tuple(setups)},
                             unit="tempo", formula="TsetupTotal = soma(Tsetup_j)")


@dataclass(frozen=True)
class PCPMechanismBinding:
    mechanism: str
    role: str
    owner: str
    action: str


MECHANISM_BINDINGS: tuple[PCPMechanismBinding, ...] = (
    PCPMechanismBinding("analise_estruturar", "precondicao", "SKILL_PLANEJAMENTO_MULTITEINER",
                        "estruturar demanda, fluxo, dependencias e restricoes antes da decisao"),
    PCPMechanismBinding("planejamento_restricoes", "decisao", "SKILL_PLANEJAMENTO_MULTITEINER",
                        "testar restricoes criticas antes de programar"),
    PCPMechanismBinding("pcp_motor_analitico_demanda_planejamento", "calculo", "SKILL_PLANEJAMENTO_MULTITEINER",
                        "aplicar formulas NL/NM/NLM/COB/ICL/DP/DE/RUP/ATR/CAP/UTI/GARG/WIP/SETUP quando variaveis existirem"),
    PCPMechanismBinding("produto_contexto", "contexto", "Forge Specialist Skill Registry",
                        "selecionar aplicabilidade por contexto; nao substituir pelo nome do produto"),
    PCPMechanismBinding("modulacao_por_contexto", "contexto", "SIMBIONTE-ADAPT-001",
                        "comparar contexto e registrar adaptacoes sem criar autoridade paralela"),
    PCPMechanismBinding("analise_validar", "governanca", "Loop Simbionte / Evolution Gate",
                        "validar evidencia, teste, conflito, aplicabilidade e confianca"),
    PCPMechanismBinding("diagnose", "diagnostico", "elo-virtual-core/regras/orquestrador.py",
                        "reutilizar sinais de atraso material e gargalo de capacidade"),
    PCPMechanismBinding("v_elo_pcp_inteligente", "fonte", "Supabase",
                        "consultar visao integrada como substrato de cenario; nao tratar como Skill"),
)


def mechanism_bindings() -> tuple[PCPMechanismBinding, ...]:
    return MECHANISM_BINDINGS


def prepare_symbiont_evidence(*, request_id: str, source_ref: str,
                              source_commit: str, evidence_ids: Sequence[str],
                              baseline: str, experiment: str, result: str,
                              expected_outcome: str, observed_outcome: str,
                              regression_status: str, generalization_status: str,
                              existing_owner: str,
                              scope: str, tenant_id: str = "pcp",
                              domain: str = "PCP") -> dict[str, object]:
    """Prepare the evidence payload for the existing SymbiontLabAdapter.

    This function does not call the adapter and does not persist learning.
    The canonical runtime remains responsible for the governed handoff.
    """
    return {
        "observation_id": request_id,
        "tenant_id": tenant_id,
        "domain": domain,
        "decision_id": request_id,
        "expected_outcome": expected_outcome,
        "observed_outcome": observed_outcome,
        "evidence_ids": tuple(evidence_ids),
        "source_ref": source_ref,
        "source_commit": source_commit,
        "hypothesis": result,
        "baseline": baseline,
        "experiment": experiment,
        "result": result,
        "regression_status": regression_status,
        "generalization_status": generalization_status,
        "risk": "LOW",
        "existing_owner": existing_owner,
        "scope": scope,
        "tenant_scope": tenant_id,
        "source_kind": "benchmark",
    }


def handoff_symbiont_evidence(
    lifecycle: DecisionLifecycle,
    *,
    adapter: object,
    evidence_payload: Mapping[str, object],
    principal_id: str,
    dataset_version: str,
):
    """Route a PCP laboratory observation through the canonical Symbiont handoff.

    The PCP Skill supplies the analytical evidence; DecisionLifecycle and the
    existing Symbiont runtime remain the authorities for governed learning.
    """
    observation = SymbiontLabObservation(
        observation_id=str(evidence_payload["observation_id"]),
        tenant_id=str(evidence_payload["tenant_id"]),
        domain=str(evidence_payload["domain"]),
        decision_id=str(evidence_payload["decision_id"]),
        expected_outcome=str(evidence_payload["expected_outcome"]),
        observed_outcome=str(evidence_payload["observed_outcome"]),
        evidence_ids=tuple(evidence_payload["evidence_ids"]),
        source_ref=str(evidence_payload["source_ref"]),
        source_commit=str(evidence_payload["source_commit"]),
        hypothesis=str(evidence_payload["hypothesis"]),
        baseline=str(evidence_payload["baseline"]),
        experiment=str(evidence_payload["experiment"]),
        result=str(evidence_payload["result"]),
        regression_status=str(evidence_payload["regression_status"]),
        generalization_status=str(evidence_payload["generalization_status"]),
        risk=str(evidence_payload["risk"]),
        existing_owner=str(evidence_payload["existing_owner"]),
        scope=str(evidence_payload["scope"]),
        tenant_scope=str(evidence_payload.get("tenant_scope")) if evidence_payload.get("tenant_scope") is not None else None,
        source_kind=str(evidence_payload.get("source_kind")) if evidence_payload.get("source_kind") is not None else None,
    )
    return SymbiontSkillRuntime.handoff_decision(
        lifecycle,
        adapter=adapter,
        observation=observation,
        principal_id=principal_id,
        dataset_version=dataset_version,
    )
