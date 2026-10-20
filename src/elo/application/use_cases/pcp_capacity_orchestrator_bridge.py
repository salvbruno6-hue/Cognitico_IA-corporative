"""Bridge governed PCP expansion evidence into Orchestrator-facing guidance.

The bridge does not execute changes. It converts a cognitive expansion
assessment into bounded actions that the canonical Orchestrator may surface or
handoff for authorization/execution.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.pcp_capacity_expansion import CapacityExpansionAssessment


@dataclass(frozen=True, slots=True)
class PCPOrchestratorAction:
    target: str
    action: str
    authorization_required: bool
    reason: str
    evidence_required: tuple[str, ...]


class PCPCapacityOrchestratorBridge:
    """Translate capacity reasoning into non-mutating orchestration guidance."""

    _MUTATING_ACTIONS = {
        "EMITIR_NECESSIDADE_COMPRAS",
        "AUMENTAR_CAPACIDADE_RECURSO",
    }

    def orient(self, assessment: CapacityExpansionAssessment) -> tuple[PCPOrchestratorAction, ...]:
        actions: list[PCPOrchestratorAction] = []
        for item in assessment.actions:
            actions.append(
                PCPOrchestratorAction(
                    target=item.target,
                    action=item.action,
                    authorization_required=item.action in self._MUTATING_ACTIONS,
                    reason=item.reason,
                    evidence_required=item.evidence_required,
                )
            )
        return tuple(actions)


__all__ = ["PCPCapacityOrchestratorBridge", "PCPOrchestratorAction"]
