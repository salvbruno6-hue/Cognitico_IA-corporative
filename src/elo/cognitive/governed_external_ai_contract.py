"""ELO-owned contract for governed external-AI/Symbiont decision intake.

This contract consolidates existing governance primitives without creating a
second decision, memory, authorization, or promotion authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

MIN_CONFIDENCE = 0.70
ALLOWED_ESCALATIONS = frozenset({
    "LOW_CONFIDENCE",
    "HIGH_RISK",
    "FINANCIAL_LIMIT",
    "CANON_CONFLICT",
    "INSUFFICIENT_EVIDENCE",
    "AUTHORIZATION_GAP",
})


@dataclass(frozen=True)
class ExternalAIMandateAck:
    """Proof that an external AI accepted the ELO operating boundary."""

    request_id: str
    actor_id: str
    tenant_scope: str
    mandate_version: str
    acknowledged: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.request_id, "request_id"),
            (self.actor_id, "actor_id"),
            (self.tenant_scope, "tenant_scope"),
            (self.mandate_version, "mandate_version"),
        ):
            if not value or not value.strip():
                raise ValueError(f"{name} is required")
        if not self.acknowledged:
            raise ValueError("external AI mandate must be acknowledged")


@dataclass(frozen=True)
class DecisionBrief:
    """Evidence-bearing consultative result; never a canonical decision."""

    request_id: str
    tenant_scope: str
    problem: str
    evidence: tuple[str, ...]
    alternatives: tuple[str, ...]
    trade_offs: tuple[str, ...]
    recommendation: str
    confidence: float
    risks: tuple[str, ...] = ()
    escalation_reasons: tuple[str, ...] = ()
    audit: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for value, name in (
            (self.request_id, "request_id"),
            (self.tenant_scope, "tenant_scope"),
            (self.problem, "problem"),
            (self.recommendation, "recommendation"),
        ):
            if not value or not value.strip():
                raise ValueError(f"{name} is required")
        if not self.evidence:
            raise ValueError("decision brief requires evidence")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.audit:
            raise ValueError("decision brief requires audit metadata")
        if any(reason not in ALLOWED_ESCALATIONS for reason in self.escalation_reasons):
            raise ValueError("unsupported escalation reason")
        if self.confidence < MIN_CONFIDENCE and "LOW_CONFIDENCE" not in self.escalation_reasons:
            raise ValueError("low confidence requires LOW_CONFIDENCE escalation")
        if "CANON_CONFLICT" in self.escalation_reasons and self.confidence >= MIN_CONFIDENCE:
            # A canon conflict is independently escalatable; confidence does not clear it.
            pass

    @property
    def human_escalation_required(self) -> bool:
        return bool(self.escalation_reasons) or self.confidence < MIN_CONFIDENCE


@dataclass(frozen=True)
class GovernedExternalAIEnvelope:
    """Execution envelope joining mandate, scope, capabilities and evidence rules."""

    mandate: ExternalAIMandateAck
    tenant_scope: str
    authorized_capabilities: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    constraints: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tenant_scope != self.mandate.tenant_scope:
            raise ValueError("tenant scope does not match acknowledged mandate")
        if not self.authorized_capabilities:
            raise ValueError("authorized_capabilities is required")
        if not self.evidence_requirements:
            raise ValueError("evidence_requirements is required")
        if self.constraints.get("canonical_mutation", False):
            raise ValueError("external AI envelope cannot grant canonical mutation authority")
        if self.constraints.get("read_only") is False and not self.constraints.get("explicit_operation_authorization", False):
            raise ValueError("non-read-only execution requires explicit operation authorization")
