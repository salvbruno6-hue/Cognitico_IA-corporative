"""Analytical integrity guard for ELO reasoning.

This module adds deterministic checks for *misuse* of otherwise valid evidence.
It does not replace requirement analysis, source admission, the Orchestrator,
Symbiont, Evolution Gate, or domain-specific reasoning.

The core rule is:

    evidence quality != decision authority != action authorization

External or retrieved data may inform an analysis but cannot silently increase
execution authority. Historical, theoretical, inferred, conflicting or missing
evidence also cannot be promoted to stronger states without an explicit governed
transition.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from elo.cognitive.reasoning.requirement_analysis import RequirementState


class EvidenceUse(StrEnum):
    ANALYSIS = "ANALYSIS"
    CURRENT_STATE_CLAIM = "CURRENT_STATE_CLAIM"
    DECISION_RECOMMENDATION = "DECISION_RECOMMENDATION"
    ACTION_AUTHORIZATION = "ACTION_AUTHORIZATION"


class SourceRole(StrEnum):
    EVIDENCE = "EVIDENCE"
    AUTHORITY = "AUTHORITY"


class Temporality(StrEnum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    THEORETICAL = "THEORETICAL"
    UNKNOWN = "UNKNOWN"


class IntegritySeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCK = "BLOCK"


@dataclass(frozen=True, slots=True)
class EvidenceUsage:
    subject: str
    state: RequirementState
    use: EvidenceUse
    source_role: SourceRole = SourceRole.EVIDENCE
    temporality: Temporality = Temporality.UNKNOWN
    explicit_label: bool = False
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IntegrityFinding:
    code: str
    severity: IntegritySeverity
    subject: str
    message: str
    corrective_action: str


@dataclass(frozen=True, slots=True)
class BehavioralExpectation:
    control_id: str
    expected: bool
    observed: bool
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BehavioralConformance:
    control_id: str
    status: str
    evidence_ids: tuple[str, ...]


_UNRESOLVED_STATES = {
    RequirementState.MISSING,
    RequirementState.GAP_CANDIDATE,
    RequirementState.GAP_CONFIRMED,
    RequirementState.HUMAN_VALIDATION_REQUIRED,
}

_WEAK_STATES = {
    RequirementState.INFERRED,
    RequirementState.ASSUMPTION_REQUIRED,
}

_DECISIVE_USES = {
    EvidenceUse.CURRENT_STATE_CLAIM,
    EvidenceUse.ACTION_AUTHORIZATION,
}


def assess_evidence_usage(usage: EvidenceUsage) -> tuple[IntegrityFinding, ...]:
    """Detect invalid promotion or use of evidence.

    The function is intentionally small and deterministic. Callers provide the
    already-classified evidence state; this guard only checks whether the chosen
    use is compatible with that state and its authority/temporality.
    """
    findings: list[IntegrityFinding] = []

    if usage.state in _UNRESOLVED_STATES and usage.use != EvidenceUse.ANALYSIS:
        findings.append(IntegrityFinding(
            code="ELO-AI-001-UNRESOLVED-AS-FACT",
            severity=IntegritySeverity.BLOCK,
            subject=usage.subject,
            message="Unresolved or missing evidence cannot be promoted to a factual/decisory use.",
            corrective_action="Keep the value unresolved and request the next required evidence.",
        ))

    if usage.state in _WEAK_STATES and not usage.explicit_label:
        findings.append(IntegrityFinding(
            code="ELO-AI-002-UNLABELED-INFERENCE",
            severity=IntegritySeverity.WARNING,
            subject=usage.subject,
            message="Inference or assumption is being used without an explicit uncertainty label.",
            corrective_action="Label it as inference/assumption and preserve the validation boundary.",
        ))

    if usage.state in _WEAK_STATES and usage.use in _DECISIVE_USES:
        findings.append(IntegrityFinding(
            code="ELO-AI-007-WEAK-EVIDENCE-AS-DECISIVE",
            severity=IntegritySeverity.BLOCK,
            subject=usage.subject,
            message="Inference or assumption cannot establish current fact or authorize an action.",
            corrective_action="Keep it analytical/recommendatory until governed evidence validates the claim.",
        ))

    if usage.state == RequirementState.CONFLICT and usage.use != EvidenceUse.ANALYSIS:
        findings.append(IntegrityFinding(
            code="ELO-AI-003-CONFLICT-SILENTLY-RESOLVED",
            severity=IntegritySeverity.BLOCK,
            subject=usage.subject,
            message="Conflicting evidence cannot be silently selected as the resolved truth.",
            corrective_action="Preserve the contradiction and resolve it with evidence, policy or authorized decision.",
        ))

    if usage.temporality == Temporality.HISTORICAL and usage.use == EvidenceUse.CURRENT_STATE_CLAIM:
        findings.append(IntegrityFinding(
            code="ELO-AI-004-HISTORICAL-AS-CURRENT",
            severity=IntegritySeverity.BLOCK,
            subject=usage.subject,
            message="Historical evidence cannot be presented as current state without revalidation.",
            corrective_action="Use it only as historical reference or obtain current evidence.",
        ))

    if usage.temporality == Temporality.THEORETICAL and usage.use == EvidenceUse.CURRENT_STATE_CLAIM:
        findings.append(IntegrityFinding(
            code="ELO-AI-005-THEORETICAL-AS-REALIZED",
            severity=IntegritySeverity.BLOCK,
            subject=usage.subject,
            message="Theoretical capacity/result cannot be presented as realized current performance.",
            corrective_action="Keep the theoretical label and compare against observed/realized evidence.",
        ))

    if usage.use == EvidenceUse.ACTION_AUTHORIZATION and usage.source_role != SourceRole.AUTHORITY:
        findings.append(IntegrityFinding(
            code="ELO-AI-006-EVIDENCE-AS-AUTHORIZATION",
            severity=IntegritySeverity.BLOCK,
            subject=usage.subject,
            message="Evidence may support an action but cannot itself grant action authority.",
            corrective_action="Resolve authorization through the governed human/policy/action boundary.",
        ))

    return tuple(findings)


def assess_many(usages: Iterable[EvidenceUsage]) -> tuple[IntegrityFinding, ...]:
    return tuple(finding for usage in usages for finding in assess_evidence_usage(usage))


def assess_behavioral_conformance(
    expectations: Iterable[BehavioralExpectation],
) -> tuple[BehavioralConformance, ...]:
    """Compare declared controls with observed behavior without changing authority."""
    results: list[BehavioralConformance] = []
    for item in expectations:
        status = "CONFORMANT" if item.expected == item.observed else "DIVERGENT"
        results.append(BehavioralConformance(
            control_id=item.control_id,
            status=status,
            evidence_ids=item.evidence_ids,
        ))
    return tuple(results)


__all__ = [
    "BehavioralConformance",
    "BehavioralExpectation",
    "EvidenceUse",
    "EvidenceUsage",
    "IntegrityFinding",
    "IntegritySeverity",
    "SourceRole",
    "Temporality",
    "assess_behavioral_conformance",
    "assess_evidence_usage",
    "assess_many",
]
