"""Governed ELO -> GPT specialist handoff contract.

The ELO remains responsible for systemic interpretation and decision support.
GPT is consulted as a specialist. The response never authorizes a canonical
change and is first treated as temporal/external evidence.
"""

from dataclasses import dataclass
from typing import Literal

from .context_resolution import ContextPack
from .maturity_engine import MaturityAssessment


HandoffMode = Literal["DISCOVERY_ASSIST", "SPECIALIST_VALIDATION"]


@dataclass(frozen=True)
class GPTDecisionHandoff:
    question: str
    objective: str
    mode: HandoffMode
    elo_analysis: tuple[str, ...] = ()
    dimensions_to_check: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    context_entity: str | None = None
    context_scope: str | None = None
    context_uncertainties: tuple[str, ...] = ()
    decision_required: bool = False
    correlation_id: str = ""

    @classmethod
    def from_maturity(
        cls,
        *,
        question: str,
        objective: str,
        maturity: MaturityAssessment,
        elo_analysis: tuple[str, ...] = (),
        dimensions_to_check: tuple[str, ...] = (),
        evidence_ids: tuple[str, ...] = (),
        decision_required: bool = False,
        correlation_id: str = "",
    ) -> "GPTDecisionHandoff":
        return cls(
            question=question,
            objective=objective,
            mode=maturity.mode,
            elo_analysis=elo_analysis,
            dimensions_to_check=dimensions_to_check,
            evidence_ids=evidence_ids,
            decision_required=decision_required,
            correlation_id=correlation_id,
        )

    @classmethod
    def from_context(
        cls,
        *,
        objective: str,
        context: ContextPack,
        maturity: MaturityAssessment,
        elo_analysis: tuple[str, ...] = (),
        decision_required: bool = False,
        correlation_id: str = "",
    ) -> "GPTDecisionHandoff":
        if not context.discovery_plan:
            raise ValueError("context discovery must run before GPT handoff")
        if maturity.mode == "SPECIALIST_VALIDATION" and not context.requires_specialist():
            raise ValueError("specialist validation requires scoped evidence")
        return cls(
            question=context.query.question,
            objective=objective,
            mode=maturity.mode,
            elo_analysis=elo_analysis,
            dimensions_to_check=context.query.dimensions,
            evidence_ids=context.evidence_ids(),
            context_entity=context.query.entity,
            context_scope=context.query.scope,
            context_uncertainties=context.uncertainties,
            decision_required=decision_required,
            correlation_id=correlation_id,
        )

    def specialist_instruction(self) -> str:
        if self.mode == "SPECIALIST_VALIDATION":
            return (
                "Answer only the specialist question, then identify risks, assumptions, "
                "contradictions, evidence gaps and implications that the ELO should evaluate "
                "across other decision dimensions. Do not make or authorize the final decision."
            )
        return (
            "Provide discovery-oriented analysis and identify missing context, evidence and "
            "specialist considerations. Do not treat the response as canonical knowledge."
        )
