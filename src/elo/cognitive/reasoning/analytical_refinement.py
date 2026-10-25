"""Contextual selection for ELO Analytical Integrity Framework (EAIF).

This module decides *whether* an analysis should receive additional integrity
refinement. It does not reason about business facts, inspect free-form user text,
select models/tools, execute actions, or grant authority.

Callers must provide already-structured signals. The selector is deterministic,
side-effect free and intentionally conservative about escalating work.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RefinementLevel(StrEnum):
    NONE = "NONE"
    TARGETED = "TARGETED"
    DEEP = "DEEP"


@dataclass(frozen=True, slots=True)
class AnalyticalRefinementSignals:
    """Governed signals that may justify additional analytical refinement."""

    decision_required: bool = False
    consequential_action: bool = False
    integrity_gaps: tuple[str, ...] = ()
    uncertainties: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    temporal_risks: tuple[str, ...] = ()
    weak_evidence: bool = False


@dataclass(frozen=True, slots=True)
class AnalyticalRefinementDecision:
    level: RefinementLevel
    reasons: tuple[str, ...]
    checks: tuple[str, ...]


_TARGETED_CHECKS = (
    "verify evidence state and explicit uncertainty",
    "verify temporal validity and applicability",
    "preserve contradiction instead of silently resolving it",
    "keep evidence separate from decision/action authority",
)

_DEEP_CHECKS = _TARGETED_CHECKS + (
    "search for counterevidence and alternative hypotheses",
    "state what evidence would falsify the proposed conclusion",
    "verify that weak/inferred evidence is not promoted to decisive use",
)


def select_analytical_refinement(
    signals: AnalyticalRefinementSignals,
) -> AnalyticalRefinementDecision:
    """Select NONE, TARGETED or DEEP refinement from structured risk signals.

    Rules are intentionally transparent:
    - no relevant signal -> NONE;
    - one or more ordinary integrity risks -> TARGETED;
    - explicit conflict -> DEEP;
    - consequential action combined with another integrity risk -> DEEP;
    - three or more independent risk families -> DEEP.

    A consequential action by itself triggers TARGETED review because action
    authority must remain distinct from analytical evidence.
    """
    reasons: list[str] = []
    risk_families = 0

    if signals.decision_required:
        reasons.append("decision boundary is active")
        risk_families += 1
    if signals.consequential_action:
        reasons.append("consequential action is contemplated")
        risk_families += 1
    if signals.integrity_gaps:
        reasons.append("context/evidence integrity gaps are unresolved")
        risk_families += 1
    if signals.uncertainties:
        reasons.append("material uncertainty remains")
        risk_families += 1
    if signals.conflicts:
        reasons.append("conflicting evidence or interpretations are present")
        risk_families += 1
    if signals.temporal_risks:
        reasons.append("historical/theoretical/stale evidence may be misapplied")
        risk_families += 1
    if signals.weak_evidence:
        reasons.append("available evidence is below the sufficiency threshold")
        risk_families += 1

    if not reasons:
        return AnalyticalRefinementDecision(
            level=RefinementLevel.NONE,
            reasons=(),
            checks=(),
        )

    deep = bool(signals.conflicts)
    non_action_risk = any((
        signals.integrity_gaps,
        signals.uncertainties,
        signals.conflicts,
        signals.temporal_risks,
        signals.weak_evidence,
    ))
    if signals.consequential_action and non_action_risk:
        deep = True
    if risk_families >= 3:
        deep = True

    level = RefinementLevel.DEEP if deep else RefinementLevel.TARGETED
    return AnalyticalRefinementDecision(
        level=level,
        reasons=tuple(reasons),
        checks=_DEEP_CHECKS if deep else _TARGETED_CHECKS,
    )


__all__ = [
    "AnalyticalRefinementDecision",
    "AnalyticalRefinementSignals",
    "RefinementLevel",
    "select_analytical_refinement",
]
