"""Governed promotion states for the eight Hermes capability candidates.

Operational activation and Core canonization are separate gates. A native capability
may become operationally active after its controlled functional proof passes. Canonical
promotion additionally requires explicit structural relevance to an ELO Core pillar,
complete provenance/governance, and an Evolution Gate approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .native_capabilities import CAPABILITY_IDS, NativeEvidence


class PromotionState(str, Enum):
    CANDIDATE = "candidate"
    ACTIVE_OPERATIONAL = "active_operational"
    CANONICAL = "canonical"


@dataclass(frozen=True, slots=True)
class PromotionDecision:
    capability_id: str
    state: PromotionState
    operationally_active: bool
    canonical_eligible: bool
    reasons: tuple[str, ...] = ()


def evaluate_promotion(
    evidence: NativeEvidence,
    *,
    provenance_passed: bool,
    governance_complete: bool,
    core_pillar_relevance: bool = False,
    evolution_gate_approved: bool = False,
) -> PromotionDecision:
    """Evaluate promotion without silently mutating canonical knowledge."""
    if evidence.capability_id not in CAPABILITY_IDS:
        raise ValueError(f"unknown capability: {evidence.capability_id}")

    reasons: list[str] = []
    operational = evidence.status == "completed" and all(evidence.outcome.values())
    if not operational:
        reasons.append("controlled native functional proof is not green")
    if not provenance_passed:
        reasons.append("provenance is incomplete")
    if not governance_complete:
        reasons.append("governance metadata is incomplete")

    if not operational or not provenance_passed or not governance_complete:
        return PromotionDecision(evidence.capability_id, PromotionState.CANDIDATE, False, False, tuple(reasons))

    canonical = core_pillar_relevance and evolution_gate_approved
    if canonical:
        return PromotionDecision(evidence.capability_id, PromotionState.CANONICAL, True, True, ())

    if not core_pillar_relevance:
        reasons.append("no explicit Core-pillar relevance established")
    if not evolution_gate_approved:
        reasons.append("Evolution Gate approval not established")
    return PromotionDecision(evidence.capability_id, PromotionState.ACTIVE_OPERATIONAL, True, False, tuple(reasons))


def evaluate_all_candidates(
    *,
    request_prefix: str = "PROMOTION-TEST",
    tenant_scope: str = "elo-lab",
    provenance_passed: bool = True,
    governance_complete: bool = True,
) -> tuple[PromotionDecision, ...]:
    """Run the first operational promotion test against all eight native probes."""
    from .native_capabilities import execute_candidate

    decisions = []
    for capability_id in CAPABILITY_IDS:
        evidence = execute_candidate(
            capability_id,
            request_id=f"{request_prefix}-{capability_id}",
            tenant_scope=tenant_scope,
        )
        decisions.append(
            evaluate_promotion(
                evidence,
                provenance_passed=provenance_passed,
                governance_complete=governance_complete,
            )
        )
    return tuple(decisions)


__all__ = ["PromotionDecision", "PromotionState", "evaluate_promotion", "evaluate_all_candidates"]
