"""Deterministic materialization of governed ELO knowledge candidates.

This module is deliberately downstream of GovernedLearningService: it does
not decide eligibility, mutate canonical memory, write Supabase, or merge Git.
It only converts an already eligible PromotionPackage into a safe candidate
artifact payload for the canonical learning destination.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from .learning_governance import PromotionPackage


CANONICAL_LEARNING_PATH = "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/"
_SAFE_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$")


class KnowledgeMaterializationError(ValueError):
    """Raised when a promotion package cannot be safely materialized."""


@dataclass(frozen=True)
class MaterializedKnowledge:
    path: str
    content: str
    source_learning_id: str
    knowledge_key: str


def _safe_key(value: str) -> str:
    key = value.strip()
    if not _SAFE_KEY.fullmatch(key) or ".." in key:
        raise KnowledgeMaterializationError("knowledge_key_invalid")
    return key


def materialize_promotion_package(package: PromotionPackage) -> MaterializedKnowledge:
    """Build a deterministic candidate artifact from an eligible package only."""
    if package.status not in {"PROMOTABLE_KNOWLEDGE", "FACULTY_CANDIDATE"}:
        raise KnowledgeMaterializationError("promotion_package_not_eligible")
    payload: Mapping[str, Any] = package.payload
    required = ("knowledge_key", "title", "concept", "source_learning_id", "provenance",
                "scope", "evidence_refs", "confidence", "evolution_gate_classification",
                "evolution_gate_proposal_id")
    missing = [field for field in required if field not in payload]
    if missing:
        raise KnowledgeMaterializationError("promotion_payload_incomplete:" + ",".join(missing))

    key = _safe_key(str(payload["knowledge_key"]))
    source_id = str(payload["source_learning_id"]).strip()
    if not source_id:
        raise KnowledgeMaterializationError("source_learning_id_missing")
    evidence = [str(item) for item in payload["evidence_refs"]]
    if not evidence:
        raise KnowledgeMaterializationError("evidence_refs_missing")

    document = {
        "schema": "ELO_VALIDATED_LEARNING_KNOWLEDGE_CANDIDATE_V1",
        "status": package.status,
        "knowledge_key": key,
        "title": str(payload["title"]).strip(),
        "concept": str(payload["concept"]).strip(),
        "source_learning_id": source_id,
        "provenance": dict(payload["provenance"]),
        "scope": str(payload["scope"]).strip(),
        "evidence_refs": evidence,
        "confidence": payload["confidence"],
        "evolution_gate": {
            "classification": str(payload["evolution_gate_classification"]),
            "proposal_id": str(payload["evolution_gate_proposal_id"]),
        },
        "promotion": str(payload.get("promotion", "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE")),
        "materialization": {
            "mode": "CANDIDATE_ARTIFACT_ONLY",
            "canonical_destination": CANONICAL_LEARNING_PATH,
            "mutation_authority": False,
        },
    }
    content = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return MaterializedKnowledge(
        path=f"{CANONICAL_LEARNING_PATH}{key}.json",
        content=content,
        source_learning_id=source_id,
        knowledge_key=key,
    )
