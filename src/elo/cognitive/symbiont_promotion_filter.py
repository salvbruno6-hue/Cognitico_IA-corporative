"""Symbiont promotion recommendation filter.

The Symbiont may recommend PROMOTE, STRENGTHEN, REUSE or BLOCK, but never
promotes canonical knowledge itself. Canonical eligibility remains owned by
Evolution Gate + GovernedLearningService + the existing human approval path.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping

from elo.cognitive.symbionte_lab import SymbiontLabEvaluation
from elo.core.evolution_gate import EvolutionClassification, EvolutionDecision
from elo.core.learning_governance import GovernedLearningService, LearningCandidate, PromotionPackage


class PromotionRecommendation(StrEnum):
    PROMOTE = "PROMOTE"
    STRENGTHEN = "STRENGTHEN"
    REUSE = "REUSE"
    BLOCK = "BLOCK"


@dataclass(frozen=True, slots=True)
class SymbiontPromotionAssessment:
    recommendation: PromotionRecommendation
    rationale: str
    evidence_ids: tuple[str, ...]
    canonical_mutation_allowed: bool = False


@dataclass(frozen=True, slots=True)
class SymbiontPromotionResult:
    assessment: SymbiontPromotionAssessment
    package: PromotionPackage | None


class SymbiontPromotionFilter:
    """Non-authoritative filter between laboratory evidence and promotion eligibility."""

    @staticmethod
    def assess(evaluation: SymbiontLabEvaluation) -> SymbiontPromotionAssessment:
        obs = evaluation.observation
        classification = evaluation.evolution_classification
        evidence = tuple(obs.evidence_ids)

        if classification == EvolutionClassification.DUPLICATE_SUPERSEDED.value or evaluation.disposition == "REUSE":
            return SymbiontPromotionAssessment(
                PromotionRecommendation.REUSE,
                "existing canonical owner/concept should be reused instead of creating parallel knowledge",
                evidence,
            )

        if classification in {
            EvolutionClassification.EVOLUTIONARY_CONFLICT.value,
            EvolutionClassification.INCOMPATIBLE.value,
        } or evaluation.disposition == "BLOCK":
            return SymbiontPromotionAssessment(
                PromotionRecommendation.BLOCK,
                "evolution or governance conflict blocks promotion recommendation",
                evidence,
            )

        if evaluation.candidate is None:
            return SymbiontPromotionAssessment(
                PromotionRecommendation.STRENGTHEN,
                "no governed learning candidate is available yet",
                evidence,
            )

        if classification == EvolutionClassification.ADAPT_REQUIRED.value:
            return SymbiontPromotionAssessment(
                PromotionRecommendation.STRENGTHEN,
                "Evolution Gate requires stronger evidence or maturity before promotion",
                evidence,
            )

        if obs.regression_status.upper() in {"REGRESSION", "FAIL"}:
            return SymbiontPromotionAssessment(
                PromotionRecommendation.BLOCK,
                "regression evidence blocks promotion recommendation",
                evidence,
            )

        if obs.generalization_status.upper() != "CONFIRMED":
            return SymbiontPromotionAssessment(
                PromotionRecommendation.STRENGTHEN,
                "generalization must be confirmed before Symbiont recommends promotion",
                evidence,
            )

        if obs.risk.upper() in {"HIGH", "CRITICAL", "ALTO", "CRITICO"}:
            return SymbiontPromotionAssessment(
                PromotionRecommendation.STRENGTHEN,
                "high or critical risk requires stronger validation before promotion",
                evidence,
            )

        if classification != EvolutionClassification.COMPATIBLE.value:
            return SymbiontPromotionAssessment(
                PromotionRecommendation.STRENGTHEN,
                "promotion requires a COMPATIBLE Evolution Gate classification",
                evidence,
            )

        return SymbiontPromotionAssessment(
            PromotionRecommendation.PROMOTE,
            "evidence, generalization, risk and Evolution Gate state support promotion eligibility review",
            evidence,
        )

    @classmethod
    def prepare_promotion(
        cls,
        evaluation: SymbiontLabEvaluation,
        *,
        evolution_decision: EvolutionDecision,
        approved_candidate: LearningCandidate,
        knowledge_key: str,
        title: str,
        concept: str,
        provenance: Mapping[str, Any],
        scope: str,
        confidence: float,
        faculty_relevant: bool = False,
        duplicate_found: bool = False,
        conflict_open: bool = False,
    ) -> SymbiontPromotionResult:
        """Pass PROMOTE recommendations into existing governed promotion eligibility.

        This function does not approve a candidate, write canonical knowledge, or mutate Git/Supabase.
        The supplied candidate must already be APPROVED through GovernedLearningService.
        """
        assessment = cls.assess(evaluation)
        if assessment.recommendation is not PromotionRecommendation.PROMOTE:
            return SymbiontPromotionResult(assessment=assessment, package=None)

        if evaluation.candidate is None or evaluation.candidate.candidate_id != approved_candidate.candidate_id:
            return SymbiontPromotionResult(
                assessment=SymbiontPromotionAssessment(
                    PromotionRecommendation.BLOCK,
                    "approved candidate does not match the candidate evaluated by Symbiont",
                    assessment.evidence_ids,
                ),
                package=None,
            )

        package = GovernedLearningService.prepare_knowledge_promotion(
            learning_id=approved_candidate.candidate_id,
            knowledge_key=knowledge_key,
            title=title,
            concept=concept,
            provenance=provenance,
            scope=scope,
            evidence_refs=assessment.evidence_ids,
            confidence=confidence,
            evolution_decision=evolution_decision,
            duplicate_found=duplicate_found,
            conflict_open=conflict_open,
            faculty_relevant=faculty_relevant,
            learning_candidate=approved_candidate,
        )
        return SymbiontPromotionResult(assessment=assessment, package=package)


__all__ = [
    "PromotionRecommendation",
    "SymbiontPromotionAssessment",
    "SymbiontPromotionFilter",
    "SymbiontPromotionResult",
]
