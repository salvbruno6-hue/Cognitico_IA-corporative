"""Governed ELO -> GPT specialist handoff contract.

The ELO remains responsible for systemic interpretation and decision support.
GPT is consulted as a specialist. The response never authorizes a canonical
change and is first treated as temporal/external evidence.
"""

from dataclasses import dataclass, field
from typing import Literal, Mapping

from .context_resolution import ContextPack
from .maturity_engine import MaturityAssessment
from .specialist_skill_resolution import SpecialistSkillResolution


HandoffMode = Literal["DISCOVERY_ASSIST", "SPECIALIST_VALIDATION"]


@dataclass(frozen=True)
class ConsultativeReturn:
    """Bounded GPT return contract; it is evidence for ELO evaluation, not authority."""

    status: str
    classification: str
    confidence: float
    evidence: tuple[str, ...] = ()
    compatible_elements: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    recommended_adjustments: tuple[str, ...] = ()
    rejected_elements: tuple[str, ...] = ()
    future_candidates: tuple[str, ...] = ()
    human_decision_required: bool = False
    decision_question: str | None = None
    recommended_action: str | None = None
    provenance: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


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
    context_gaps: tuple[str, ...] = ()
    decision_required: bool = False
    correlation_id: str = ""
    tenant_id: str | None = None
    domain: str | None = None
    principal_id: str | None = None
    request_id: str | None = None
    skill_id: str | None = None

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
        skill_resolution: SpecialistSkillResolution | None = None,
    ) -> "GPTDecisionHandoff":
        if not context.discovery_plan:
            raise ValueError("context discovery must run before GPT handoff")
        if maturity.mode == "SPECIALIST_VALIDATION" and not context.requires_specialist():
            raise ValueError("specialist validation requires scoped evidence")
        if maturity.mode == "SPECIALIST_VALIDATION":
            if skill_resolution is None or not skill_resolution.resolved:
                raise ValueError("specialist validation requires a resolved governed skill")
            if context.query.domain != skill_resolution.domain_family:
                raise ValueError("resolved specialist skill domain does not match context domain")
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
            context_gaps=context.integrity_gaps(),
            decision_required=decision_required or bool(context.integrity_gaps()),
            correlation_id=correlation_id or (context.query.correlation_id or ""),
            tenant_id=context.query.tenant_id,
            domain=context.query.domain,
            principal_id=context.query.principal_id,
            request_id=context.query.request_id,
            skill_id=skill_resolution.skill_id if skill_resolution is not None else None,
        )

    def consultation_payload(self) -> Mapping[str, object]:
        """Return only resolved context and governance metadata, never private reasoning."""
        return {
            "question": self.question,
            "objective": self.objective,
            "mode": self.mode,
            "dimensions_to_check": self.dimensions_to_check,
            "evidence_ids": self.evidence_ids,
            "context_entity": self.context_entity,
            "context_scope": self.context_scope,
            "context_uncertainties": self.context_uncertainties,
            "context_gaps": self.context_gaps,
            "decision_required": self.decision_required,
            "tenant_id": self.tenant_id,
            "domain": self.domain,
            "principal_id": self.principal_id,
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "skill_id": self.skill_id,
            "specialist_instruction": self.specialist_instruction(),
        }

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
