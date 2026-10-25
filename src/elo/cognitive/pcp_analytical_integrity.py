"""PCP adapter for the transversal ELO analytical-integrity guard.

Owner: SKILL_PLANEJAMENTO_MULTITEINER / PCP cognitive control
Authority: implementation only

This adapter does not calculate PCP values and does not authorize business
actions. It translates already-classified PCP evidence into the transversal
analytical-integrity contract.
"""
from __future__ import annotations

from elo.cognitive.reasoning.analytical_integrity import (
    EvidenceUse,
    EvidenceUsage,
    IntegrityFinding,
    SourceRole,
    Temporality,
    assess_evidence_usage,
)
from elo.cognitive.reasoning.requirement_analysis import RequirementState


PCP_ANALYTICAL_INTEGRITY_BINDING = {
    "mechanism": "elo_analytical_integrity",
    "role": "guard",
    "owner": "ELO governed reasoning / SKILL_PLANEJAMENTO_MULTITEINER consumer",
    "action": "prevent invalid promotion or use of PCP evidence before recommendation/action",
}


def guard_capacity_claim(
    *,
    subject: str,
    state: RequirementState,
    capacity_kind: str,
) -> tuple[IntegrityFinding, ...]:
    """Guard a PCP capacity value before presenting it as current capacity."""
    normalized = capacity_kind.strip().upper()
    temporality = {
        "ATUAL": Temporality.CURRENT,
        "CURRENT": Temporality.CURRENT,
        "HISTORICA": Temporality.HISTORICAL,
        "HISTÓRICA": Temporality.HISTORICAL,
        "HISTORICAL": Temporality.HISTORICAL,
        "TEORICA": Temporality.THEORETICAL,
        "TEÓRICA": Temporality.THEORETICAL,
        "THEORETICAL": Temporality.THEORETICAL,
    }.get(normalized, Temporality.UNKNOWN)
    return assess_evidence_usage(EvidenceUsage(
        subject=subject,
        state=state,
        use=EvidenceUse.CURRENT_STATE_CLAIM,
        temporality=temporality,
    ))


def guard_pcp_action_authorization(
    *,
    subject: str,
    state: RequirementState,
    source_role: SourceRole,
) -> tuple[IntegrityFinding, ...]:
    """Keep MRP/capacity evidence separate from authority to execute an action."""
    return assess_evidence_usage(EvidenceUsage(
        subject=subject,
        state=state,
        use=EvidenceUse.ACTION_AUTHORIZATION,
        source_role=source_role,
    ))


__all__ = [
    "PCP_ANALYTICAL_INTEGRITY_BINDING",
    "guard_capacity_claim",
    "guard_pcp_action_authorization",
]
