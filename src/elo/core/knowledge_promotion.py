"""Canonical gate for transforming validated learning into reusable knowledge.

This module is deliberately pure: it does not create a second memory store,
write Supabase, commit Git, or bypass the Evolution Gate. It converts an
already validated learning into a canonical promotion decision/package only
when provenance, scope, evidence, duplication, conflict, and the real
Evolution Gate decision are satisfied.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .evolution_gate import EvolutionClassification, EvolutionDecision

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
    evolution_decision: EvolutionDecision | None = None,
    duplicate_found: bool = False,
    conflict_open: bool = False,
    faculty_relevant: bool = False,
) -> KnowledgePromotionDecision:
    """Return a governed promotion package; never persist or mutate state.

    ``evolution_decision`` must be the actual decision returned by the
    canonical ``EvolutionGate``. A caller cannot authorize promotion with an
    independent boolean flag.
    """
    required_text = {"learning_id": learning_id, "knowledge_key": knowledge_key,
                     "title": title, "concept": concept, "scope": scope}
    for name, value in required_text.items():
        if not value or not value.strip():
            return KnowledgePromotionDecision(BLOCKED_STATUS, f"{name}_missing", learning_id, knowledge_key, {})
    if not provenance:
        return KnowledgePromotionDecision(BLOCKED_STATUS, "provenance_missing", learning_id, knowledge_key, {})
    if not 0.0 <= confidence <= 1.0:
        return KnowledgePromotionDecision(BLOCKED_STATUS, "confidence_invalid", learning_id, knowledge_key, {})
    if not evidence_refs:
        return KnowledgePromotionDecision(BLOCKED_STATUS, "evidence_missing", learning_id, knowledge_key, {})
    if duplicate_found:
        return KnowledgePromotionDecision(BLOCKED_STATUS, "duplicate_or_parallel_knowledge", learning_id, knowledge_key, {})
    if conflict_open:
        return KnowledgePromotionDecision(BLOCKED_STATUS, "unresolved_conflict", learning_id, knowledge_key, {})
    if evolution_decision is None:
        return KnowledgePromotionDecision(BLOCKED_STATUS, "evolution_gate_decision_missing", learning_id, knowledge_key, {})
    if evolution_decision.classification is not EvolutionClassification.COMPATIBLE:
        return KnowledgePromotionDecision(
            BLOCKED_STATUS,
            f"evolution_gate_not_compatible:{evolution_decision.classification.value}",
            learning_id, knowledge_key, {},
        )
    if evolution_decision.canonical_mutation_allowed:
        return KnowledgePromotionDecision(BLOCKED_STATUS, "unexpected_gate_mutation_authority", learning_id, knowledge_key, {})

    status = FACULTY_CANDIDATE_STATUS if faculty_relevant else PROMOTABLE_STATUS
    payload = {
        "knowledge_key": knowledge_key.strip(),
        "title": title.strip(),
        "concept": concept.strip(),
        "source_learning_id": learning_id.strip(),
        "provenance": dict(provenance),
        "scope": scope.strip(),
        "evidence_refs": tuple(evidence_refs),
        "confidence": confidence,
        "status": status,
        "promotion": "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE",
        "evolution_gate_classification": evolution_decision.classification.value,
        "evolution_gate_proposal_id": evolution_decision.proposal_id,
    }
    return KnowledgePromotionDecision(status, "eligible_after_all_governance_gates",
                                       learning_id.strip(), knowledge_key.strip(), payload)
