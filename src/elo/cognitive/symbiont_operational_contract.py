"""Operational boundary contract for governed Symbiont decision support.

This module consolidates the executable boundary rules already distributed across
ELO Cognitive, Hermes and MCP contracts. It is a validation/translation layer,
not a second governance engine, decision ledger, memory authority or evolution gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping


MIN_CONFIDENCE = 0.70


class SymbiontOperation(StrEnum):
    METADATA_READ = "metadata_read"
    READ = "read"
    QUERY = "query"
    SCENARIO_SIM = "scenario_sim"
    RISK_ASSESS = "risk_assess"
    KPI_CALC = "kpi_calc"


class DecisionArtifact(StrEnum):
    SQL_QUERY_READONLY = "sql_query_readonly"
    KPI_CALC = "kpi_calc"
    SCENARIO_SIM = "scenario_sim"
    RISK_ASSESS = "risk_assess"
    DECISION_BRIEF = "decision_brief"


@dataclass(frozen=True)
class HumanEscalation:
    required: bool
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class SymbiontDecisionBrief:
    """Evidence-bearing advisory output; never a canonical decision record."""

    request_id: str
    tenant_scope: str
    problem: str
    evidence: tuple[str, ...]
    alternatives: tuple[str, ...]
    trade_offs: tuple[str, ...]
    recommendation: str
    confidence: float
    risks: tuple[str, ...]
    audit_refs: tuple[str, ...]
    artifacts: tuple[DecisionArtifact, ...] = ()
    canonical_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        for name, value in (
            ("request_id", self.request_id),
            ("tenant_scope", self.tenant_scope),
            ("problem", self.problem),
            ("recommendation", self.recommendation),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not self.evidence:
            raise ValueError("decision_brief requires evidence")
        if not self.audit_refs:
            raise ValueError("decision_brief requires audit_refs")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.canonical_mutation_allowed:
            raise ValueError("decision_brief cannot mutate canonical state")

    @property
    def human_escalation(self) -> HumanEscalation:
        reasons: list[str] = []
        if self.confidence < MIN_CONFIDENCE:
            reasons.append("confidence_below_minimum")
        if not self.evidence:
            reasons.append("insufficient_evidence")
        return HumanEscalation(bool(reasons), tuple(reasons))


@dataclass(frozen=True)
class SymbiontRequestGuard:
    """Explicit request-level controls for the external reasoning boundary."""

    request_id: str
    tenant_scope: str
    acknowledged: bool
    authorized: bool
    non_destructive: bool = True
    canonical_mutation_allowed: bool = False
    pii_masked: bool = False
    financial_impact: float | None = None
    owner_financial_limit: float | None = None
    canon_conflict: bool = False
    high_risk: bool = False
    evidence_available: bool = True

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.tenant_scope.strip():
            raise ValueError("request identity and tenant scope are required")
        if not self.acknowledged:
            raise ValueError("mandate acknowledgement is required")
        if not self.authorized:
            raise ValueError("ELO authorization is required")
        if not self.non_destructive:
            raise ValueError("destructive Symbiont operations are outside this boundary")
        if self.canonical_mutation_allowed:
            raise ValueError("Symbiont cannot mutate canonical state")
        if self.financial_impact is not None and self.financial_impact < 0:
            raise ValueError("financial_impact cannot be negative")
        if self.owner_financial_limit is not None and self.owner_financial_limit < 0:
            raise ValueError("owner_financial_limit cannot be negative")

    def human_escalation(self) -> HumanEscalation:
        reasons: list[str] = []
        if self.high_risk:
            reasons.append("high_risk")
        if self.canon_conflict:
            reasons.append("canon_conflict")
        if not self.evidence_available:
            reasons.append("insufficient_evidence")
        if (
            self.financial_impact is not None
            and self.owner_financial_limit is not None
            and self.financial_impact > self.owner_financial_limit
        ):
            reasons.append("financial_impact_above_owner_limit")
        if not self.pii_masked:
            reasons.append("pii_masking_not_confirmed")
        return HumanEscalation(bool(reasons), tuple(reasons))


_ALLOWED_OPERATIONS = frozenset(SymbiontOperation)
_BLOCKED_OPERATIONS = frozenset({"write", "schema_change", "ddl", "dml", "decision_register"})


def validate_operation(operation: str) -> SymbiontOperation:
    """Allow only governed read/reasoning operations; reject arbitrary SQL/write paths."""
    if operation in _BLOCKED_OPERATIONS:
        raise ValueError(f"operation is blocked at Symbiont boundary: {operation}")
    try:
        return SymbiontOperation(operation)
    except ValueError as exc:
        raise ValueError(f"unsupported Symbiont operation: {operation}") from exc


def validate_artifact(artifact: str) -> DecisionArtifact:
    try:
        return DecisionArtifact(artifact)
    except ValueError as exc:
        raise ValueError(f"unsupported decision artifact: {artifact}") from exc


def reject_canonical_or_secret_fields(value: Any) -> None:
    """Prevent infrastructure, secrets and competing canonical-authority fields."""
    forbidden = {
        "project_id",
        "project_ref",
        "supabase_project",
        "database_url",
        "service_role_key",
        "canonical_knowledge",
        "decision_ledger",
        "memory_ledger",
    }
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in forbidden:
                raise ValueError(f"forbidden field at Symbiont boundary: {key}")
            reject_canonical_or_secret_fields(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            reject_canonical_or_secret_fields(child)


__all__ = [
    "DecisionArtifact",
    "HumanEscalation",
    "MIN_CONFIDENCE",
    "SymbiontDecisionBrief",
    "SymbiontOperation",
    "SymbiontRequestGuard",
    "reject_canonical_or_secret_fields",
    "validate_artifact",
    "validate_operation",
]
