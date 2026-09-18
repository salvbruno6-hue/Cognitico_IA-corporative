"""Build a deterministic resource-address registry from provider inventories.

The builder normalizes inventories already obtained by an authorized provider.
It does not connect to GitHub/Supabase, authorize access, or infer semantics.
"""

from __future__ import annotations

from typing import Iterable, Any


# Explicit, governed aliases only. Generic fuzzy matching remains prohibited.
DATABASE_ALIASES: dict[str, tuple[str, ...]] = {
    "excedentes": ("tabela excedente", "tabela excedentes", "excedente"),
    "lista_mae": ("lista mãe", "lista mae", "lista master"),
    "fornecedores": ("tabela fornecedor", "tabela fornecedores", "fornecedor"),
    "fornecedor_itens_cotacao": ("itens de cotação", "itens cotação fornecedor"),
    "mt_lotes_estoque": ("lotes estoque", "estoque lotes", "almoxarifado lotes"),
    "mt_movimentacoes_estoque": (
        "movimentações estoque",
        "movimentacoes estoque",
        "movimentações almoxarifado",
        "movimentacoes almoxarifado",
    ),
}


def build_registry(
    *,
    repository_files: Iterable[str] = (),
    database_tables: Iterable[str] = (),
    database_views: Iterable[str] = (),
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []

    normalized_files = sorted(
        {
            path.strip().replace("\\", "/")
            for path in repository_files
            if path and path.strip()
        }
    )

    # Directories are derived from the authoritative Git tree, so ELO can
    # navigate to a known folder without recursively scanning the repository.
    directories: set[str] = set()
    for path in normalized_files:
        parts = path.split("/")[:-1]
        for index in range(1, len(parts) + 1):
            directories.add("/".join(parts[:index]))

    for directory in sorted(directories):
        records.append(
            {
                "resource_id": f"ELO.REPO.DIR.{_slug(directory)}",
                "resource_type": "repository_directory",
                "provider": "github",
                "logical_name": directory,
                "physical_address": directory,
                "canonical": True,
                "status": "ACTIVE",
                "scope": "repository",
                "authority": "COGNITICO",
                "provenance": "git-tree-derived",
            }
        )

    for path in normalized_files:
        records.append(
            {
                "resource_id": f"ELO.REPO.{_slug(path)}",
                "resource_type": "repository_file",
                "provider": "github",
                "logical_name": path.rsplit("/", 1)[-1],
                "physical_address": path,
                "canonical": True,
                "status": "ACTIVE",
                "scope": "repository",
                "authority": "COGNITICO",
                "provenance": "git-tree",
            }
        )

    for table in sorted({value.strip() for value in database_tables if value and value.strip()}):
        aliases = DATABASE_ALIASES.get(table, ())
        records.append(
            {
                "resource_id": f"ELO.DB.TABLE.{_slug(table)}",
                "resource_type": "database_table",
                "provider": "supabase",
                "logical_name": table,
                "physical_address": f"public.{table}",
                "canonical": True,
                "status": "ACTIVE",
                "scope": "database",
                "authority": "ELO-FORGE",
                "provenance": "information-schema",
                **({"aliases": list(aliases)} if aliases else {}),
            }
        )

    for view in sorted({value.strip() for value in database_views if value and value.strip()}):
        records.append(
            {
                "resource_id": f"ELO.DB.VIEW.{_slug(view)}",
                "resource_type": "database_view",
                "provider": "supabase",
                "logical_name": view,
                "physical_address": f"public.{view}",
                "canonical": True,
                "status": "ACTIVE",
                "scope": "database",
                "authority": "ELO-FORGE",
                "provenance": "information-schema",
            }
        )

    return {"schema_version": "1.1", "records": records}


def _slug(value: str) -> str:
    return "".join(ch.upper() if ch.isalnum() else "_" for ch in value).strip("_")
