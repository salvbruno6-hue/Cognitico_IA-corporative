"""Operational PCP analytical utilities.

Deterministic calculations over supplied PCP records. No data retrieval,
persistence, forecasting authority, learning, or mutation is performed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Sequence


@dataclass(frozen=True)
class PCPMetric:
    code: str
    value: float | int | str | None
    status: str
    inputs: dict[str, object]
    note: str | None = None


def demand_gap(demand: float | None, available: float | None) -> PCPMetric:
    if demand is None or available is None:
        return PCPMetric("GAP_DEMANDA", None, "NAO_LOCALIZADO",
                         {"demanda": demand, "disponivel": available})
    return PCPMetric("GAP_DEMANDA", demand - available, "CALCULADO",
                     {"demanda": demand, "disponivel": available})


def net_demand(demand: float | None, stock: float | None,
               scheduled_production: float | None) -> PCPMetric:
    if None in (demand, stock, scheduled_production):
        return PCPMetric("NECESSIDADE_LIQUIDA", None, "NAO_LOCALIZADO",
                         {"demanda": demand, "estoque": stock,
                          "producao_programada": scheduled_production})
    return PCPMetric(
        "NECESSIDADE_LIQUIDA",
        max(0.0, demand - stock - scheduled_production),
        "CALCULADO",
        {"demanda": demand, "estoque": stock,
         "producao_programada": scheduled_production},
    )


def capacity_load(load: float | None, capacity: float | None) -> PCPMetric:
    if load is None or capacity is None or capacity <= 0:
        return PCPMetric("UTILIZACAO_CAPACIDADE", None, "NAO_LOCALIZADO",
                         {"carga": load, "capacidade": capacity})
    return PCPMetric("UTILIZACAO_CAPACIDADE", load / capacity, "CALCULADO",
                     {"carga": load, "capacidade": capacity})


def identify_bottleneck(
    resources: Sequence[dict[str, float | str]],
) -> PCPMetric:
    if not resources:
        return PCPMetric("GARGALO", None, "NAO_LOCALIZADO", {})
    ratios = []
    for item in resources:
        load, capacity = item.get("carga"), item.get("capacidade")
        if (not isinstance(load, (int, float))
                or not isinstance(capacity, (int, float))
                or capacity <= 0):
            continue
        ratios.append((load / capacity, item.get("id", "NAO_INFORMADO")))
    if not ratios:
        return PCPMetric("GARGALO", None, "NAO_LOCALIZADO", {})
    ratio, resource_id = max(ratios, key=lambda x: x[0])
    return PCPMetric("GARGALO", ratio, "CALCULADO",
                     {"recurso": resource_id, "utilizacao": ratio})


def material_gap(gross_need: float | None, allocated: float | None,
                 purchased: float | None) -> PCPMetric:
    if None in (gross_need, allocated, purchased):
        return PCPMetric("GAP_MATERIAL", None, "NAO_LOCALIZADO",
                         {"necessidade_bruta": gross_need, "alocado": allocated,
                          "comprado": purchased})
    return PCPMetric(
        "GAP_MATERIAL", max(0.0, gross_need - allocated - purchased),
        "CALCULADO",
        {"necessidade_bruta": gross_need, "alocado": allocated,
         "comprado": purchased},
    )


def coverage(stock: float | None,
             consumption_per_period: float | None) -> PCPMetric:
    if stock is None or consumption_per_period is None or consumption_per_period <= 0:
        return PCPMetric("COBERTURA", None, "NAO_LOCALIZADO",
                         {"estoque": stock, "consumo": consumption_per_period})
    return PCPMetric("COBERTURA", stock / consumption_per_period, "CALCULADO",
                     {"estoque": stock, "consumo": consumption_per_period},
                     "periodos de cobertura")


def wip_delta(entries: float | None, exits: float | None) -> PCPMetric:
    if entries is None or exits is None:
        return PCPMetric("DELTA_WIP", None, "NAO_LOCALIZADO",
                         {"entradas": entries, "saidas": exits})
    return PCPMetric("DELTA_WIP", entries - exits, "CALCULADO",
                     {"entradas": entries, "saidas": exits})


def lead_time_days(start: date | datetime | None,
                   end: date | datetime | None) -> PCPMetric:
    if start is None or end is None:
        return PCPMetric("LEAD_TIME", None, "NAO_LOCALIZADO",
                         {"inicio": start, "fim": end})
    s = start.date() if isinstance(start, datetime) else start
    e = end.date() if isinstance(end, datetime) else end
    return PCPMetric("LEAD_TIME", (e - s).days, "CALCULADO",
                     {"inicio": start, "fim": end}, "dias corridos")


def on_time(promised: date | datetime | None,
            delivered: date | datetime | None) -> PCPMetric:
    if promised is None or delivered is None:
        return PCPMetric("OTD", None, "NAO_LOCALIZADO",
                         {"prometido": promised, "entregue": delivered})
    p = promised.date() if isinstance(promised, datetime) else promised
    d = delivered.date() if isinstance(delivered, datetime) else delivered
    return PCPMetric("OTD", 1 if d <= p else 0, "CALCULADO",
                     {"prometido": promised, "entregue": delivered})


def first_pass_yield(approved_without_rework: float | None,
                     total_completed: float | None) -> PCPMetric:
    if (approved_without_rework is None or total_completed is None
            or total_completed <= 0):
        return PCPMetric("FPY", None, "NAO_LOCALIZADO",
                         {"sem_retrabalho": approved_without_rework,
                          "concluido": total_completed})
    return PCPMetric("FPY", approved_without_rework / total_completed,
                     "CALCULADO",
                     {"sem_retrabalho": approved_without_rework,
                      "concluido": total_completed})
