"""Resolver de contexto por SO.

Dada uma SO (ex: 'SO 155.26'), retorna:
- aprendizado persistido
- documentos do handbook relevantes
- precedentes similares

Não cria autoridade paralela. Consulta índices existentes.

Refs: ADR-0014, ADR-0015.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from elo.core.precedent_index import PrecedentIndex

from ..store.memory_store import PrecedentStore

HANDBOOK_INDEX = Path("04-knowledge-handbook/INDEX.json")
LEARNING_INDEX = Path("memory/solicitations_learning/INDEX.json")


def normalize_so_id(so_id: str) -> str:
    """Normaliza 'SO 155.26' -> 'SO-155.26'."""
    cleaned = so_id.strip().upper().replace("_", "-").replace(" ", "-")
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned


class SOResolver:
    def __init__(
        self,
        handbook_index: Path = HANDBOOK_INDEX,
        learning_index: Path = LEARNING_INDEX,
    ) -> None:
        self.handbook_index = handbook_index
        self.learning_index = learning_index

    def resolve(self, so_id: str) -> dict[str, Any]:
        normalized = normalize_so_id(so_id)
        learning = self._find_learning(normalized)
        tags = learning.get("tags", []) if learning else []
        handbook = self._find_handbook(tags)
        precedents = self._find_precedents(tags)

        return {
            "so_id": normalized,
            "learning": learning,
            "handbook": handbook,
            "precedents": precedents,
            "context_keys": tags,
        }

    def _find_learning(self, normalized: str) -> dict[str, Any] | None:
        if not self.learning_index.exists():
            return None
        payload = json.loads(self.learning_index.read_text(encoding="utf-8"))
        for entry in payload.get("solicitations", []):
            if entry.get("canonical_key") == normalized.replace("-", "_"):
                return entry
            if entry.get("so_id") == normalized:
                return entry
        return None

    def _find_handbook(self, tags: list[str]) -> list[dict[str, Any]]:
        if not self.handbook_index.exists() or not tags:
            return []
        payload = json.loads(self.handbook_index.read_text(encoding="utf-8"))
        scored = []
        for doc in payload.get("documents", []):
            doc_tags = set(doc.get("tags", []))
            overlap = len(doc_tags & set(tags))
            if overlap > 0:
                scored.append((overlap, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:5]]

    def _find_precedents(self, tags: list[str]) -> list[dict[str, Any]]:
        if not tags:
            return []
        index: PrecedentIndex = PrecedentStore().load()
        results = index.find(
            domain="orcamento",
            context_keys=tuple(tags),
            limit=5,
        )
        return [
            {
                "decision_id": p.decision_id,
                "domain": p.domain,
                "outcome_summary": p.outcome_summary,
                "context_keys": list(p.context_keys),
            }
            for p in results
        ]
