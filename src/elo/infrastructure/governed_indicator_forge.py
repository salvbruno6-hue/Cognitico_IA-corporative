"""Governed indicator enrichment for the canonical Forge adapter.

This module does not own source authorization, KPI definitions, evidence,
learning, or decisions. It only enriches an existing Forge consultation with
sources already admitted by ``elo_aprendizado_fontes``.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


_INDICATOR_QUERY_TERMS = (
    "indicador",
    "indicadores",
    "kpi",
    "capacidade",
    "utilização",
    "utilizacao",
    "carga",
    "aderência",
    "aderencia",
)


def _source_rule(source: dict[str, Any]) -> dict[str, Any]:
    rule = source.get("regra_extracao")
    return rule if isinstance(rule, dict) else {}


def _is_indicator_or_kpi_source(source: dict[str, Any]) -> bool:
    rule = _source_rule(source)
    source_type = str(rule.get("tipo") or "").casefold()
    domain = str(source.get("dominio_codigo") or "").casefold()
    return "indicador" in source_type or "kpi" in source_type or domain == "gestao_indicadores"


class GovernedIndicatorForge:
    """Decorator that preserves the canonical Forge adapter as source authority."""

    def __init__(self, base: Any):
        self._base = base

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)

    def governed_demand_context(self, query: str) -> dict[str, Any]:
        context = deepcopy(self._base.governed_demand_context(query))
        normalized = query.casefold()
        if not any(term in normalized for term in _INDICATOR_QUERY_TERMS):
            return context

        governed_sources = list(self._base.governed_sources())
        selected = [source for source in governed_sources if _is_indicator_or_kpi_source(source)]

        discovery = context.setdefault("governed_discovery", {})
        linked = discovery.setdefault("linked_records", {})
        considered = discovery.setdefault("sources_considered", [])
        considered_names = {
            str(item.get("table_name"))
            for item in considered
            if isinstance(item, dict) and item.get("table_name")
        }

        source_states: list[dict[str, Any]] = []
        definitions: list[dict[str, Any]] | None = None
        snapshots: list[dict[str, Any]] | None = None

        for source in selected:
            table = str(source.get("table_name") or "")
            if not table:
                continue
            rows = self._base.read_table(table, limit=100)
            linked[table] = rows
            if table not in considered_names:
                considered.append(
                    {
                        "table_name": table,
                        "dominio_codigo": source.get("dominio_codigo"),
                        "prioridade": source.get("prioridade"),
                    }
                )
                considered_names.add(table)

            rule = _source_rule(source)
            source_states.append(
                {
                    "table_name": table,
                    "source_type": rule.get("tipo"),
                    "row_count": len(rows),
                    "read_only": rule.get("somente_leitura") is True,
                    "preserve_provenance": rule.get("preservar_proveniencia") is True,
                    "no_automatic_kpi_promotion": rule.get("nao_promover_a_kpi") is True,
                }
            )

            source_type = str(rule.get("tipo") or "").casefold()
            if source_type == "kpi_definition_registry":
                definitions = rows
            elif source_type == "kpi_snapshot_registry":
                snapshots = rows

        if definitions is None:
            formal_kpi_state = "REGISTRO_KPI_NAO_GOVERNADO"
            definition_count = None
        elif not definitions:
            formal_kpi_state = "SEM_KPI_FORMAL_REGISTRADO"
            definition_count = 0
        else:
            formal_kpi_state = "KPI_FORMAL_REGISTRADO"
            definition_count = len(definitions)

        indicator_context = {
            "state": "CONSULTED" if selected else "NO_GOVERNED_INDICATOR_SOURCE",
            "sources": source_states,
            "formal_kpi_state": formal_kpi_state,
            "kpi_definition_count": definition_count,
            "kpi_snapshot_count": None if snapshots is None else len(snapshots),
            "automatic_kpi_promotion": False,
            "catalog_authority": discovery.get("catalog_authority") or "elo_aprendizado_fontes",
            "read_only": True,
        }
        context["indicator_context"] = indicator_context
        context.setdefault("provenance", {})["indicator_catalog_authority"] = indicator_context[
            "catalog_authority"
        ]
        context["provenance"]["indicator_read_only"] = True
        context["provenance"]["automatic_kpi_promotion"] = False
        return context
