"""Read-only bridge between ELO knowledge routing and Supabase Elo-forge.

The adapter is deliberately infrastructure-only: it does not learn, promote,
write, migrate, or decide. It retrieves current Forge records and follows the
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


ALLOWED_TABLES = frozenset(
    {
        "taxonomia",
        "dimensoes",
        "modelos",
        "modelo_apresentacao",
        "kits",
        "kit_itens",
        "lista_mae",
        "estrutura_modular",
        "estrutura_modular_itens",
    }
)

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
        if table not in ALLOWED_TABLES:
            raise ForgeRetrievalError(f"table_not_allowed: {table}")
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

    def resolve_model(self, reference: str) -> dict[str, Any]:
        """Resolve aliases to canonical model identity without duplicating data."""
        code = self.canonical_model_code(reference)
        rows = self.read_table("modelos", filters={"codigo": f"eq.{code}"}, limit=2)
        if len(rows) != 1:
            raise ForgeRetrievalError(
                f"model_resolution_not_unique: {reference} -> {code} ({len(rows)} rows)"
            )
        return rows[0]

    def model_context(self, reference: str) -> dict[str, Any]:
        """Retrieve the canonical model and its existing Forge relationships."""
        model = self.resolve_model(reference)
        model_id = model["id"]

        result: dict[str, Any] = {
            "source": "supabase_elo_forge",
            "project_ref": self.config.project_ref,
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

        kit_items: list[dict[str, Any]] = []
        lista_mae: list[dict[str, Any]] = []
        for kit in kits:
            items = self.read_table(
                "kit_itens", filters={"kit_id": f"eq.{kit['id']}"}
            )
            kit_items.extend(items)
            for item in items:
                lista_id = item.get("lista_mae_id")
                if lista_id:
                    lista_mae.extend(
                        self.read_table(
                            "lista_mae", filters={"id": f"eq.{lista_id}"}, limit=1
                        )
                    )
        result["relationships"]["kit_itens"] = kit_items
        result["relationships"]["lista_mae"] = lista_mae

        structures = self.read_table(
            "estrutura_modular", filters={"modelo_id": f"eq.{model_id}"}
        )
        result["relationships"]["estrutura_modular"] = structures

        structure_items: list[dict[str, Any]] = []
        for structure in structures:
            structure_items.extend(
                self.read_table(
                    "estrutura_modular_itens",
                    filters={"estrutura_modular_id": f"eq.{structure['id']}"},
                )
            )
        result["relationships"]["estrutura_modular_itens"] = structure_items
        return result
