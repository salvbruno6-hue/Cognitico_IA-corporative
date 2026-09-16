"""Controlled semantic-recall mechanism attached to the existing ELO Memory capability."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CAPABILITY_ID = "HERMES-MEMORY"

# Bounded vocabulary for the laboratory adaptation experiment only.
CONTROLLED_ALIASES = {
    "recall": "retrieval",
    "retrieve": "retrieval",
    "retention": "memory",
    "remembering": "memory",
}


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


@dataclass(frozen=True, slots=True)
class SemanticRecallEvaluation:
    capability_id: str
    baseline_matches: tuple[str, ...]
    adapted_matches: tuple[str, ...]
    baseline_count: int
    adapted_count: int
    gain: int
    repeatable: bool
    regression: bool
    learning_candidate: dict[str, Any]


def _tokens(text: str) -> set[str]:
    return {token.strip(".,;:!?()[]{}\"'").lower() for token in text.split() if token.strip()}


def _adapted_tokens(text: str) -> set[str]:
    return {CONTROLLED_ALIASES.get(token, token) for token in _tokens(text)}


def _rank(*, tenant_scope: str, query: str, records: tuple[dict[str, Any], ...], adapted: bool, top_k: int) -> tuple[str, ...]:
    query_tokens = _adapted_tokens(query) if adapted else _tokens(query)
    scored: list[tuple[int, str]] = []
    for record in records:
        if record.get("tenant_scope") != tenant_scope:
            continue
        record_id = str(record.get("id", ""))
        text = str(record.get("text", ""))
        record_tokens = _adapted_tokens(text) if adapted else _tokens(text)
        score = len(query_tokens & record_tokens)
        if record_id and score > 0:
            scored.append((score, record_id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return tuple(record_id for _, record_id in scored[:top_k])


def semantic_recall(*, request_id: str, tenant_scope: str, query: str, records: tuple[dict[str, Any], ...], top_k: int = 3) -> SemanticRecallEvidence:
    """Rank deterministic lexical relevance inside supplied tenant-scoped records."""
    if not tenant_scope.strip() or not query.strip():
        raise ValueError("tenant_scope and query are required")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    matched_ids = _rank(tenant_scope=tenant_scope, query=query, records=records, adapted=False, top_k=top_k)
    passed = bool(matched_ids)
    return SemanticRecallEvidence(
        capability_id=CAPABILITY_ID,
        request_id=request_id,
        tenant_scope=tenant_scope,
        query=query,
        matched_ids=matched_ids,
        status="completed" if passed else "no_match",
        evidence=(
            {"operation": "tenant_scoped_recall", "candidate_count": len(matched_ids)},
            {"ranking": [{"id": record_id} for record_id in matched_ids]},
        ),
        learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
    )


def evaluate_semantic_recall_adaptation(*, tenant_scope: str, query: str, records: tuple[dict[str, Any], ...], top_k: int = 3) -> SemanticRecallEvaluation:
    """Compare baseline lexical retrieval with a bounded, deterministic adaptation."""
    if not tenant_scope.strip() or not query.strip():
        raise ValueError("tenant_scope and query are required")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    baseline = _rank(tenant_scope=tenant_scope, query=query, records=records, adapted=False, top_k=top_k)
    adapted = _rank(tenant_scope=tenant_scope, query=query, records=records, adapted=True, top_k=top_k)
    repeat = _rank(tenant_scope=tenant_scope, query=query, records=records, adapted=True, top_k=top_k)
    return SemanticRecallEvaluation(
        capability_id=CAPABILITY_ID,
        baseline_matches=baseline,
        adapted_matches=adapted,
        baseline_count=len(baseline),
        adapted_count=len(adapted),
        gain=len(adapted) - len(baseline),
        repeatable=adapted == repeat,
        regression=not set(baseline).issubset(set(adapted)),
        learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
    )


__all__ = ["CAPABILITY_ID", "CONTROLLED_ALIASES", "SemanticRecallEvidence", "SemanticRecallEvaluation", "evaluate_semantic_recall_adaptation", "semantic_recall"]
