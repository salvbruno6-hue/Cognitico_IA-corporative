"""Compatibility facade for the canonical external-AI Symbiont contract.

The canonical mandate and decision-brief definitions live in
governed_external_ai_contract. This module keeps the existing Symbiont
runtime import surface while ensuring there is only one contract authority.
Authorization, evolution and learning remain owned by their existing services.
"""

from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.governed_external_ai_contract import (
    ALLOWED_ESCALATIONS,
    MIN_CONFIDENCE,
    DecisionBrief,
    ExternalAIMandateAck,
)

CONFIDENCE_MINIMUM = MIN_CONFIDENCE
MandateAcknowledgement = ExternalAIMandateAck
ALLOWED_OPERATIONS = frozenset(
    {"metadata_read", "read", "query", "write", "schema_change"}
)


@dataclass(frozen=True)
class EscalationAssessment:
    required: bool
    reasons: tuple[str, ...]


def assess_escalation(
    *,
    confidence: float,
    risk: str,
    canonical_conflict: bool = False,
    insufficient_evidence: bool = False,
    financial_impact: float | None = None,
    financial_limit: float | None = None,
    irreversible_action: bool = False,
    pii_exposure: bool = False,
) -> EscalationAssessment:
    """Apply existing escalation conditions without granting authority."""
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if financial_impact is not None and financial_impact < 0:
        raise ValueError("financial_impact cannot be negative")
    if financial_limit is not None and financial_limit < 0:
        raise ValueError("financial_limit cannot be negative")

    reasons: list[str] = []
    if confidence < CONFIDENCE_MINIMUM:
        reasons.append("LOW_CONFIDENCE")
    if risk.strip().upper() in {"HIGH", "CRITICAL", "ALTO", "CRITICO"}:
        reasons.append("HIGH_RISK")
    if canonical_conflict:
        reasons.append("CANON_CONFLICT")
    if insufficient_evidence:
        reasons.append("INSUFFICIENT_EVIDENCE")
    if irreversible_action:
        reasons.append("IRREVERSIBLE_ACTION")
    if pii_exposure:
        reasons.append("PII_EXPOSURE")
    if financial_impact is not None and financial_limit is not None and financial_impact > financial_limit:
        reasons.append("FINANCIAL_LIMIT")

    return EscalationAssessment(required=bool(reasons), reasons=tuple(reasons))


def validate_symbiont_operation(
    *,
    acknowledgement: MandateAcknowledgement | None,
    operation: str,
    pii_exposure: bool = False,
    canonical_mutation: bool = False,
) -> None:
    """Fail closed before an external-AI operation reaches an execution adapter."""
    if acknowledgement is None:
        raise ValueError("valid mandate acknowledgement is required")
    if operation not in ALLOWED_OPERATIONS:
        raise ValueError(f"unsupported operation: {operation}")
    if pii_exposure:
        raise ValueError("PII exposure is not permitted")
    if canonical_mutation:
        raise ValueError("canonical mutation is not permitted by Symbiont contract")


__all__ = [
    "ALLOWED_ESCALATIONS",
    "ALLOWED_OPERATIONS",
    "CONFIDENCE_MINIMUM",
    "DecisionBrief",
    "EscalationAssessment",
    "MandateAcknowledgement",
    "assess_escalation",
    "validate_symbiont_operation",
]
