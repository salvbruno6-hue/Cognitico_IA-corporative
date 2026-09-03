"""Canonical gate for transforming validated learning into reusable knowledge.

This module is deliberately pure: it does not create a second memory store,
write Supabase, commit Git, or bypass the Evolution Gate. It converts an
already validated learning into a canonical promotion decision/package only
when provenance, scope, evidence, duplication, conflict, and evolution-gate
conditions are satisfied.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


PROMOTABLE_STATUS = "PROMOTABLE_KNOWLEDGE"
BLOCKED_STATUS = "PROMOTION_BLOCKED"
FACULTY_CANDIDATE_STATUS = "FACULTY_CANDIDATE"


@dataclass(frozen=True)
class KnowledgePromotionDecision:
    status: str
    reason: str
    source_learning_id: str
    knowledge_key: str
    payload: Mapping[str, Any]


def promote_validated_learning(
    *,
    learning_id: str,
    knowledge_key: str,
    title: str,
    concept: str,
    provenance: Mapping[str, Any],
    scope: str,
    evidence_refs: tuple[str, ...] | list[str],
    confidence: float,
    duplicate_found: bool = False,
    conflict_open: bool = False,
    evolution_gate_approved: bool = False,
    faculty_relevant: bool = False,
) -> KnowledgePromotionDecision:
    """Return the only canonical promotion outcome allowed by governance.

    No side effect occurs here. Persistence/commit remains downstream and must
    use the existing canonical Git destination and Evolution Gate.
    """
    required_text = {
        "learning_id": learning_id,
        "knowledge_key": knowledge_key,
        "title": title,
        "concept": concept,
        "scope": scope,
    }
    for name, value in required_text.items():
        if not value or not value.strip():
            return KnowledgePromotionDecision(
                BLOCKED_STATUS,
                f"{name}_missing",
                learning_id,
                knowledge_key,
                {},
            )

    if not provenance:
        return KnowledgePromotionDecision(
            BLOCKED_STATUS, "provenance_missing", learning_id, knowledge_key, {}
        )
    if not 0.0 <= confidence <= 1.0:
        return KnowledgePromotionDecision(
            BLOCKED_STATUS, "confidence_invalid", learning_id, knowledge_key, {}
        )
    if not evidence_refs:
        return KnowledgePromotionDecision(
            BLOCKED_STATUS, "evidence_missing", learning_id, knowledge_key, {}
        )
    if duplicate_found:
        return KnowledgePromotionDecision(
            BLOCKED_STATUS, "duplicate_or_parallel_knowledge", learning_id, knowledge_key, {}
        )
    if conflict_open:
        return KnowledgePromotionDecision(
            BLOCKED_STATUS, "unresolved_conflict", learning_id, knowledge_key, {}
        )
    if not evolution_gate_approved:
        return KnowledgePromotionDecision(
            BLOCKED_STATUS, "evolution_gate_not_approved", learning_id, knowledge_key, {}
        )

    status = FACULTY_CANDIDATE_STATUS if faculty_relevant else PROMOTABLE_STATUS
    payload = {
        "knowledge_key": knowledge_key,
        "title": title.strip(),
        "concept": concept.strip(),
        "source_learning_id": learning_id.strip(),
        "provenance": dict(provenance),
        "scope": scope.strip(),
        "evidence_refs": tuple(evidence_refs),
        "confidence": confidence,
        "status": status,
        "promotion": "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE",
    }
    return KnowledgePromotionDecision(
        status,
        "eligible_after_all_governance_gates",
        learning_id.strip(),
        knowledge_key.strip(),
        payload,
    )
