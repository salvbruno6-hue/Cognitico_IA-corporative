"""Build a deterministic resource-address registry from provider inventories.

The builder normalizes inventories already obtained by an authorized provider.
It does not connect to GitHub/Supabase, authorize access, or infer semantics.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Any


def build_registry(
    *,
    repository_files: Iterable[str] = (),
    database_tables: Iterable[str] = (),
    database_views: Iterable[str] = (),
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []

    for path in sorted(set(repository_files)):
        normalized = path.strip().replace("\\", "/")
        if not normalized:
            continue
        records.append(
            {
                "resource_id": f"ELO.REPO.{_slug(normalized)}",
                "resource_type": "repository_file",
                "provider": "github",
                "logical_name": normalized.rsplit("/", 1)[-1],
                "physical_address": normalized,
                "canonical": True,
                "status": "ACTIVE",
                "scope": "repository",
                "authority": "COGNITICO",
                "provenance": "git-tree",
            }
        )

    for table in sorted(set(database_tables)):
        normalized = table.strip()
        if not normalized:
            continue
        records.append(
            {
                "resource_id": f"ELO.DB.TABLE.{_slug(normalized)}",
                "resource_type": "database_table",
                "provider": "supabase",
                "logical_name": normalized,
                "physical_address": f"public.{normalized}",
                "canonical": True,
                "status": "ACTIVE",
                "scope": "database",
                "authority": "ELO-FORGE",
                "provenance": "information-schema",
            }
        )

    for view in sorted(set(database_views)):
        normalized = view.strip()
        if not normalized:
            continue
        records.append(
            {
                "resource_id": f"ELO.DB.VIEW.{_slug(normalized)}",
                "resource_type": "database_view",
                "provider": "supabase",
                "logical_name": normalized,
                "physical_address": f"public.{normalized}",
                "canonical": True,
                "status": "ACTIVE",
                "scope": "database",
                "authority": "ELO-FORGE",
                "provenance": "information-schema",
            }
        )

    return {"schema_version": "1.0", "records": records}


def _slug(value: str) -> str:
    return "".join(ch.upper() if ch.isalnum() else "_" for ch in value).strip("_")
