"""Governance contract for the ELO Symbiont external-AI boundary.

This module consolidates existing ELO rules without creating a new authority.
It defines mandate acknowledgement, decision-brief shape and escalation
conditions; authorization, evolution and learning remain owned by their
existing canonical services.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

CONFIDENCE_MINIMUM = 0.70
ALLOWED_OPERATIONS = frozenset(
    {"metadata_read", "read", "query", "write", "schema_change"}
)


@dataclass(frozen=True)
class MandateAcknowledgement:
    request_id: str
    identity_id: str
    tenant_scope: str
    mandate_version: str
    acknowledged: bool

    def __post_init__(self) -> None:
        for value, name in (
            (self.request_id, "request_id"),
            (self.identity_id, "identity_id"),
            (self.tenant_scope, "tenant_scope"),
            (self.mandate_version, "mandate_version"),
        ):
            if not value or not value.strip():
                raise ValueError(f"{name} is required")
        if not self.acknowledged:
            raise ValueError("mandate acknowledgement is required")


@dataclass(frozen=True)
class DecisionBrief:
    request_id: str
    tenant_scope: str
    problem: str
    evidence: tuple[str, ...]
    alternatives: tuple[str, ...]
    tradeoffs: tuple[str, ...]
    recommendation: str
    confidence: float
    risks: tuple[str, ...]
    audit_ref: str

    def __post_init__(self) -> None:
        required = (
            self.request_id,
            self.tenant_scope,
            self.problem,
            self.recommendation,
            self.audit_ref,
        )
        if not all(value and value.strip() for value in required):
            raise ValueError("decision brief requires identity, problem, recommendation and audit")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.evidence:
            raise ValueError("decision brief requires evidence")

    @property
    def confidence_sufficient(self) -> bool:
        return self.confidence >= CONFIDENCE_MINIMUM


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
    """Apply the existing human-escalation boundary to a Symbiont result.

    A financial threshold is contextual: no monetary limit is invented here.
    PII exposure and irreversible actions are treated as escalation conditions;
    execution authority remains outside this function.
    """
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if financial_impact is not None and financial_impact < 0:
        raise ValueError("financial_impact cannot be negative")
    if financial_limit is not None and financial_limit < 0:
        raise ValueError("financial_limit cannot be negative")

    reasons: list[str] = []
    if confidence < CONFIDENCE_MINIMUM:
        reasons.append("confidence_below_minimum")
    if risk.strip().upper() in {"HIGH", "CRITICAL", "ALTO", "CRITICO"}:
        reasons.append("high_risk")
    if canonical_conflict:
        reasons.append("canonical_conflict")
    if insufficient_evidence:
        reasons.append("insufficient_evidence")
    if irreversible_action:
        reasons.append("irreversible_action")
    if pii_exposure:
        reasons.append("pii_exposure")
    if (
        financial_impact is not None
        and financial_limit is not None
        and financial_impact > financial_limit
    ):
        reasons.append("financial_limit_exceeded")

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
