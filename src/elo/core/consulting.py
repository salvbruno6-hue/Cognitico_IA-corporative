"""Canonical consulting-response contract for the ELO Cognitive Core."""

from dataclasses import dataclass, field
from typing import Literal


ConsultingStatus = Literal["ANALYSIS", "RECOMMENDATION", "DECISION_REQUIRED", "INSUFFICIENT_EVIDENCE"]


@dataclass(frozen=True)
class ConsultingResponse:
    """Structured result expected from ELO consulting mode.

    The contract keeps analysis separate from recommendation and human decision.
    It does not itself authorize an action or modify ELO Soul.
    """

    objective: str
    context: tuple[str, ...] = ()
    facts: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    analysis: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    recommendation: str | None = None
    decision_required: str | None = None
    next_actions: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    status: ConsultingStatus = "ANALYSIS"
    uncertainty: tuple[str, ...] = ()

    def is_actionable(self) -> bool:
        """Return whether the response contains a recommendation or required decision."""
        return bool(self.recommendation or self.decision_required)

    def summary_sections(self) -> dict[str, object]:
        """Return the stable consultant presentation contract."""
        return {
            "objective": self.objective,
            "context": self.context,
            "facts": self.facts,
            "evidence": self.evidence,
            "assumptions": self.assumptions,
            "analysis": self.analysis,
            "alternatives": self.alternatives,
            "risks": self.risks,
            "recommendation": self.recommendation,
            "decision_required": self.decision_required,
            "next_actions": self.next_actions,
            "provenance": self.provenance,
            "status": self.status,
            "uncertainty": self.uncertainty,
        }
