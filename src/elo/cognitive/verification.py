from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VerificationResult:
    accepted: bool
    confidence: float
    reasons: tuple[str, ...]


class CognitiveVerifier:
    """Provider-agnostic verification gate for cognitive outputs."""

    def verify(
        self,
        *,
        answer: str,
        evidence_confidences: tuple[float, ...] = (),
        contradiction: bool = False,
        required_confidence: float = 0.7,
    ) -> VerificationResult:
        if not 0.0 <= required_confidence <= 1.0:
            raise ValueError("required_confidence must be between 0 and 1")
        if any(not 0.0 <= value <= 1.0 for value in evidence_confidences):
            raise ValueError("evidence confidence must be between 0 and 1")

        if not answer.strip():
            return VerificationResult(False, 0.0, ("empty answer",))
        if contradiction:
            return VerificationResult(False, 0.0, ("contradictory evidence",))

        confidence = min(evidence_confidences) if evidence_confidences else 0.5
        accepted = confidence >= required_confidence
        reason = "evidence threshold satisfied" if accepted else "insufficient evidence confidence"
        return VerificationResult(accepted, confidence, (reason,))
