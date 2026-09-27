"""Resolver de contexto por SO.

Dada uma SO (ex: 'SO 155.26'), retorna referências para:
- aprendizado persistido;
- documentos do handbook relevantes;
- precedentes similares;
- índice governado do dossiê SO.

Não cria autoridade paralela.

Refs: ADR-0014, ADR-0015, ELO-SO-DOSSIER-PROTOCOL.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from elo.core.precedent_index import PrecedentIndex

from ..store.memory_store import PrecedentStore
from .so_dossier import SODossier

HANDBOOK_INDEX = Path("04-knowledge-handbook/INDEX.json")
LEARNING_INDEX = Path("memory/solicitations_learning/INDEX.json")
SO_PATTERN = re.compile(r"^SO[\s_-]*(\d{3})[\s_.-]*(\d{2})$")


def normalize_so_id(so_id: str) -> str:
    """Normaliza formas equivalentes para 'SO-NNN.AA'."""
    if not isinstance(so_id, str) or not so_id.strip():
        raise ValueError("so_id is required")
    match = SO_PATTERN.fullmatch(so_id.strip().upper())
    if not match:
        raise ValueError("invalid SO id; expected format SO NNN.AA")
    return f"SO-{match.group(1)}.{match.group(2)}"


def canonical_so_key(so_id: str) -> str:
    """Converte uma SO canônica em chave de armazenamento SO_NNN_AA."""
    normalized = normalize_so_id(so_id)
    number, year = normalized[3:].split(".", 1)
    return f"SO_{number}_{year}"


class SOResolver:
    def __init__(
        self,
        handbook_index: Path = HANDBOOK_INDEX,
        learning_index: Path = LEARNING_INDEX,
        repository_root: Path | None = None,
    ) -> None:
        self.handbook_index = handbook_index
        self.learning_index = learning_index
        self.repository_root = repository_root or Path(".")

    def resolve(
        self,
        so_id: str,
        *,
        tenant_id: str | None = None,
        domain: str | None = None,
    ) -> dict[str, Any]:
        normalized = normalize_so_id(so_id)
        canonical_key = canonical_so_key(normalized)
        learning = self._find_learning(
            normalized,
            tenant_id=tenant_id,
            domain=domain,
        )
        tags = list(learning.get("tags", [])) if learning else []
        handbook = self._find_handbook(tags, domain=domain)
        precedents = self._find_precedents(
            tags,
            tenant_id=tenant_id,
            domain=domain or "orcamento",
        )
        dossier = SODossier.from_resolved_context(
            so_id=normalized,
            canonical_key=canonical_key,
            learning=learning,
            handbook=handbook,
            context_keys=tuple(tags),
            repository_root=self.repository_root,
            tenant_id=tenant_id,
            domain=domain,
        )

        return {
            "so_id": normalized,
            "canonical_key": canonical_key,
            "mask": "SO NNN.AA",
            "tenant_id": tenant_id,
            "domain": domain,
            "learning": learning,
            "handbook": handbook,
            "precedents": precedents,
            "context_keys": tags,
            "dossier": dossier.to_dict(),
        }

    def _find_learning(
        self,
        normalized: str,
        *,
        tenant_id: str | None,
        domain: str | None,
    ) -> dict[str, Any] | None:
        if not self.learning_index.exists():
            return None
        payload = json.loads(self.learning_index.read_text(encoding="utf-8"))
        for entry in payload.get("solicitations", []):
            if not (
                entry.get("canonical_key") == canonical_so_key(normalized)
                or entry.get("so_id") == normalized
            ):
                continue
            if tenant_id is not None and entry.get("tenant_id") not in {
                None, tenant_id
            }:
                continue
            if domain is not None and entry.get("domain") not in {
                None, domain
            }:
                continue
            return entry
        return None

    def _find_handbook(
        self,
        tags: list[str],
        *,
        domain: str | None,
    ) -> list[dict[str, Any]]:
        if not self.handbook_index.exists() or not tags:
            return []
        payload = json.loads(self.handbook_index.read_text(encoding="utf-8"))
        scored = []
        for doc in payload.get("documents", []):
            if domain and doc.get("domain") not in {None, domain}:
                continue
            doc_tags = set(doc.get("tags", []))
            overlap = len(doc_tags & set(tags))
            if overlap > 0:
                scored.append((overlap, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:5]]

    def _find_precedents(
        self,
        tags: list[str],
        *,
        tenant_id: str | None,
        domain: str,
    ) -> list[dict[str, Any]]:
        if not tags:
            return []
        index: PrecedentIndex = PrecedentStore().load()
        results = index.find(
            domain=domain,
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
            if tenant_id is None or getattr(p, "tenant_id", tenant_id) == tenant_id
        ]
