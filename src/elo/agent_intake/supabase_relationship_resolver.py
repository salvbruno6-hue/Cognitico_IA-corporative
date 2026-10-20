"""Resolve bounded Supabase FK edges into the scan relationship investigator.

This module only transforms already-fetched schema metadata and scoped rows.
It does not connect to Supabase or persist anything.
"""
from __future__ import annotations
from typing import Any, Mapping, Sequence

def resolve_fk_edges(
    foreign_keys: Sequence[Mapping[str, Any]],
    rows_by_table: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    tenant_scope: str = "",
) -> tuple[dict[str, Any], ...]:
    edges: list[dict[str, Any]] = []
    for fk in foreign_keys:
        source_table = str(fk.get("source_table", "")).strip()
        source_column = str(fk.get("source_column", "")).strip()
        target_table = str(fk.get("target_table", "")).strip()
        target_column = str(fk.get("target_column", "")).strip()
        provenance = str(fk.get("constraint_name", "")).strip()
        if not all((source_table, source_column, target_table, target_column, provenance)):
            continue
        targets = {
            str(row.get(target_column)).strip(): row
            for row in rows_by_table.get(target_table, ())
            if row.get(target_column) is not None
        }
        for row in rows_by_table.get(source_table, ()):
            value = row.get(source_column)
            if value is None:
                continue
            target = targets.get(str(value).strip())
            if target is None:
                continue
            source_id = str(row.get("id", row.get(source_column, ""))).strip()
            target_id = str(target.get("id", target.get(target_column, ""))).strip()
            if not source_id or not target_id:
                continue
            edges.append({
                "source": f"{source_table}:{source_id}",
                "target": f"{target_table}:{target_id}",
                "relation_type": "requires",
                "provenance": f"fk:{provenance}",
                "tenant_scope": tenant_scope,
            })
    return tuple(sorted(edges, key=lambda e: (e["source"], e["target"], e["provenance"])))

__all__ = ["resolve_fk_edges"]
