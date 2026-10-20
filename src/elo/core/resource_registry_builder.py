"""Build a deterministic resource-address registry from provider inventories.

The builder normalizes inventories already obtained by an authorized provider.
It does not connect to GitHub/Supabase, authorize access, or infer semantics.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Any


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
    canonical_artifacts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    canonical_paths: set[str] = set()

    for artifact in canonical_artifacts:
        artifact_id = str(artifact.get("artifact_id", "")).strip()
        canonical_path = str(artifact.get("canonical_path", "")).strip().replace("\\\\", "/")
        if not artifact_id or not canonical_path:
            continue
        legacy_paths = tuple(
            str(value).strip().replace("\\\\", "/")
            for value in artifact.get("legacy_paths", ())
            if str(value).strip()
        )
        aliases = tuple(dict.fromkeys((str(artifact.get("source_path", "")).strip(), *legacy_paths)))
        aliases = tuple(value for value in aliases if value and value != canonical_path)
        records.append({
            "resource_id": artifact_id,
            "resource_type": "governed_document",
            "provider": "github",
            "logical_name": str(artifact.get("concept_id") or artifact_id),
            "physical_address": canonical_path,
            "canonical": True,
            "status": "ACTIVE" if artifact.get("migration_status") != "RETIRED" else "RETIRED",
            "scope": "repository",
            "authority": str(artifact.get("authority") or "COGNITICO"),
            "provenance": "canonical-artifact-registry",
            **({"aliases": list(aliases)} if aliases else {}),
        })
        canonical_paths.add(canonical_path)

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
        if path in canonical_paths:
            continue
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
