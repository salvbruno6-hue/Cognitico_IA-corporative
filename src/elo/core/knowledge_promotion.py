"""Compatibility boundary for the canonical learning promotion service.

The promotion policy is owned by ``GovernedLearningService``. This module
keeps the established public API while delegating to that single authority;
it does not define a second promotion engine or persistence mechanism.
"""

from __future__ import annotations

from typing import Any, Mapping

from .evolution_gate import EvolutionDecision
from .learning_governance import GovernedLearningService, PromotionPackage

PROMOTABLE_STATUS = "PROMOTABLE_KNOWLEDGE"
BLOCKED_STATUS = "PROMOTION_BLOCKED"
FACULTY_CANDIDATE_STATUS = "FACULTY_CANDIDATE"
KnowledgePromotionDecision = PromotionPackage


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
    """Delegate promotion eligibility to the canonical learning service."""
    return GovernedLearningService.prepare_knowledge_promotion(
        learning_id=learning_id,
        knowledge_key=knowledge_key,
        title=title,
        concept=concept,
        provenance=provenance,
        scope=scope,
        evidence_refs=evidence_refs,
        confidence=confidence,
        evolution_decision=evolution_decision,
        duplicate_found=duplicate_found,
        conflict_open=conflict_open,
        faculty_relevant=faculty_relevant,
    )
