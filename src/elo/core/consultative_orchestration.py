"""Provider-neutral orchestration for the existing ELO→GPT consultative contract."""
from dataclasses import dataclass
from typing import Callable

from .context_resolution import ContextPack
from .gpt_handoff import ConsultativeReturn, GPTDecisionHandoff
from .maturity_engine import MaturityAssessment


@dataclass(frozen=True)
class ConsultativeOutcome:
    handoff: GPTDecisionHandoff
    result: ConsultativeReturn | None
    status: str


class ConsultativeOrchestrator:
    """Builds bounded handoffs and validates returns; it cannot mutate canonical state."""
    def prepare(self, *, context: ContextPack, maturity: MaturityAssessment,
                objective: str, decision_required: bool = False) -> GPTDecisionHandoff:
        return GPTDecisionHandoff.from_context(
            objective=objective, context=context, maturity=maturity,
            decision_required=decision_required,
        )

    def consult(self, handoff: GPTDecisionHandoff,
                provider: Callable[[dict], ConsultativeReturn]) -> ConsultativeOutcome:
        result = provider(dict(handoff.consultation_payload()))
        if result.provenance.get("canonical_authority") == "true":
            raise ValueError("consultative provider cannot claim canonical authority")
        return ConsultativeOutcome(handoff=handoff, result=result, status="RETURNED")
