"""Bridge Symbiont system-health observation into bounded orchestration guidance.

The Symbiont owns observation/diagnosis. Canonical owners own remediation.
Authorization remains external. This bridge never mutates health state, runs a
repair, rewrites RLS, grants scopes/capabilities, or promotes through a gate.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.system_health_assessment import (
    HealthSeverity,
    SystemHealthAssessment,
    SystemHealthFinding,
)


@dataclass(frozen=True, slots=True)
class HealthOrientation:
    finding_id: str
    dimension: str
    severity: str
    action: str
    owner: str | None
    authorized: bool
    evidence_refs: tuple[str, ...]
    reason: str


class SystemHealthSymbiontBridge:
    """Translate read-only health findings into non-authoritative next actions."""

    _ACTIONS = {
        HealthSeverity.BLOCK: "STOP_PROMOTION_AND_REMEDIATE",
        HealthSeverity.GAP_HIGH: "BOUNDED_REMEDIATION",
        HealthSeverity.REVIEW: "INVESTIGATE_PROVENANCE",
        HealthSeverity.PASS: "PRESERVE_VERIFIED_STATE",
    }

    def orient(
        self,
        assessment: SystemHealthAssessment,
        *,
        authorized_actions: frozenset[str] = frozenset(),
    ) -> tuple[HealthOrientation, ...]:
        findings = assessment.priority_findings or tuple(
            item for item in assessment.findings if item.severity is HealthSeverity.PASS
        )
        return tuple(
            self._orient_one(item, authorized_actions=authorized_actions)
            for item in findings
        )

    def _orient_one(
        self,
        finding: SystemHealthFinding,
        *,
        authorized_actions: frozenset[str],
    ) -> HealthOrientation:
        action = self._ACTIONS[finding.severity]
        return HealthOrientation(
            finding_id=finding.finding_id,
            dimension=finding.dimension,
            severity=finding.severity.value,
            action=action,
            owner=finding.owner,
            authorized=action in authorized_actions,
            evidence_refs=finding.evidence_refs,
            reason=(
                "Symbiont observation requires canonical-owner intervention; authorization remains external"
                if finding.severity is not HealthSeverity.PASS
                else "preserve the explicitly evidenced healthy state"
            ),
        )


__all__ = ["HealthOrientation", "SystemHealthSymbiontBridge"]
