"""Read-only governed bridge between ELO knowledge routing and Supabase Elo-forge.

The Forge source registry is the only runtime allowlist. Source selection is
derived from registry metadata and the user question; this adapter never
learns, promotes, writes, or creates a second source authority.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from elo.evidence import Evidence, EvidenceRepository


SOURCE_REGISTRY_TABLE = "elo_aprendizado_fontes"
_MODEL_RE = re.compile(r"\b(?:MLT\.)?M\d{2}\b", re.IGNORECASE)


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
    """Read-only PostgREST adapter with registry-governed source selection."""

    def __init__(
        self,
        config: ForgeConfig | None = None,
        timeout: float = 15.0,
    ):
        self.config = config or ForgeConfig.from_environment()
        self.timeout = timeout

    @staticmethod
    def canonical_model_code(reference: str) -> str:
        normalized = reference.strip().upper()
        return normalized[4:] if normalized.startswith("MLT.") else normalized

    def _read_table_unchecked(
        self,
        table: str,
        *,
        filters: dict[str, str] | None = None,
        limit: int = 100,
        order_by: str | None = None,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        if not 1 <= limit <= 500:
            raise ForgeRetrievalError("limit_out_of_range")
        if offset < 0:
            raise ForgeRetrievalError("offset_out_of_range")

        params: list[tuple[str, str]] = [("select", "*")]
        for column, expression in (filters or {}).items():
            if not column.replace("_", "").isalnum() or not column[0].isalpha():
                raise ForgeRetrievalError(f"invalid_filter_column: {column}")
            params.append((column, expression))
        if order_by:
            if not order_by.replace("_", "").isalnum() or not order_by[0].isalpha():
                raise ForgeRetrievalError("invalid_order_column")
            params.append(("order", f"{order_by}.asc"))
        params.extend([("limit", str(limit)), ("offset", str(offset))])

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

    def discover_sources(self) -> list[dict[str, Any]]:
        """Read the canonical Forge source registry; never creates a catalog."""
        rows = self._read_table_unchecked(
            SOURCE_REGISTRY_TABLE,
            limit=200,
            order_by="prioridade",
        )
        return [
            row
            for row in rows
            if bool(row.get("enabled")) and bool(row.get("extracao_ativa"))
        ]

    def _governed_source(self, table: str) -> dict[str, Any] | None:
        for source in self.discover_sources():
            if source.get("schema_name") == "public" and source.get("table_name") == table:
                return source
        return None

    def read_table(
        self,
        table: str,
        *,
        filters: dict[str, str] | None = None,
        limit: int = 100,
        order_by: str | None = None,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Read only a table currently enabled by elo_aprendizado_fontes."""
        if table != SOURCE_REGISTRY_TABLE and self._governed_source(table) is None:
            raise ForgeRetrievalError(f"table_not_governed: {table}")
        return self._read_table_unchecked(
            table,
            filters=filters,
            limit=limit,
            order_by=order_by,
            offset=offset,
        )

    @staticmethod
    def _tokens(text: str) -> set[str]:
        normalized = re.sub(r"[^a-z0-9_]+", " ", text.lower())
        return {token for token in normalized.split() if len(token) >= 3}

    def select_sources(
        self,
        question: str,
        *,
        entity_code: str | None = None,
        max_sources: int = 12,
    ) -> list[dict[str, Any]]:
        """Select governed sources from registry metadata, not a hardcoded allowlist."""
        if max_sources < 1:
            raise ValueError("max_sources must be positive")

        question_tokens = self._tokens(question)
        entity = self.canonical_model_code(entity_code) if entity_code else None
        selected: list[tuple[int, int, dict[str, Any]]] = []

        for source in self.discover_sources():
            metadata = " ".join(
                [
                    str(source.get("table_name", "")),
                    str(source.get("dominio_codigo", "")),
                    str(source.get("extraction_mode", "")),
                    json.dumps(source.get("regra_extracao") or {}, ensure_ascii=False),
                ]
            )
            metadata_tokens = self._tokens(metadata)
            score = len(question_tokens & metadata_tokens)

            if entity and source.get("dominio_codigo") == "produtos":
                score += 3
            if entity and entity.lower() in metadata.lower():
                score += 2

            if score > 0:
                selected.append(
                    (score, -int(source.get("prioridade") or 999999), source)
                )

        selected.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return [source for _, _, source in selected[:max_sources]]

    def resolve_model(self, reference: str) -> dict[str, Any]:
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
        structure_ids = [row["id"] for row in structures if row.get("id")]
        result["relationships"]["estrutura_modular_itens"] = (
            self.read_table(
                "estrutura_modular_itens",
                filters={"estrutura_modular_id": f"in.({','.join(structure_ids)})"},
            )
            if structure_ids
            else []
        )
        return result

    @staticmethod
    def _row_matches_entity(row: dict[str, Any], entity_code: str) -> bool:
        text = json.dumps(row, ensure_ascii=False).lower()
        return entity_code.lower() in text or f"mlt.{entity_code.lower()}" in text

    def _scan_for_entity(
        self,
        table: str,
        entity_code: str,
        *,
        page_size: int = 100,
        max_pages: int = 5,
    ) -> tuple[list[dict[str, Any]], int]:
        matches: list[dict[str, Any]] = []
        offset = 0
        scanned = 0
        for _ in range(max_pages):
            rows = self.read_table(table, limit=page_size, offset=offset)
            scanned += len(rows)
            matches.extend(
                row for row in rows if self._row_matches_entity(row, entity_code)
            )
            if len(rows) < page_size:
                break
            offset += page_size
        return matches, scanned

    def gather_evidence(
        self,
        *,
        question: str,
        tenant_id: str,
        repository: EvidenceRepository,
        entity_code: str | None = None,
    ) -> dict[str, Any]:
        """Discover, select, read and convert Forge observations into evidence."""
        entity = self.canonical_model_code(entity_code) if entity_code else None
        selected = self.select_sources(
            question,
            entity_code=entity,
        )
        evidence: list[Evidence] = []
        absences: list[Evidence] = []
        conflicts: list[dict[str, Any]] = []
        source_results: list[dict[str, Any]] = []

        if entity:
            model_context = self.model_context(entity)
            source_results.append(
                {
                    "table": "modelos",
                    "mode": "relational_context",
                    "records": 1,
                }
            )
            model = model_context["model"]
            evidence.append(
                Evidence.from_forge(
                    tenant_id=tenant_id,
                    source_table="modelos",
                    source_record_id=str(model.get("id", "")),
                    source_domain="produtos",
                    source_fields=("codigo", "nome", "ativo"),
                    claim=f"O modelo {model.get('codigo')} é {model.get('nome')} e está ativo={model.get('ativo')}.",
                    value={
                        "codigo": model.get("codigo"),
                        "nome": model.get("nome"),
                        "ativo": model.get("ativo"),
                    },
                )
            )
            for table, rows in model_context["relationships"].items():
                if table not in {source.get("table_name") for source in selected}:
                    continue
                for row in rows[:100]:
                    evidence.append(
                        Evidence.from_forge(
                            tenant_id=tenant_id,
                            source_table=table,
                            source_record_id=str(row.get("id", "")),
                            source_domain=next(
                                (
                                    str(source.get("dominio_codigo"))
                                    for source in selected
                                    if source.get("table_name") == table
                                ),
                                "produtos",
                            ),
                            source_fields=tuple(row.keys()),
                            claim=f"Registro observado em {table} relacionado ao modelo {entity}.",
                            value=row,
                        )
                    )

        handled = {"modelos"}
        for source in selected:
            table = str(source.get("table_name"))
            if table in handled or table == SOURCE_REGISTRY_TABLE:
                continue
            if entity:
                matches, scanned = self._scan_for_entity(table, entity)
                source_results.append(
                    {
                        "table": table,
                        "mode": "entity_scan",
                        "records_scanned": scanned,
                        "matches": len(matches),
                    }
                )
                if matches:
                    for row in matches[:100]:
                        evidence.append(
                            Evidence.from_forge(
                                tenant_id=tenant_id,
                                source_table=table,
                                source_record_id=str(row.get("id", "")),
                                source_domain=str(source.get("dominio_codigo") or ""),
                                source_fields=tuple(row.keys()),
                                claim=f"Registro observado em {table} relacionado a {entity}.",
                                value=row,
                            )
                        )
                else:
                    if scanned:
                        evidence.append(
                            Evidence.from_forge(
                                tenant_id=tenant_id,
                                source_table=table,
                                source_domain=str(source.get("dominio_codigo") or ""),
                                source_fields=(),
                                claim=f"A consulta somente leitura retornou {scanned} registro(s) em {table}; nenhum foi relacionado a {entity} no escopo pesquisado.",
                                value={"records_scanned": scanned},
                                query_scope={"entity_code": entity},
                            )
                        )
                    absence = Evidence.from_forge(
                        tenant_id=tenant_id,
                        source_table=table,
                        source_domain=str(source.get("dominio_codigo") or ""),
                        source_fields=(),
                        claim=f"Nenhum registro correspondente a {entity} foi encontrado em {table} dentro do escopo consultado.",
                        value=None,
                        confidence="observed",
                        absence_type="no_matching_record_found",
                        query_scope={
                            "entity_code": entity,
                            "records_scanned": scanned,
                        },
                    )
                    absences.append(absence)
            else:
                rows = self.read_table(table, limit=20)
                source_results.append(
                    {"table": table, "mode": "bounded_read", "records": len(rows)}
                )
                for row in rows[:20]:
                    evidence.append(
                        Evidence.from_forge(
                            tenant_id=tenant_id,
                            source_table=table,
                            source_record_id=str(row.get("id", "")),
                            source_domain=str(source.get("dominio_codigo") or ""),
                            source_fields=tuple(row.keys()),
                            claim=f"Registro observado em {table}.",
                            value=row,
                        )
                    )

        for item in evidence + absences:
            repository.save(item)

        return {
            "entity_code": entity,
            "selected_sources": [
                {
                    "schema_name": source.get("schema_name"),
                    "table_name": source.get("table_name"),
                    "dominio_codigo": source.get("dominio_codigo"),
                    "prioridade": source.get("prioridade"),
                }
                for source in selected
            ],
            "source_results": source_results,
            "evidence": evidence,
            "absences": absences,
            "conflicts": conflicts,
            "evidence_ids": tuple(item.evidence_id for item in evidence + absences),
        }


__all__ = [
    "ForgeConfig",
    "ForgeRetrievalError",
    "SOURCE_REGISTRY_TABLE",
    "SupabaseEloForge",
]
