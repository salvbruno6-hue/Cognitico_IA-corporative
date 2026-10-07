"""Read-only bridge between ELO knowledge routing and Supabase Elo-forge.

This adapter is infrastructure-only: it does not learn, promote, write,
migrate, or decide. It retrieves current Forge records and follows the
canonical relational chain needed by ELO's cognitive layer.

Required runtime environment:
- SUPABASE_URL (or ELO_FORGE_SUPABASE_URL)
- SUPABASE_SERVICE_ROLE_KEY (or ELO_FORGE_SUPABASE_SERVICE_ROLE_KEY)

The service-role credential must remain server-side and must never be exposed
to a client or committed to the repository.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


CATALOG_TABLE = "elo_aprendizado_fontes"

# The catalog is the sole runtime allow-list.  Concrete tables are never
# admitted by a second static list.
CATALOG_MATCH_TERMS = {
    "produto": {"produtos"},
    "modelo": {"produtos"},
    "módulo": {"produtos"},
    "modulo": {"produtos"},
    "kit": {"produtos"},
    "composição": {"produtos"},
    "composicao": {"produtos"},
    "lista": {"produtos"},
    "produção": {"producao_fluxo_modular"},
    "producao": {"producao_fluxo_modular"},
    "fluxo": {"producao_fluxo_modular"},
    "demanda": {"planejamento_demanda", "planejamento_pcp"},
    "demanda comercial": {"comercial_licitacoes", "planejamento_demanda"},
    "demanda de fabricação": {"planejamento_pcp", "producao_fluxo_modular"},
    "demanda fabricação": {"planejamento_pcp", "producao_fluxo_modular"},
    "demanda de reparos": {"reparos_modulares", "planejamento_pcp"},
    "demanda de operações externas": {"operacoes_externas", "planejamento_pcp"},
    "demanda de operacoes externas": {"operacoes_externas", "planejamento_pcp"},
    "impacto": {"planejamento_pcp", "operacoes_externas", "reparos_modulares", "compras"},
    "impactos": {"planejamento_pcp", "operacoes_externas", "reparos_modulares", "compras"},
    "material": {"planejamento_demanda", "produtos", "compras"},
    "recurso": {"planejamento_pcp"},
    "cobertura": {"planejamento_pcp", "operacoes_externas", "reparos_modulares"},
    "decisão externa": {"operacoes_externas"},
    "decisao externa": {"operacoes_externas"},
    "resumo pcp": {"planejamento_pcp", "operacoes_externas"},
    "dados pendentes": {"planejamento_pcp"},
    "operação externa": {"operacoes_externas"},
    "operacao externa": {"operacoes_externas"},
    "operações externas": {"operacoes_externas"},
    "operacoes externas": {"operacoes_externas"},
    "montagem externa": {"operacoes_externas"},
    "reparo": {"reparos_modulares"},
    "reparos": {"reparos_modulares"},
    "unidade modular": {"reparos_modulares"},
    "unidade": {"reparos_modulares"},
    "fornecedor": {"compras"},
    "cotação": {"compras"},
    "cotacao": {"compras"},
    "custo": {"rh", "compras"},
    "regra": {"gestao"},
    "exceção": {"gestao"},
    "excecao": {"gestao"},
    "proveniência": {"dados_banco"},
    "proveniencia": {"dados_banco"},
}

MODEL_ALIASES = {
    "MLT.M01": "M01",
    "MLT.M02": "M02",
}


class ForgeRetrievalError(RuntimeError):
    """Raised when Forge cannot be queried safely."""


@dataclass(frozen=True)
class ForgeConfig:
    url: str
    service_role_key: str
    project_ref: str = "fxbpevjrkwhbicpmecow"

    @classmethod
    def from_environment(cls) -> "ForgeConfig":
        url = os.getenv("ELO_FORGE_SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = os.getenv("ELO_FORGE_SUPABASE_SERVICE_ROLE_KEY") or os.getenv(
            "SUPABASE_SERVICE_ROLE_KEY"
        )
        if not url or not key:
            raise ForgeRetrievalError(
                "Supabase Forge runtime credentials are not configured"
            )
        return cls(url=url.rstrip("/"), service_role_key=key)


class SupabaseEloForge:
    """Minimal read-only PostgREST adapter for the ELO Forge schema."""

    def __init__(self, config: ForgeConfig | None = None, timeout: float = 15.0):
        self.config = config or ForgeConfig.from_environment()
        self.timeout = timeout

    @staticmethod
    def canonical_model_code(reference: str) -> str:
        normalized = reference.strip().upper()
        return MODEL_ALIASES.get(normalized, normalized)

    def read_table(
        self,
        table: str,
        *,
        filters: dict[str, str] | None = None,
        limit: int = 100,
        order_by: str | None = None,
    ) -> list[dict[str, Any]]:
        if table != CATALOG_TABLE and not self._is_governed_table(table):
            raise ForgeRetrievalError(f"table_not_governed: {table}")
        if not 1 <= limit <= 100:
            raise ForgeRetrievalError("limit_out_of_range")

        params: list[tuple[str, str]] = [("select", "*")]
        for column, expression in (filters or {}).items():
            if not column.replace("_", "").isalnum() or not column[0].isalpha():
                raise ForgeRetrievalError(f"invalid_filter_column: {column}")
            params.append((column, expression))
        if order_by:
            if not order_by.replace("_", "").isalnum() or not order_by[0].isalpha():
                raise ForgeRetrievalError("invalid_order_column")
            params.append(("order", f"{order_by}.asc"))
        params.append(("limit", str(limit)))

        endpoint = f"{self.config.url}/rest/v1/{quote(table, safe='')}"
        request = Request(
            f"{endpoint}?{urlencode(params)}",
            headers={
                "apikey": self.config.service_role_key,
                "Authorization": f"Bearer {self.config.service_role_key}",
                "Accept": "application/json",
            },
            method="GET",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            raise ForgeRetrievalError(f"forge_read_failed: {table}") from exc
        if not isinstance(payload, list):
            raise ForgeRetrievalError(f"forge_invalid_response: {table}")
        return payload

    def _read_raw_table(
        self,
        table: str,
        *,
        filters: dict[str, str] | None = None,
        limit: int = 100,
        order_by: str | None = None,
    ) -> list[dict[str, Any]]:
        """Read a table without applying the governed-source guard."""
        if not 1 <= limit <= 100:
            raise ForgeRetrievalError("limit_out_of_range")
        params: list[tuple[str, str]] = [("select", "*")]
        for column, expression in (filters or {}).items():
            if not column.replace("_", "").isalnum() or not column[0].isalpha():
                raise ForgeRetrievalError(f"invalid_filter_column: {column}")
            params.append((column, expression))
        if order_by:
            if not order_by.replace("_", "").isalnum() or not order_by[0].isalpha():
                raise ForgeRetrievalError("invalid_order_column")
            params.append(("order", f"{order_by}.asc"))
        params.append(("limit", str(limit)))
        endpoint = f"{self.config.url}/rest/v1/{quote(table, safe='')}"
        request = Request(
            f"{endpoint}?{urlencode(params)}",
            headers={
                "apikey": self.config.service_role_key,
                "Authorization": f"Bearer {self.config.service_role_key}",
                "Accept": "application/json",
            },
            method="GET",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            raise ForgeRetrievalError(f"forge_read_failed: {table}") from exc
        if not isinstance(payload, list):
            raise ForgeRetrievalError(f"forge_invalid_response: {table}")
        return payload

    def governed_sources(self) -> list[dict[str, Any]]:
        """Return the active Forge sources from the canonical source catalog."""
        rows = self._read_raw_table(
            CATALOG_TABLE,
            filters={"enabled": "eq.true", "extracao_ativa": "eq.true"},
            limit=100,
            order_by="prioridade",
        )
        sources = []
        for row in rows:
            table = row.get("table_name")
            schema = row.get("schema_name")
            if schema != "public" or not isinstance(table, str) or not table:
                continue
            sources.append(row)
        return sources

    def _is_governed_table(self, table: str) -> bool:
        return any(source.get("table_name") == table for source in self.governed_sources())

    def discover_sources(self, query: str) -> list[dict[str, Any]]:
        """Select governed sources from catalog metadata; never invents a source."""
        normalized = query.casefold()
        sources = self.governed_sources()
        scored: list[tuple[int, int, dict[str, Any]]] = []
        for source in sources:
            domain = str(source.get("dominio_codigo") or "").casefold()
            table = str(source.get("table_name") or "").casefold()
            rule = json.dumps(source.get("regra_extracao") or {}, ensure_ascii=False).casefold()
            score = 0
            for term, domains in CATALOG_MATCH_TERMS.items():
                if term in normalized and any(domain == candidate.casefold() for candidate in domains):
                    score += 4
            if any(token in normalized for token in table.replace("_", " ").split()):
                score += 2
            if domain and domain.replace("_", " ") in normalized:
                score += 2
            if score:
                scored.append((score, int(source.get("prioridade") or 999999), source))
        scored.sort(key=lambda item: (-item[0], item[1], str(item[2].get("table_name"))))
        return [item[2] for item in scored]

    @staticmethod
    def _ids(values: list[Any]) -> list[str]:
        return list(dict.fromkeys(str(value) for value in values if value is not None))

    def governed_demand_context(self, query: str) -> dict[str, Any]:
        """Consult demand and impact sources selected by the canonical catalog.

        This is a read-only cross-domain view. Source selection is dynamic from
        the canonical source catalog; the bounded table set is only a safety
        boundary for globally scoped sources.
        """
        discovered = self.discover_sources(query)
        global_tables = {
            "v_elo_pcp_cobertura_demanda_externa",
            "v_elo_pcp_decisao_externa_detalhe",
            "v_elo_pcp_decisao_externa_resumo",
            "v_elo_pcp_dialogo_regras",
            "fluxo_produtivo_modular",
            "elo_sim_cenarios",
            "elo_sim_demanda",
            "elo_sim_demanda_materiais",
            "elo_sim_demanda_recursos",
            "elo_orcamento_decisoes",
            "elo_orcamento_associacoes",
        }
        linked: dict[str, list[dict[str, Any]]] = {}
        not_scoped: list[dict[str, Any]] = []
        for source in discovered:
            table = str(source.get("table_name") or "")
            if table not in global_tables:
                not_scoped.append({
                    "table_name": table,
                    "dominio_codigo": source.get("dominio_codigo"),
                    "reason": "model_or_entity_scope_required",
                })
                continue
            filters = {"ativo": "eq.true"} if table == "fluxo_produtivo_modular" else None
            linked[table] = self._read_raw_table(table, filters=filters, limit=100)

        demand_rows = linked.get("elo_sim_demanda") or []
        resource_rows = linked.get("elo_sim_demanda_recursos") or []
        decision_rows = linked.get("v_elo_pcp_decisao_externa_resumo") or []
        rule_rows = linked.get("v_elo_pcp_dialogo_regras") or []
        coverage_rows = linked.get("v_elo_pcp_cobertura_demanda_externa") or []

        decision = {}
        if decision_rows:
            row = decision_rows[0]
            decision = {
                "estado_decisao": row.get("estado_decisao"),
                "estado_cobertura_global": row.get("estado_cobertura_global"),
            }

        gap = {}
        if rule_rows:
            row = rule_rows[0]
            gap = {
                "gate": row.get("gate"),
                "gap_codigo": row.get("gap_codigo"),
                "bloqueia_execucao": row.get("bloqueia_execucao"),
                "motivo": row.get("motivo"),
                "authorized_source": row.get("fonte_autorizada"),
            }

        demand_total = sum(float(row.get("quantidade") or 0) for row in demand_rows if row.get("quantidade") is not None)
        resource_hours = sum(float(row.get("horas_demanda_h") or 0) for row in resource_rows if row.get("horas_demanda_h") is not None)

        return {
            "source": "supabase_elo_forge",
            "query": query,
            "scope": "cross_domain_demand_and_impacts",
            "linked_counts": {table: len(rows) for table, rows in linked.items()},
            "demand_total": demand_total,
            "resource_hours": resource_hours,
            "decision": decision,
            "gap": gap,
            "coverage_records": len(coverage_rows),
            "governed_discovery": {
                "sources_considered": [{"table_name": source.get("table_name"), "dominio_codigo": source.get("dominio_codigo"), "prioridade": source.get("prioridade")} for source in discovered],
                "linked_records": linked,
                "not_scoped": not_scoped,
                "catalog_authority": CATALOG_TABLE,
                "learning_performed": False,
                "scope": "cross_domain_demand_and_impacts",
            },
            "provenance": {
                "source": "Supabase Elo-forge",
                "governed_catalog": CATALOG_TABLE,
                "read_only": True,
                "guessed": False,
                "learning_performed": False,
            },
        }
    def governed_model_context(self, reference: str, query: str) -> dict[str, Any]:
        """Retrieve a model and safely extend it through catalog-governed sources."""
        result = self.model_context(reference)
        discovered = self.discover_sources(query)

        model_id = result["entity"]["model_id"]
        relationships = result["relationships"]
        kit_ids = self._ids([row.get("id") for row in relationships.get("kits", [])])
        lista_ids = self._ids([row.get("id") for row in relationships.get("lista_mae", [])])
        item_codes = self._ids([
            row.get("cod_item") or row.get("cod_produt")
            for row in result.get("kit_composition", [])
        ])
        model_code = result["entity"]["canonical_code"]

        linked: dict[str, list[dict[str, Any]]] = {}
        not_linked: list[dict[str, Any]] = []

        governed_table_names = {
            str(source.get("table_name"))
            for source in self.governed_sources()
            if source.get("table_name")
        }

        def read_governed(table: str, **kwargs):
            if table not in governed_table_names:
                raise ForgeRetrievalError(f"table_not_governed: {table}")
            return self._read_raw_table(table, **kwargs)

        def ids_from(rows, key):
            return self._ids([row.get(key) for row in rows])

        external_order_items: list[dict[str, Any]] = []
        repair_units: list[dict[str, Any]] = []

        if any(s.get("table_name") == "mt_ordens_montagem_externa" for s in discovered):
            if "mt_pedidos_venda_itens" in governed_table_names:
                external_order_items = read_governed(
                    "mt_pedidos_venda_itens",
                    filters={"modelo_id": f"eq.{model_id}"},
                    limit=100,
                )
                linked["mt_pedidos_venda_itens"] = external_order_items

        if any(s.get("table_name") in {"mt_unidades_modulares", "mt_ordens_reparo"} for s in discovered):
            if "mt_unidades_modulares" in governed_table_names:
                repair_units = read_governed(
                    "mt_unidades_modulares",
                    filters={"modelo_id": f"eq.{model_id}"},
                    limit=100,
                )
                linked["mt_unidades_modulares"] = repair_units

        for source in discovered:
            table = source["table_name"]
            if table in relationships or table in linked:
                continue
            rows = read_governed(table, limit=25)
            if not rows:
                linked[table] = []
                continue
            keys = set(rows[0].keys())
            filters: dict[str, str] | None = None
            if "modelo_id" in keys:
                filters = {"modelo_id": f"eq.{model_id}"}
            elif "model_id" in keys:
                filters = {"model_id": f"eq.{model_id}"}
            elif table in {"v_elo_pcp_decisao_externa_resumo", "v_elo_pcp_dialogo_regras"}:
                filters = None
            elif table == "mt_ordens_montagem_externa":
                pedido_ids = ids_from(external_order_items, "pedido_venda_id")
                if pedido_ids:
                    filters = {"pedido_venda_id": f"in.({','.join(pedido_ids)})"}
                else:
                    linked[table] = []
                    continue
            elif table == "mt_equipe_montagem_externa":
                order_ids = ids_from(linked.get("mt_ordens_montagem_externa", []), "id")
                if order_ids:
                    filters = {"ordem_montagem_externa_id": f"in.({','.join(order_ids)})"}
                else:
                    linked[table] = []
                    continue
            elif table == "mt_funcoes_montagem":
                function_ids = ids_from(linked.get("mt_equipe_montagem_externa", []), "funcao_montagem_id")
                if function_ids:
                    filters = {"id": f"in.({','.join(function_ids)})"}
                else:
                    linked[table] = []
                    continue
            elif table == "mt_ordens_reparo":
                unit_ids = ids_from(repair_units, "id")
                if unit_ids:
                    filters = {"unidade_modular_id": f"in.({','.join(unit_ids)})"}
                else:
                    linked[table] = []
                    continue
            elif "taxonomia_id" in keys and relationships.get("taxonomia"):
                tax_id = relationships["taxonomia"][0].get("id")
                if tax_id:
                    filters = {"taxonomia_id": f"eq.{tax_id}"}
            elif "lista_mae_id" in keys and lista_ids:
                filters = {"lista_mae_id": f"in.({','.join(lista_ids)})"}
            elif "codigo_item" in keys and item_codes:
                filters = {"codigo_item": f"in.({','.join(item_codes)})"}
            elif table == "fluxo_produtivo_modular" and "ativo" in keys:
                # A flow without modelo_id is a generic reference flow, not an M01 flow.
                filters = {"ativo": "eq.true"}
            else:
                not_linked.append({
                    "table_name": table,
                    "dominio_codigo": source.get("dominio_codigo"),
                    "reason": "no_safe_relationship_to_model",
                })
                continue

            selected = read_governed(table, filters=filters, limit=100)
            linked[table] = selected

            if table == "fluxo_produtivo_modular":
                flow_ids = self._ids([row.get("id") for row in selected])
                if flow_ids:
                    stages_source = next(
                        (s for s in self.governed_sources()
                         if s.get("table_name") == "fluxo_produtivo_modular_etapas"),
                        None,
                    )
                    if stages_source:
                        stages = self._read_raw_table(
                            "fluxo_produtivo_modular_etapas",
                            filters={"fluxo_id": f"in.({','.join(flow_ids)})"},
                            limit=100,
                        )
                        linked["fluxo_produtivo_modular_etapas"] = stages

                # A row with no modelo_id/taxonomia_id is not "unrelated":
                # the canonical PCP/production flow defines a modular family-wide
                # reference. Preserve that scope without attributing the flow
                # exclusively to the requested model.
                scope = []
                for row in selected:
                    if row.get("modelo_id") == model_id:
                        scope.append({
                            "flow_id": row.get("id"),
                            "scope": "model_specific",
                            "model_specific": True,
                        })
                    elif (
                        row.get("modelo_id") is None
                        and row.get("taxonomia_id") is None
                        and row.get("ativo") is True
                    ):
                        scope.append({
                            "flow_id": row.get("id"),
                            "scope": "family_wide_modular",
                            "model_specific": False,
                            "reason": "active_modular_reference_flow",
                        })
                linked["fluxo_produtivo_modular_scope"] = scope

        result["governed_discovery"] = {
            "query": query,
            "sources_considered": [
                {
                    "table_name": source.get("table_name"),
                    "dominio_codigo": source.get("dominio_codigo"),
                    "prioridade": source.get("prioridade"),
                }
                for source in discovered
            ],
            "linked_records": linked,
            "not_linked": not_linked,
            "catalog_authority": CATALOG_TABLE,
            "learning_performed": False,
            "applicability": {
                "fluxo_produtivo_modular": linked.get("fluxo_produtivo_modular_scope", []),
                "operacoes_externas": {
                    "scope": "model_via_pedido_venda",
                    "model_specific": bool(linked.get("mt_ordens_montagem_externa")),
                },
                "reparos_modulares": {
                    "scope": "model_via_unidade_modular",
                    "model_specific": bool(linked.get("mt_ordens_reparo") or linked.get("mt_unidades_modulares")),
                },
            },
        }
        result["provenance"]["governed_catalog"] = CATALOG_TABLE
        result["provenance"]["guessed"] = False
        result["provenance"]["model_code"] = model_code
        return result

    def resolve_model(self, reference: str) -> dict[str, Any]:
        """Resolve aliases to canonical model identity without duplicating data."""
        code = self.canonical_model_code(reference)
        rows = self.read_table("modelos", filters={"codigo": f"eq.{code}"}, limit=2)
        if len(rows) != 1:
            raise ForgeRetrievalError(
                f"model_resolution_not_unique: {reference} -> {code} ({len(rows)} rows)"
            )
        return rows[0]

    @staticmethod
    def present_kit_item(
        kit_item: dict[str, Any], lista_mae: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Return the stable specialist-facing kit columns without inventing data.

        Product code is resolved from the canonical Lista Mãe relationship first,
        then from the kit item when present. A missing value remains None so the
        cognitive layer can explicitly report the catalog gap.
        """
        lista = lista_mae or {}
        quantidade = kit_item.get("quantidade")
        if quantidade is None:
            quantidade = kit_item.get("qtd_uni")
        if quantidade is None:
            quantidade = kit_item.get("quant_total")

        valor_unitario = lista.get("valor_unitario")
        if valor_unitario is None:
            valor_unitario = kit_item.get("valor_unitario")

        valor_total = kit_item.get("valor_total")
        if valor_total is None and valor_unitario is not None and quantidade is not None:
            try:
                valor_total = float(valor_unitario) * float(quantidade)
            except (TypeError, ValueError):
                valor_total = None

        return {
            "codigo_item": kit_item.get("cod_item"),
            "cod_produto": lista.get("cod_produt") or kit_item.get("cod_produt"),
            "descricao": lista.get("descricao_oficial") or kit_item.get("descricao_oficial"),
            "un": lista.get("un") or kit_item.get("un"),
            "qtd": quantidade,
            "valor_unitario": valor_unitario,
            "valor_total": valor_total,
            "lista_mae_id": kit_item.get("lista_mae_id"),
        }

    def model_context(self, reference: str) -> dict[str, Any]:
        """Retrieve the canonical model and its existing Forge relationships."""
        model = self.resolve_model(reference)
        model_id = model["id"]

        result: dict[str, Any] = {
            "source": "supabase_elo_forge",
            "entity": {
                "requested_reference": reference,
                "canonical_code": model["codigo"],
                "model_id": model_id,
            },
            "model": model,
            "relationships": {},
            "provenance": {
                "source": "Supabase Elo-forge",
                "read_only": True,
                "guessed": False,
            },
        }

        taxonomia_id = model.get("taxonomia_id")
        if taxonomia_id:
            result["relationships"]["taxonomia"] = self.read_table(
                "taxonomia", filters={"id": f"eq.{taxonomia_id}"}, limit=1
            )

        dimensao_id = model.get("dimensao_id")
        if dimensao_id:
            result["relationships"]["dimensoes"] = self.read_table(
                "dimensoes", filters={"id": f"eq.{dimensao_id}"}, limit=1
            )

        kits = self.read_table("kits", filters={"modelo_id": f"eq.{model_id}"})
        result["relationships"]["kits"] = kits

        kit_ids = [kit["id"] for kit in kits if kit.get("id")]
        kit_items = (
            self.read_table(
                "kit_itens",
                filters={"kit_id": f"in.({','.join(kit_ids)})"},
            )
            if kit_ids
            else []
        )
        result["relationships"]["kit_itens"] = kit_items

        lista_ids = list(
            dict.fromkeys(
                item["lista_mae_id"]
                for item in kit_items
                if item.get("lista_mae_id")
            )
        )
        lista_mae = (
            self.read_table(
                "lista_mae",
                filters={"id": f"in.({','.join(lista_ids)})"},
            )
            if lista_ids
            else []
        )
        lista_by_id = {row["id"]: row for row in lista_mae if row.get("id")}

        result["relationships"]["lista_mae"] = lista_mae
        result["kit_composition"] = [
            self.present_kit_item(item, lista_by_id.get(item.get("lista_mae_id")))
            for item in kit_items
        ]

        structures = self.read_table(
            "estrutura_modular", filters={"modelo_id": f"eq.{model_id}"}
        )
        result["relationships"]["estrutura_modular"] = structures

        structure_ids = [
            structure["id"] for structure in structures if structure.get("id")
        ]
        structure_items = (
            self.read_table(
                "estrutura_modular_itens",
                filters={"estrutura_modular_id": f"in.({','.join(structure_ids)})"},
            )
            if structure_ids
            else []
        )
        result["relationships"]["estrutura_modular_itens"] = structure_items
        return result
