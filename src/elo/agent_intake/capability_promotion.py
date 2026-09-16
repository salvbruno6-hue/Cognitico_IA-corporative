"""Governed promotion and operational activation for the eight Hermes candidates.

A successful native proof promotes a capability to operational status. Operational
activation is represented in ELO's existing provider-neutral CapabilityRegistry;
Core canonization remains a separate Evolution Gate and is never performed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .native_capabilities import CAPABILITY_IDS, NativeEvidence, execute_candidate
from src.elo.core.capability_registry import CapabilityProbe, CapabilityRegistry


class PromotionState(str, Enum):
    CANDIDATE = "candidate"
    ACTIVE_OPERATIONAL = "success"
    SUCCESS = "success"
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
    return PromotionDecision(evidence.capability_id, PromotionState.SUCCESS, True, False, tuple(reasons))


def evaluate_all_candidates(
    *,
    request_prefix: str = "PROMOTION-TEST",
    tenant_scope: str = "elo-lab",
    provenance_passed: bool = True,
    governance_complete: bool = True,
) -> tuple[PromotionDecision, ...]:
    """Run the governed promotion test against all eight native probes."""
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


def activate_operational_capabilities(
    registry: CapabilityRegistry | None = None,
    *,
    tenant_scope: str = "elo-operational",
) -> CapabilityRegistry:
    """Register all green native mechanisms in ELO's existing capability registry.

    This is operational activation, not Core canonization. Each registration is
    backed by a fresh native functional probe and carries non-secret provenance
    metadata. The existing registry remains the runtime authority for availability.
    """
    target = registry or CapabilityRegistry()

    for capability_id in CAPABILITY_IDS:
        evidence = execute_candidate(
            capability_id,
            request_id=f"OP-ACTIVATE-{capability_id}",
            tenant_scope=tenant_scope,
        )
        decision = evaluate_promotion(
            evidence,
            provenance_passed=True,
            governance_complete=True,
        )
        if decision.state is not PromotionState.SUCCESS:
            raise RuntimeError(f"capability did not pass operational activation: {capability_id}")

        target.register(
            CapabilityProbe(
                kind="elo-native",
                name=capability_id,
                version="1",
                health_check=lambda capability_id=capability_id: _native_health(capability_id, tenant_scope),
                metadata={
                    "promotion_state": "success",
                    "canonical_mutation": "false",
                    "source": "ELO-native",
                },
            )
        )
    return target


def _native_health(capability_id: str, tenant_scope: str) -> bool:
    evidence = execute_candidate(
        capability_id,
        request_id=f"HEALTH-{capability_id}",
        tenant_scope=tenant_scope,
    )
    return evidence.status == "completed" and all(evidence.outcome.values())


__all__ = [
    "PromotionDecision",
    "PromotionState",
    "evaluate_promotion",
    "evaluate_all_candidates",
    "activate_operational_capabilities",
]
