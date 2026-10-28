"""Governed readiness assessment for cognitive relation candidates.

This module does not promote or persist canonical relations. It only classifies
whether an evidence-backed relation is ready to enter the existing Symbiont /
Evolution Gate promotion path, reusing the canonical PromotionRecommendation
vocabulary.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.symbiont_promotion_filter import PromotionRecommendation
from elo.core.evolution_gate import EvolutionClassification


@dataclass(frozen=True, slots=True)
class CognitiveRelationCandidate:
    relation_id: str
    evidence_ids: tuple[str, ...]
    confidence: float
    source_exists: bool
    target_exists: bool
    generalization_status: str | None = None
    regression_status: str = "NONE"
    risk: str = "MEDIUM"
    evolution_classification: str | None = None
    governed_candidate_available: bool = False
    duplicate_found: bool = False
    conflict_open: bool = False


@dataclass(frozen=True, slots=True)
class CognitiveRelationReadiness:
    relation_id: str
    recommendation: PromotionRecommendation
    rationale: str
    canonical_mutation_allowed: bool = False


class CognitiveRelationReadinessFilter:
    """Fail-closed preflight for relation candidates.

    PROMOTE here means only "eligible to enter the existing governed promotion
    review". It never writes ``elo_cognitive_relations`` or canonical knowledge.
    """

    @staticmethod
    def assess(candidate: CognitiveRelationCandidate) -> CognitiveRelationReadiness:
        if not candidate.source_exists or not candidate.target_exists:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.BLOCK,
                "source or target no longer exists",
            )

        if candidate.conflict_open:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.BLOCK,
                "open semantic or governance conflict blocks relation promotion",
            )

        if candidate.duplicate_found:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.REUSE,
                "an equivalent canonical relation already exists and should be reused",
            )

        if not candidate.evidence_ids:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.STRENGTHEN,
                "relation requires evidence before governed promotion review",
            )

        if candidate.regression_status.upper() in {"REGRESSION", "FAIL"}:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.BLOCK,
                "regression evidence blocks relation promotion",
            )

        if (candidate.generalization_status or "").upper() != "CONFIRMED":
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.STRENGTHEN,
                "generalization has not been confirmed by the governed learning path",
            )

        if candidate.risk.upper() in {"HIGH", "CRITICAL", "ALTO", "CRITICO"}:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.STRENGTHEN,
                "high or critical risk requires stronger validation",
            )

        if candidate.evolution_classification != EvolutionClassification.COMPATIBLE.value:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.STRENGTHEN,
                "Evolution Gate compatibility is required before promotion review",
            )

        if not candidate.governed_candidate_available:
            return CognitiveRelationReadiness(
                candidate.relation_id,
                PromotionRecommendation.STRENGTHEN,
                "no governed learning candidate is available yet",
            )

        return CognitiveRelationReadiness(
            candidate.relation_id,
            PromotionRecommendation.PROMOTE,
            "relation is eligible for the existing governed promotion review",
        )


__all__ = [
    "CognitiveRelationCandidate",
    "CognitiveRelationReadiness",
    "CognitiveRelationReadinessFilter",
]
