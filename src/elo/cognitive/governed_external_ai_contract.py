"""ELO-owned contract for governed external-AI/Symbiont decision intake.

This contract consolidates existing governance primitives without creating a
second decision, memory, authorization, or promotion authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

MIN_CONFIDENCE = 0.70
_FORBIDDEN_AUDIT_KEYS = frozenset({"password", "secret", "token", "api_key", "service_role_key", "database_url"})


def _reject_sensitive_keys(value: Any, path: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _FORBIDDEN_AUDIT_KEYS:
                raise ValueError(f"sensitive field is not allowed: {path}.{key}")
            _reject_sensitive_keys(child, f"{path}.{key}")
    elif isinstance(value, (tuple, list)):
        for index, child in enumerate(value):
            _reject_sensitive_keys(child, f"{path}[{index}]")

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
        if not self.alternatives:
            raise ValueError("decision brief requires alternatives")
        if not self.trade_offs:
            raise ValueError("decision brief requires trade-offs")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.audit:
            raise ValueError("decision brief requires audit metadata")
        _reject_sensitive_keys(self.audit, "audit")
        if not self.audit.get("authorization_decision_id"):
            raise ValueError("decision brief requires authorization_decision_id")
        if self.audit.get("request_id") not in {None, self.request_id}:
            raise ValueError("audit request_id does not match decision brief")
        if self.audit.get("tenant_scope") not in {None, self.tenant_scope}:
            raise ValueError("audit tenant_scope does not match decision brief")
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
    authorization_decision_id: str
    constraints: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tenant_scope != self.mandate.tenant_scope:
            raise ValueError("tenant scope does not match acknowledged mandate")
        if not self.authorization_decision_id.strip():
            raise ValueError("authorization_decision_id is required")
        if not self.authorized_capabilities:
            raise ValueError("authorized_capabilities is required")
        if any(not capability.strip() for capability in self.authorized_capabilities):
            raise ValueError("authorized_capabilities cannot contain empty values")
        if not self.evidence_requirements:
            raise ValueError("evidence_requirements is required")
        if self.constraints.get("canonical_mutation", False):
            raise ValueError("external AI envelope cannot grant canonical mutation authority")
        if self.constraints.get("pii_exposure", False):
            raise ValueError("external AI envelope cannot authorize unmasked PII exposure")
        financial_impact = self.constraints.get("financial_impact")
        financial_limit = self.constraints.get("financial_limit")
        if financial_impact is not None or financial_limit is not None:
            if not isinstance(financial_impact, (int, float)) or not isinstance(financial_limit, (int, float)):
                raise ValueError("financial_impact and financial_limit must be numeric when supplied")
            if financial_impact > financial_limit and "FINANCIAL_LIMIT" not in self.constraints.get("escalation_reasons", ()):
                raise ValueError("financial impact above limit requires FINANCIAL_LIMIT escalation")
        if self.constraints.get("read_only") is False and not self.constraints.get("explicit_operation_authorization", False):
            raise ValueError("non-read-only execution requires explicit operation authorization")
