"""Deterministic orchestration for ELO stages 4-6."""
from __future__ import annotations

from typing import Iterable

from .analysis_models import (
    ConsultingAssessment,
    CritiqueResult,
    DecisionSupport,
    EvidenceEvaluation,
    EvidencePolarity,
    Hypothesis,
    InformationGap,
    Scenario,
)


class EvidenceEvaluator:
    def evaluate(self, *, evidence_id: str, claim_id: str, quality: str, relevance: float, supports: bool, rationale: str) -> EvidenceEvaluation:
        polarity = EvidencePolarity.SUPPORTS if supports else EvidencePolarity.CONTRADICTS
        return EvidenceEvaluation(
            evidence_id=evidence_id,
            claim_id=claim_id,
            polarity=polarity,
            quality=quality,
            relevance=max(0.0, min(1.0, relevance)),
            rationale=rationale,
        )


class CritiqueService:
    def critique(self, claim_id: str, evidence: Iterable[EvidenceEvaluation], alternatives: Iterable[str], missing_information: Iterable[str]) -> CritiqueResult:
        evidence_list = list(evidence)
        contradictions = tuple(e.rationale for e in evidence_list if e.claim_id == claim_id and e.polarity is EvidencePolarity.CONTRADICTS)
        support = [e.relevance for e in evidence_list if e.claim_id == claim_id and e.polarity is EvidencePolarity.SUPPORTS]
        contra = [e.relevance for e in evidence_list if e.claim_id == claim_id and e.polarity is EvidencePolarity.CONTRADICTS]
        revised = sum(support) / max(1, len(support)) if support else 0.0
        if contra:
            revised = max(0.0, revised - (sum(contra) / len(contra)))
        return CritiqueResult(
            target_claim_id=claim_id,
            contradictions=contradictions,
            alternatives=tuple(alternatives),
            missing_information=tuple(missing_information),
            revised_confidence=max(0.0, min(1.0, revised)),
        )


class DecisionSupportService:
    def build(self, *, decision_id: str, problem: str, scenarios: Iterable[Scenario], recommended_option: str | None, rationale: str, decision_owner: str | None, evidence_refs: Iterable[str], risks: Iterable[str]) -> DecisionSupport:
        options = tuple(scenarios)
        return DecisionSupport(
            decision_id=decision_id,
            problem=problem,
            alternatives=options,
            recommended_option=recommended_option,
            rationale=rationale,
            decision_owner=decision_owner,
            evidence_refs=tuple(evidence_refs),
            risks=tuple(risks),
        )


class ConsultingService:
    def assess(self, *, assessment_id: str, problem: str, known: Iterable[str], unknown: Iterable[str], hypotheses: Iterable[Hypothesis], information_gaps: Iterable[InformationGap], recommendations: Iterable[str], risks: Iterable[str]) -> ConsultingAssessment:
        return ConsultingAssessment(
            assessment_id=assessment_id,
            problem=problem,
            known=tuple(known),
            unknown=tuple(unknown),
            hypotheses=tuple(hypotheses),
            information_gaps=tuple(information_gaps),
            recommendations=tuple(recommendations),
            risks=tuple(risks),
        )
