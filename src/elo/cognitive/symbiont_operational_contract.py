"""Governed operational boundary for Symbiont decision support.

The contract is intentionally narrow: it validates allowed read/analysis
operations and prevents external/runtime callers from gaining canonical
mutation authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


MIN_CONFIDENCE = 0.70


class SymbiontOperation(str, Enum):
    METADATA_READ = "metadata_read"
    READ = "read"
    QUERY = "query"
    SCENARIO_SIM = "scenario_sim"
    RISK_ASSESS = "risk_assess"
    KPI_CALC = "kpi_calc"


_BLOCKED = frozenset({"write", "schema_change", "ddl", "dml", "decision_register"})


@dataclass(frozen=True)
class SymbiontRequest:
    operation: str
    tenant_scope: str
    confidence: float
    evidence_ids: tuple[str, ...] = ()
    canonical_mutation_allowed: bool = False
    authority: str = "recommend"


@dataclass(frozen=True)
class SymbiontDecisionBrief:
    problem: str
    evidence_ids: tuple[str, ...]
    alternatives: tuple[str, ...]
    trade_offs: tuple[str, ...]
    recommendation: str
    confidence: float
    risks: tuple[str, ...]


class SymbiontRequestGuard:
    """Fail-closed request guard; it does not execute or mutate anything."""

    @staticmethod
    def validate(request: SymbiontRequest) -> None:
        operation = request.operation.strip().lower()
        if operation in _BLOCKED:
            raise ValueError(f"blocked Symbiont operation: {operation}")
        if operation not in {item.value for item in SymbiontOperation}:
            raise ValueError(f"unsupported Symbiont operation: {operation}")
        if not request.tenant_scope.strip():
            raise ValueError("tenant scope is required")
        if request.canonical_mutation_allowed:
            raise ValueError("Symbiont cannot mutate canonical ELO state")
        if request.authority != "recommend":
            raise ValueError("Symbiont authority must remain recommend")
        if not 0.0 <= request.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if request.confidence >= MIN_CONFIDENCE and not request.evidence_ids:
            raise ValueError("confidence at or above threshold requires evidence")

    @staticmethod
    def requires_human_escalation(*, confidence: float, high_risk: bool = False,
                                   financial_impact: bool = False,
                                   canon_conflict: bool = False,
                                   insufficient_evidence: bool = False) -> bool:
        return (
            confidence < MIN_CONFIDENCE
            or high_risk
            or financial_impact
            or canon_conflict
            or insufficient_evidence
        )
