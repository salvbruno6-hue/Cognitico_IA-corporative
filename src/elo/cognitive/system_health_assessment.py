"""Evidence-based, read-only system health assessment for the ELO Symbiont.

This module does not replace System Health Gate, Evolution Gate, elo-authz,
canonical owners, or production probes. It only converts explicit governed
findings into a reproducible diagnostic score and priority order.

The score is observational. It is never authorization for mutation, promotion,
policy rewrite, tenant assignment, capability grant, or data backfill.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Sequence


class HealthSeverity(StrEnum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    GAP_HIGH = "GAP_HIGH"
    BLOCK = "BLOCK"


class HealthState(StrEnum):
    NOT_MEASURED = "NOT_MEASURED"
    HEALTHY = "HEALTHY"
    ATTENTION = "ATTENTION"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


_SEVERITY_PENALTY = {
    HealthSeverity.PASS: 0.0,
    HealthSeverity.REVIEW: 0.25,
    HealthSeverity.GAP_HIGH: 0.60,
    HealthSeverity.BLOCK: 1.0,
}

_SEVERITY_PRIORITY = {
    HealthSeverity.BLOCK: 0,
    HealthSeverity.GAP_HIGH: 1,
    HealthSeverity.REVIEW: 2,
    HealthSeverity.PASS: 3,
}


@dataclass(frozen=True, slots=True)
class SystemHealthFinding:
    finding_id: str
    dimension: str
    severity: HealthSeverity
    weight: float
    evidence_refs: tuple[str, ...]
    detail: str = ""
    owner: str | None = None

    def __post_init__(self) -> None:
        if not self.finding_id.strip():
            raise ValueError("finding_id is required")
        if not self.dimension.strip():
            raise ValueError("dimension is required")
        if self.weight <= 0:
            raise ValueError("weight must be greater than zero")
        if not tuple(ref for ref in self.evidence_refs if str(ref).strip()):
            raise ValueError("health findings require explicit evidence references")


@dataclass(frozen=True, slots=True)
class SystemHealthAssessment:
    state: HealthState
    score_percent: float | None
    findings: tuple[SystemHealthFinding, ...]
    priority_findings: tuple[SystemHealthFinding, ...]
    evidence_refs: tuple[str, ...]
    canonical_mutation: bool = False

    @property
    def measured(self) -> bool:
        return self.score_percent is not None

    def as_dict(self) -> dict[str, object]:
        return {
            "state": self.state.value,
            "score_percent": self.score_percent,
            "findings": [
                {
                    "finding_id": item.finding_id,
                    "dimension": item.dimension,
                    "severity": item.severity.value,
                    "weight": item.weight,
                    "evidence_refs": list(item.evidence_refs),
                    "detail": item.detail,
                    "owner": item.owner,
                }
                for item in self.findings
            ],
            "priority_findings": [item.finding_id for item in self.priority_findings],
            "evidence_refs": list(self.evidence_refs),
            "canonical_mutation": self.canonical_mutation,
        }


def assess_system_health(findings: Sequence[SystemHealthFinding]) -> SystemHealthAssessment:
    """Produce a reproducible diagnostic score from explicit governed findings.

    Each caller supplies the importance weight of each measured finding. Severity
    controls the fraction of that weight counted as health debt:

    PASS=0%, REVIEW=25%, GAP_HIGH=60%, BLOCK=100%.

    Empty input is NOT_MEASURED rather than an inferred 100% score. A BLOCK
    finding always produces BLOCKED state even when its relative weight is low.
    """
    normalized = tuple(findings)
    if not normalized:
        return SystemHealthAssessment(
            state=HealthState.NOT_MEASURED,
            score_percent=None,
            findings=(),
            priority_findings=(),
            evidence_refs=(),
        )

    total_weight = sum(item.weight for item in normalized)
    debt = sum(item.weight * _SEVERITY_PENALTY[item.severity] for item in normalized)
    score = round(max(0.0, min(100.0, 100.0 * (1.0 - debt / total_weight))), 2)

    if any(item.severity is HealthSeverity.BLOCK for item in normalized):
        state = HealthState.BLOCKED
    elif score >= 90.0:
        state = HealthState.HEALTHY
    elif score >= 75.0:
        state = HealthState.ATTENTION
    else:
        state = HealthState.DEGRADED

    priority = tuple(
        sorted(
            (item for item in normalized if item.severity is not HealthSeverity.PASS),
            key=lambda item: (_SEVERITY_PRIORITY[item.severity], -item.weight, item.finding_id),
        )
    )
    refs = tuple(
        dict.fromkeys(
            ref.strip()
            for item in normalized
            for ref in item.evidence_refs
            if str(ref).strip()
        )
    )
    return SystemHealthAssessment(
        state=state,
        score_percent=score,
        findings=normalized,
        priority_findings=priority,
        evidence_refs=refs,
    )


__all__ = [
    "HealthSeverity",
    "HealthState",
    "SystemHealthFinding",
    "SystemHealthAssessment",
    "assess_system_health",
]
