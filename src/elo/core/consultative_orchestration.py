"""Provider-neutral orchestration for the existing ELO→GPT consultative contract."""
from dataclasses import dataclass
from typing import Callable

from elo.cognitive.reasoning.analytical_refinement import (
    AnalyticalRefinementSignals,
    select_analytical_refinement,
)

from .context_resolution import ContextPack
from .gpt_handoff import ConsultativeReturn, GPTDecisionHandoff
from .maturity_engine import MaturityAssessment


@dataclass(frozen=True)
class ConsultativeOutcome:
    handoff: GPTDecisionHandoff
    result: ConsultativeReturn | None
    status: str


_RISKY_TEMPORAL_VALIDITY = {
    "historical",
    "historica",
    "histórica",
    "theoretical",
    "teorica",
    "teórica",
    "stale",
    "expired",
    "legacy",
}


def _context_temporal_risks(context: ContextPack) -> tuple[str, ...]:
    """Return only explicitly classified risky temporal states.

    Arbitrary dates/windows are not interpreted here. This prevents the
    orchestrator from inventing temporal semantics from free-form values.
    """
    risks: list[str] = []
    for source in context.scoped_sources():
        value = (source.temporal_validity or "").strip().lower()
        if value in _RISKY_TEMPORAL_VALIDITY:
            risks.append(f"source:{source.source_id}:{value}")
    for evidence in context.scoped_evidence():
        value = (evidence.temporal_validity or "").strip().lower()
        if value in _RISKY_TEMPORAL_VALIDITY:
            risks.append(f"evidence:{evidence.source_id}:{value}")
    return tuple(dict.fromkeys(risks))


class ConsultativeOrchestrator:
    """Builds bounded handoffs and validates returns; it cannot mutate canonical state."""

    def prepare(
        self,
        *,
        context: ContextPack,
        maturity: MaturityAssessment,
        objective: str,
        decision_required: bool = False,
        consequential_action: bool = False,
        analytical_conflicts: tuple[str, ...] = (),
        temporal_risks: tuple[str, ...] = (),
    ) -> GPTDecisionHandoff:
        """Prepare a handoff and select EAIF refinement only when signals justify it.

        The selector consumes structured context/governance signals. It does not
        infer risk from keywords in the user's question and does not change model,
        tool, domain or action authority.
        """
        integrity_gaps = context.integrity_gaps()
        effective_decision_required = decision_required or bool(integrity_gaps)
        detected_temporal_risks = tuple(dict.fromkeys(
            _context_temporal_risks(context) + temporal_risks
        ))
        scoped_evidence = context.scoped_evidence()
        refinement = select_analytical_refinement(AnalyticalRefinementSignals(
            decision_required=effective_decision_required,
            consequential_action=consequential_action,
            integrity_gaps=integrity_gaps,
            uncertainties=context.uncertainties,
            conflicts=analytical_conflicts,
            temporal_risks=detected_temporal_risks,
            weak_evidence=bool(scoped_evidence) and not context.sufficient_evidence(),
        ))
        return GPTDecisionHandoff.from_context(
            objective=objective,
            context=context,
            maturity=maturity,
            decision_required=effective_decision_required,
            analytical_refinement=refinement.level.value,
            analytical_refinement_reasons=refinement.reasons,
            analytical_checks=refinement.checks,
        )

    def consult(self, handoff: GPTDecisionHandoff,
                provider: Callable[[dict], ConsultativeReturn]) -> ConsultativeOutcome:
        result = provider(dict(handoff.consultation_payload()))
        if result.provenance.get("canonical_authority") == "true":
            raise ValueError("consultative provider cannot claim canonical authority")
        return ConsultativeOutcome(handoff=handoff, result=result, status="RETURNED")
