"""Governed critical reasoning for evidence gaps.

This module does not resolve requirements and does not create evidence. It sits
*after* the canonical requirement-resolution flow has identified missing or
insufficient conditions and helps the Orchestrator decide which evidence gap
should be investigated next.

The capability is intentionally deterministic and fail-closed:

- a missing field is linked to the decision it affects;
- operational impact and collection action stay explicit;
- observations may remain usable as historical evidence without becoming a
  canonical rule;
- hiring, purchasing or capacity changes are never authorized by this module;
- priority is derived from declared decision criticality, sensitivity and
  collection effort, never from invented business values.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Iterable, Sequence


class GapCriticality(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class GapPlanState(StrEnum):
    READY = "READY"
    DECISION_BLOCKED = "DECISION_BLOCKED"
    NO_GAPS = "NO_GAPS"


class ObservationUse(StrEnum):
    HISTORICAL_EVIDENCE = "HISTORICAL_EVIDENCE"
    SCENARIO_INPUT = "SCENARIO_INPUT"
    CANONICAL_RULE = "CANONICAL_RULE"


@dataclass(frozen=True, slots=True)
class CriticalEvidenceGap:
    gap_id: str
    parameter: str
    decision: str
    missing_condition: str
    operational_impact: str
    collection_action: str
    owner: str
    criticality: GapCriticality
    decision_sensitivity: int = 3
    collection_effort: int = 3
    blocks_decision: bool = True
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        required = (
            self.gap_id,
            self.parameter,
            self.decision,
            self.missing_condition,
            self.operational_impact,
            self.collection_action,
            self.owner,
        )
        if not all(value.strip() for value in required):
            raise ValueError("critical evidence gap requires nonblank semantic fields")
        if not 1 <= self.decision_sensitivity <= 5:
            raise ValueError("decision_sensitivity must be between 1 and 5")
        if not 1 <= self.collection_effort <= 5:
            raise ValueError("collection_effort must be between 1 and 5")
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs cannot contain blank values")

    @property
    def priority_score(self) -> int:
        """Rank evidence collection without inventing operational quantities."""
        blocker = 100 if self.blocks_decision else 0
        return (
            blocker
            + int(self.criticality) * 20
            + self.decision_sensitivity * 5
            - self.collection_effort
        )


@dataclass(frozen=True, slots=True)
class ObservationBoundary:
    observation_id: str
    statement: str
    source_ref: str
    allowed_uses: tuple[ObservationUse, ...]
    missing_context: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.observation_id.strip() or not self.statement.strip():
            raise ValueError("observation requires id and statement")
        if not self.source_ref.strip():
            raise ValueError("observation requires source_ref")
        if not self.allowed_uses:
            raise ValueError("observation requires at least one allowed use")
        if (
            ObservationUse.CANONICAL_RULE in self.allowed_uses
            and self.missing_context
        ):
            raise ValueError(
                "observation with missing context cannot be authorized as canonical rule"
            )

    @property
    def canonicalizable(self) -> bool:
        return (
            ObservationUse.CANONICAL_RULE in self.allowed_uses
            and not self.missing_context
        )


@dataclass(frozen=True, slots=True)
class CriticalGapPlan:
    state: GapPlanState
    ordered_gaps: tuple[CriticalEvidenceGap, ...]
    next_gap: CriticalEvidenceGap | None
    blocked_decisions: tuple[str, ...]
    canonical_mutation: bool = False


@dataclass(frozen=True, slots=True)
class AdminDecisionQuestion:
    """Presentation of a proven evidence gap for the authorized administrator."""

    question_id: str
    gap_id: str
    parameter: str
    decision: str
    prompt: str
    why_needed: str
    response_guidance: str
    owner: str
    priority_score: int
    blocks_decision: bool
    evidence_refs: tuple[str, ...] = ()
    answer_contract: str = "HUMAN_EVIDENCE_CANDIDATE"

    def to_payload(self) -> dict[str, object]:
        return {
            "question_id": self.question_id,
            "gap_id": self.gap_id,
            "parameter": self.parameter,
            "decision": self.decision,
            "prompt": self.prompt,
            "why_needed": self.why_needed,
            "response_guidance": self.response_guidance,
            "owner": self.owner,
            "priority_score": self.priority_score,
            "blocks_decision": self.blocks_decision,
            "evidence_refs": list(self.evidence_refs),
            "answer_contract": self.answer_contract,
        }


def build_admin_decision_questionnaire(
    plan: CriticalGapPlan,
    *,
    max_questions: int = 5,
    include_non_blocking: bool = False,
) -> tuple[AdminDecisionQuestion, ...]:
    """Project existing gaps into questions; never synthesize missing business facts."""
    if not 1 <= max_questions <= 20:
        raise ValueError("max_questions must be between 1 and 20")
    eligible = (
        plan.ordered_gaps
        if include_non_blocking
        else tuple(gap for gap in plan.ordered_gaps if gap.blocks_decision)
    )
    return tuple(
        AdminDecisionQuestion(
            question_id=f"ADM-{gap.gap_id}",
            gap_id=gap.gap_id,
            parameter=gap.parameter,
            decision=gap.decision,
            prompt=(
                f'Para concluir a decisão "{gap.decision}", informe ou valide: '
                f"{gap.missing_condition}"
            ),
            why_needed=gap.operational_impact,
            response_guidance=gap.collection_action,
            owner=gap.owner,
            priority_score=gap.priority_score,
            blocks_decision=gap.blocks_decision,
            evidence_refs=gap.evidence_refs,
        )
        for gap in eligible[:max_questions]
    )


def prioritize_evidence_gaps(
    gaps: Iterable[CriticalEvidenceGap],
) -> CriticalGapPlan:
    """Prioritize the next evidence to collect for an Orchestrator handoff."""
    unique: dict[str, CriticalEvidenceGap] = {}
    for gap in gaps:
        if gap.gap_id in unique and unique[gap.gap_id] != gap:
            raise ValueError(f"conflicting definitions for gap_id={gap.gap_id}")
        unique[gap.gap_id] = gap

    ordered = tuple(
        sorted(
            unique.values(),
            key=lambda item: (-item.priority_score, item.gap_id),
        )
    )
    if not ordered:
        return CriticalGapPlan(
            state=GapPlanState.NO_GAPS,
            ordered_gaps=(),
            next_gap=None,
            blocked_decisions=(),
        )

    blocked = tuple(
        dict.fromkeys(gap.decision for gap in ordered if gap.blocks_decision)
    )
    return CriticalGapPlan(
        state=(
            GapPlanState.DECISION_BLOCKED if blocked else GapPlanState.READY
        ),
        ordered_gaps=ordered,
        next_gap=ordered[0],
        blocked_decisions=blocked,
    )


def qualify_observation(
    *,
    observation_id: str,
    statement: str,
    source_ref: str,
    missing_context: Sequence[str] = (),
    allow_scenario: bool = True,
    authorize_canonical_rule: bool = False,
) -> ObservationBoundary:
    """Keep empirical observations useful without silently promoting them."""
    cleaned_context = tuple(
        dict.fromkeys(value.strip() for value in missing_context if value.strip())
    )
    uses = [ObservationUse.HISTORICAL_EVIDENCE]
    if allow_scenario:
        uses.append(ObservationUse.SCENARIO_INPUT)
    if authorize_canonical_rule:
        if cleaned_context:
            raise ValueError(
                "cannot authorize canonical rule while contextual evidence is missing"
            )
        uses.append(ObservationUse.CANONICAL_RULE)
    return ObservationBoundary(
        observation_id=observation_id,
        statement=statement,
        source_ref=source_ref,
        allowed_uses=tuple(uses),
        missing_context=cleaned_context,
    )


__all__ = [
    "CriticalEvidenceGap",
    "CriticalGapPlan",
    "AdminDecisionQuestion",
    "build_admin_decision_questionnaire",
    "GapCriticality",
    "GapPlanState",
    "ObservationBoundary",
    "ObservationUse",
    "prioritize_evidence_gaps",
    "qualify_observation",
]
