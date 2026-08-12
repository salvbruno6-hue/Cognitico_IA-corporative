"""Deterministic reasoning and self-critique primitives for ELO-004."""
from __future__ import annotations

from uuid import uuid4

from . import ClaimStatus, CritiqueResult, EvidenceItem, FindingType, ReasoningFinding, ReasoningResult


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


class ReasoningEngine:
    """Produces bounded findings from explicit evidence; it never invents evidence."""

    def reason(self, query: str, *, evidence: list[EvidenceItem], provenance: dict | None = None) -> ReasoningResult:
        if not query.strip():
            raise ValueError("query is required")
        if not evidence:
            finding = ReasoningFinding(
                finding_id=str(uuid4()), statement="Insufficient evidence to establish a finding.",
                finding_type=FindingType.UNKNOWN, status=ClaimStatus.UNVERIFIED, confidence=0.0,
            )
            critique = CritiqueResult(
                critique_id=str(uuid4()), finding_id=finding.finding_id,
                weaknesses=("No evidence was supplied.",),
                missing_evidence=("At least one relevant source or observation.",),
                recommendation="GATHER_EVIDENCE",
            )
            return ReasoningResult(str(uuid4()), query, (finding,), (critique,), 0.0, (), ("What evidence supports the query?",), provenance or {})

        relevant = [item for item in evidence if item.relevance > 0]
        supporting = [item for item in relevant if item.supports]
        contradicting = [item for item in relevant if not item.supports]
        refs = tuple(item.evidence_id for item in relevant)
        support_score = sum(_clamp(item.quality * item.relevance) for item in supporting)
        contradiction_score = sum(_clamp(item.quality * item.relevance) for item in contradicting)
        total = support_score + contradiction_score
        confidence = _clamp((support_score - contradiction_score + 1.0) / 2.0 if total else 0.0)
        if supporting and contradicting:
            status = ClaimStatus.CONTRADICTED if contradiction_score > support_score else ClaimStatus.PARTIALLY_SUPPORTED
        elif supporting:
            status = ClaimStatus.SUPPORTED
        else:
            status = ClaimStatus.UNVERIFIED
        finding = ReasoningFinding(
            finding_id=str(uuid4()), statement=query, finding_type=FindingType.INFERENCE,
            status=status, confidence=confidence, evidence_refs=refs,
            assumptions=("Evidence relevance and quality scores are valid.",),
            contradictions=tuple(item.evidence_id for item in contradicting),
        )
        strengths = tuple(f"Evidence {item.evidence_id} supports the finding." for item in supporting)
        weaknesses = tuple(f"Evidence {item.evidence_id} conflicts with or weakens the finding." for item in contradicting)
        critique = CritiqueResult(
            critique_id=str(uuid4()), finding_id=finding.finding_id,
            strengths=strengths, weaknesses=weaknesses,
            missing_evidence=() if supporting else ("Independent supporting evidence.",),
            alternative_hypotheses=("The observed relationship may have an unmeasured cause.",),
            confidence_adjustment=-0.15 if contradicting else 0.0,
            recommendation="REVIEW" if contradicting or not supporting else "PROCEED_TO_DECISION_SUPPORT",
        )
        final_confidence = _clamp(confidence + critique.confidence_adjustment)
        questions = ("What independent evidence could falsify this finding?",) if not contradicting else ("Which evidence is more reliable and why?",)
        return ReasoningResult(str(uuid4()), query, (finding,), (critique,), final_confidence, refs, questions, provenance or {})
