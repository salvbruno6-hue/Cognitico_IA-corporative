"""Controlled semantic-recall mechanism attached to the existing ELO Memory capability.

This laboratory surface evaluates retrieval behavior without introducing a second
memory authority, embeddings service, persistence layer, or canonical mutation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CAPABILITY_ID = "HERMES-MEMORY"


@dataclass(frozen=True, slots=True)
class SemanticRecallEvidence:
    capability_id: str
    request_id: str
    tenant_scope: str
    query: str
    matched_ids: tuple[str, ...]
    status: str
    evidence: tuple[dict[str, Any], ...]
    learning_candidate: dict[str, Any]



def _tokens(text: str) -> set[str]:
    return {token.strip(".,;:!?()[]{}\"'").lower() for token in text.split() if token.strip()}



def semantic_recall(
    *,
    request_id: str,
    tenant_scope: str,
    query: str,
    records: tuple[dict[str, Any], ...],
    top_k: int = 3,
) -> SemanticRecallEvidence:
    """Rank deterministic lexical relevance inside the supplied tenant-scoped records."""
    if not tenant_scope.strip() or not query.strip():
        raise ValueError("tenant_scope and query are required")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    query_tokens = _tokens(query)
    scored: list[tuple[int, str]] = []
    for record in records:
        if record.get("tenant_scope") != tenant_scope:
            continue
        record_id = str(record.get("id", ""))
        text = str(record.get("text", ""))
        score = len(query_tokens & _tokens(text))
        if record_id and score > 0:
            scored.append((score, record_id))

    scored.sort(key=lambda item: (-item[0], item[1]))
    matched_ids = tuple(record_id for _, record_id in scored[:top_k])
    passed = bool(matched_ids)

    return SemanticRecallEvidence(
        capability_id=CAPABILITY_ID,
        request_id=request_id,
        tenant_scope=tenant_scope,
        query=query,
        matched_ids=matched_ids,
        status="completed" if passed else "no_match",
        evidence=(
            {"operation": "tenant_scoped_recall", "candidate_count": len(scored)},
            {"ranking": [{"id": record_id, "score": score} for score, record_id in scored[:top_k]]},
        ),
        learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
    )


__all__ = ["CAPABILITY_ID", "SemanticRecallEvidence", "semantic_recall"]
