"""Build the ELO resource registry from provider inventory JSON files.

Expected inputs:
- repository-tree.json: {"files": ["path", ...]}
- database-schema.json: {"tables": ["name", ...], "views": ["name", ...]}
- canonical artifact registry: Docs/CANONICAL_KNOWLEDGE_ARTIFACT_ID_REGISTRY_2026-08-19.json
"""

from __future__ import annotations

import json
from pathlib import Path

from src.elo.core.resource_registry_builder import build_registry


def main() -> None:
    root = Path(".elo-inventory")
    repository = json.loads((root / "repository-tree.json").read_text(encoding="utf-8"))
    database = json.loads((root / "database-schema.json").read_text(encoding="utf-8"))\n    canonical = json.loads(Path("Docs/CANONICAL_KNOWLEDGE_ARTIFACT_ID_REGISTRY_2026-08-19.json").read_text(encoding="utf-8"))

    registry = build_registry(
        repository_files=repository.get("files", ()),
        database_tables=database.get("tables", ()),
        database_views=database.get("views", ()),\n        canonical_artifacts=canonical.get("records", ()),
    )

    output = Path("config/elo_resource_registry.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
