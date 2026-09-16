"""Controlled memory-context retention experiment on existing ELO capabilities.

This lab evaluates whether compaction-like retention can preserve required
information across a context boundary. It does not add a capability, persist
state, mutate canonical knowledge, or promote learning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.agent_intake.native_capabilities import CAPABILITY_IDS

MEMORY_CAPABILITY_ID = "HERMES-MEMORY"
CONTEXT_CAPABILITY_ID = "HERMES-CONTEXT"


@dataclass(frozen=True, slots=True)
class RetentionEvidence:
    request_id: str
    tenant_scope: str
    memory_capability_id: str
    context_capability_id: str
    retained_ids: tuple[str, ...]
    status: str
    evidence: tuple[dict[str, Any], ...]
    learning_candidate: dict[str, Any]


@dataclass(frozen=True, slots=True)
class RetentionEvaluation:
    baseline_recall: tuple[str, ...]
    adapted_recall: tuple[str, ...]
    baseline_target_hit: bool
    adapted_target_hit: bool
    continuity_preserved: bool
    gain: int
    repeatable: bool
    regression: bool
    learning_candidate: dict[str, Any]


def _tokenize(text: str) -> set[str]:
    return {
        token.strip(".,;:!?()[]{}\"'").lower()
        for token in text.split()
        if token.strip()
    }


def _retain(records: tuple[dict[str, Any], ...], *, tenant_scope: str, keep_ids: tuple[str, ...]) -> tuple[dict[str, Any], ...]:
    return tuple(
        {"id": str(record["id"]), "tenant_scope": tenant_scope, "text": str(record["text"])}
        for record in records
        if record.get("tenant_scope") == tenant_scope and str(record.get("id")) in keep_ids
    )


def _recall(records: tuple[dict[str, Any], ...], query: str, *, tenant_scope: str) -> tuple[str, ...]:
    query_tokens = _tokenize(query)
    scored: list[tuple[int, str]] = []
    for record in records:
        if record.get("tenant_scope") != tenant_scope:
            continue
        record_id = str(record.get("id", ""))
        score = len(query_tokens & _tokenize(str(record.get("text", ""))))
        if record_id and score > 0:
            scored.append((score, record_id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return tuple(record_id for _, record_id in scored)


def evaluate_memory_context_retention(
    *,
    request_id: str,
    tenant_scope: str,
    records: tuple[dict[str, Any], ...],
    required_ids: tuple[str, ...],
    query: str,
    retention_ids: tuple[str, ...],
) -> RetentionEvaluation:
    """Compare recall before and after a deterministic retention boundary."""
    baseline = _recall(records, query, tenant_scope=tenant_scope)
    retained = _retain(records, tenant_scope=tenant_scope, keep_ids=retention_ids)
    adapted = _recall(retained, query, tenant_scope=tenant_scope)

    baseline_hit = all(item in baseline for item in required_ids)
    adapted_hit = all(item in adapted for item in required_ids)
    repeat = _recall(retained, query, tenant_scope=tenant_scope)

    return RetentionEvaluation(
        baseline_recall=baseline,
        adapted_recall=adapted,
        baseline_target_hit=baseline_hit,
        adapted_target_hit=adapted_hit,
        continuity_preserved=adapted_hit,
        gain=int(adapted_hit) - int(baseline_hit),
        repeatable=adapted == repeat,
        regression=baseline_hit and not adapted_hit,
        learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
    )


def retention_evidence(
    *,
    request_id: str,
    tenant_scope: str,
    records: tuple[dict[str, Any], ...],
    required_ids: tuple[str, ...],
    query: str,
    retention_ids: tuple[str, ...],
) -> RetentionEvidence:
    evaluation = evaluate_memory_context_retention(
        request_id=request_id,
        tenant_scope=tenant_scope,
        records=records,
        required_ids=required_ids,
        query=query,
        retention_ids=retention_ids,
    )
    status = "completed" if evaluation.continuity_preserved and evaluation.repeatable and not evaluation.regression else "failed"
    return RetentionEvidence(
        request_id=request_id,
        tenant_scope=tenant_scope,
        memory_capability_id=MEMORY_CAPABILITY_ID,
        context_capability_id=CONTEXT_CAPABILITY_ID,
        retained_ids=tuple(retention_ids),
        status=status,
        evidence=(
            {"baseline_recall": evaluation.baseline_recall},
            {"adapted_recall": evaluation.adapted_recall},
            {"continuity_preserved": evaluation.continuity_preserved},
            {"repeatable": evaluation.repeatable},
            {"regression": evaluation.regression},
        ),
        learning_candidate=evaluation.learning_candidate,
    )


def validate_retention_capability_mapping() -> None:
    """Keep the experiment attached only to the canonical eight capability IDs."""
    assert MEMORY_CAPABILITY_ID in CAPABILITY_IDS
    assert CONTEXT_CAPABILITY_ID in CAPABILITY_IDS
