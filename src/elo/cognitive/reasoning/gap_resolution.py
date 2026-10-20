"""Governed post-assessment resolution planning for requirement gaps.

This module does not repeat the canonical automatic resolution flow, call a
provider, select a specialist, persist state, authorize work, or execute an
action. It translates the final epistemic state of one
``RequirementResolutionResult`` into a bounded next-resolution action that can
be handed to existing ELO owners.

The boundary is fail-closed: unresolved states remain explicit, confirmed gaps
request new evidence instead of fabricating values, conflicts require
investigation, assumptions require governed review, and any pending human gate
prevents an automatic-resolved disposition.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping, Sequence

from .requirement_analysis import (
    RequirementState,
    ResolutionAttemptKind,
    ResolutionAttemptStatus,
)
from .requirement_resolution import RequirementResolutionResult


class GapResolutionStatus(StrEnum):
    RESOLVED = "RESOLVED"
    CONTINUE_RESOLUTION = "CONTINUE_RESOLUTION"
    HANDOFF_REQUIRED = "HANDOFF_REQUIRED"


class GapResolutionAction(StrEnum):
    NONE = "NONE"
    CONTINUE_CANONICAL_RESOLUTION = "CONTINUE_CANONICAL_RESOLUTION"
    REQUEST_NEW_EVIDENCE = "REQUEST_NEW_EVIDENCE"
    VALIDATE_INFERENCE = "VALIDATE_INFERENCE"
    REVIEW_GOVERNED_ASSUMPTION = "REVIEW_GOVERNED_ASSUMPTION"
    INVESTIGATE_CONFLICT = "INVESTIGATE_CONFLICT"
    REVIEW_HUMAN_GATE = "REVIEW_HUMAN_GATE"


_CANONICAL_ATTEMPT_ORDER = (
    ResolutionAttemptKind.RETRIEVAL,
    ResolutionAttemptKind.RULE,
    ResolutionAttemptKind.CALCULATION,
    ResolutionAttemptKind.INFERENCE,
)
_AUTOMATIC_RESOLVED_STATES = frozenset(
    {
        RequirementState.KNOWN,
        RequirementState.DOCUMENTED,
        RequirementState.RETRIEVED,
        RequirementState.CALCULATED,
    }
)
_HANDOFF_ACTIONS = frozenset(
    {
        GapResolutionAction.REQUEST_NEW_EVIDENCE,
        GapResolutionAction.VALIDATE_INFERENCE,
        GapResolutionAction.REVIEW_GOVERNED_ASSUMPTION,
        GapResolutionAction.INVESTIGATE_CONFLICT,
        GapResolutionAction.REVIEW_HUMAN_GATE,
    }
)
_SCOPE_KEYS = frozenset(
    {
        "retrieval.tenant_id",
        "retrieval.domain",
        "retrieval.principal_id",
        "retrieval.session_id",
        "retrieval.request_id",
        "retrieval.correlation_id",
        "retrieval.source_id",
        "retrieval.source_kind",
        "retrieval.required_capability",
        "retrieval.authorization_scope",
    }
)


@dataclass(frozen=True, slots=True)
class GapResolutionPlan:
    requirement_id: str
    parameter: str
    assessment_state: RequirementState
    status: GapResolutionStatus
    action: GapResolutionAction
    evidence_ids: tuple[str, ...] = ()
    executed_attempts: tuple[ResolutionAttemptKind, ...] = ()
    unexecuted_attempts: tuple[ResolutionAttemptKind, ...] = ()
    handoff_required: bool = False
    human_validation_required: bool = False
    scope_context: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.requirement_id.strip():
            raise ValueError("gap resolution plan requires requirement_id")
        if not self.parameter or not self.parameter.strip():
            raise ValueError("gap resolution plan requires parameter")
        if set(self.scope_context) - _SCOPE_KEYS:
            raise ValueError("gap resolution plan contains unsafe scope keys")
        if any(not str(value).strip() for value in self.scope_context.values()):
            raise ValueError("gap resolution scope values must be nonblank")

        _validate_plan_attempt_partition(
            executed=self.executed_attempts,
            unexecuted=self.unexecuted_attempts,
        )

        if self.status is GapResolutionStatus.RESOLVED:
            if self.action is not GapResolutionAction.NONE:
                raise ValueError("resolved gap plan cannot request another action")
            if self.handoff_required or self.human_validation_required:
                raise ValueError("resolved gap plan cannot retain a human/handoff gate")
        elif self.status is GapResolutionStatus.CONTINUE_RESOLUTION:
            if self.action is not GapResolutionAction.CONTINUE_CANONICAL_RESOLUTION:
                raise ValueError("continue-resolution status requires canonical resolution action")
            if not self.unexecuted_attempts:
                raise ValueError("continue-resolution status requires unexecuted attempts")
            if self.handoff_required:
                raise ValueError("canonical resolution continuation is not a handoff")
        elif self.status is GapResolutionStatus.HANDOFF_REQUIRED:
            if not self.handoff_required:
                raise ValueError("handoff-required status must set handoff_required")
            if self.action not in _HANDOFF_ACTIONS:
                raise ValueError("handoff-required status requires a governed handoff action")

    @property
    def can_execute(self) -> bool:
        """Planning never grants execution authority."""
        return False


def plan_gap_resolution(result: RequirementResolutionResult) -> GapResolutionPlan:
    """Translate one canonical requirement result into its next governed action."""
    assessment = result.assessment
    executed = _validate_result_attempt_trace(result)
    unexecuted = tuple(kind for kind in _CANONICAL_ATTEMPT_ORDER if kind not in executed)
    evidence_ids = _clean_ids(assessment.evidence_ids)
    scope_context = dict(result.scope_context)

    if assessment.state in _AUTOMATIC_RESOLVED_STATES:
        if assessment.human_validation_required:
            return _handoff_plan(
                result=result,
                action=GapResolutionAction.REVIEW_HUMAN_GATE,
                evidence_ids=evidence_ids,
                executed=executed,
                unexecuted=unexecuted,
                human_validation_required=True,
                scope_context=scope_context,
            )
        return GapResolutionPlan(
            requirement_id=result.requirement_id,
            parameter=result.parameter,
            assessment_state=assessment.state,
            status=GapResolutionStatus.RESOLVED,
            action=GapResolutionAction.NONE,
            evidence_ids=evidence_ids,
            executed_attempts=executed,
            unexecuted_attempts=unexecuted,
            scope_context=scope_context,
        )

    if assessment.state is RequirementState.GAP_CANDIDATE:
        if assessment.human_validation_required:
            return _handoff_plan(
                result=result,
                action=GapResolutionAction.REVIEW_HUMAN_GATE,
                evidence_ids=evidence_ids,
                executed=executed,
                unexecuted=unexecuted,
                human_validation_required=True,
                scope_context=scope_context,
            )
        if not unexecuted:
            raise ValueError(
                "GAP_CANDIDATE is inconsistent after every canonical resolution attempt executes"
            )
        return GapResolutionPlan(
            requirement_id=result.requirement_id,
            parameter=result.parameter,
            assessment_state=assessment.state,
            status=GapResolutionStatus.CONTINUE_RESOLUTION,
            action=GapResolutionAction.CONTINUE_CANONICAL_RESOLUTION,
            evidence_ids=evidence_ids,
            executed_attempts=executed,
            unexecuted_attempts=unexecuted,
            human_validation_required=False,
            scope_context=scope_context,
        )

    if assessment.state is RequirementState.GAP_CONFIRMED:
        if unexecuted:
            raise ValueError(
                "GAP_CONFIRMED is invalid before every canonical resolution attempt executes"
            )
        if any(attempt.status is ResolutionAttemptStatus.RESOLVED for attempt in result.attempts):
            raise ValueError(
                "GAP_CONFIRMED is invalid when a canonical resolution attempt is RESOLVED"
            )
        return _handoff_plan(
            result=result,
            action=GapResolutionAction.REQUEST_NEW_EVIDENCE,
            evidence_ids=evidence_ids,
            executed=executed,
            unexecuted=(),
            human_validation_required=True,
            scope_context=scope_context,
        )

    if assessment.state is RequirementState.HUMAN_VALIDATION_REQUIRED:
        return _handoff_plan(
            result=result,
            action=GapResolutionAction.REVIEW_HUMAN_GATE,
            evidence_ids=evidence_ids,
            executed=executed,
            unexecuted=unexecuted,
            human_validation_required=True,
            scope_context=scope_context,
        )

    if assessment.state is RequirementState.INFERRED:
        return _handoff_plan(
            result=result,
            action=GapResolutionAction.VALIDATE_INFERENCE,
            evidence_ids=evidence_ids,
            executed=executed,
            unexecuted=unexecuted,
            human_validation_required=True,
            scope_context=scope_context,
        )

    if assessment.state is RequirementState.ASSUMPTION_REQUIRED:
        return _handoff_plan(
            result=result,
            action=GapResolutionAction.REVIEW_GOVERNED_ASSUMPTION,
            evidence_ids=evidence_ids,
            executed=executed,
            unexecuted=unexecuted,
            human_validation_required=True,
            scope_context=scope_context,
        )

    if assessment.state is RequirementState.CONFLICT:
        return _handoff_plan(
            result=result,
            action=GapResolutionAction.INVESTIGATE_CONFLICT,
            evidence_ids=evidence_ids,
            executed=executed,
            unexecuted=unexecuted,
            human_validation_required=True,
            scope_context=scope_context,
        )

    if assessment.state is RequirementState.MISSING:
        return _handoff_plan(
            result=result,
            action=GapResolutionAction.REQUEST_NEW_EVIDENCE,
            evidence_ids=evidence_ids,
            executed=executed,
            unexecuted=unexecuted,
            human_validation_required=assessment.human_validation_required,
            scope_context=scope_context,
        )

    raise ValueError(f"unsupported requirement state for gap resolution: {assessment.state.value}")


def audit_gap_resolution_plan(plan: GapResolutionPlan) -> Mapping[str, object]:
    """Return a bounded audit trace without private reasoning or arbitrary metadata."""
    return {
        "requirement_id": plan.requirement_id,
        "parameter": plan.parameter,
        "assessment_state": plan.assessment_state.value,
        "status": plan.status.value,
        "action": plan.action.value,
        "evidence_ids": plan.evidence_ids,
        "executed_attempts": tuple(kind.value for kind in plan.executed_attempts),
        "unexecuted_attempts": tuple(kind.value for kind in plan.unexecuted_attempts),
        "handoff_required": plan.handoff_required,
        "human_validation_required": plan.human_validation_required,
        "scope_context": dict(plan.scope_context),
        "can_execute": plan.can_execute,
    }


def _handoff_plan(
    *,
    result: RequirementResolutionResult,
    action: GapResolutionAction,
    evidence_ids: tuple[str, ...],
    executed: tuple[ResolutionAttemptKind, ...],
    unexecuted: tuple[ResolutionAttemptKind, ...],
    human_validation_required: bool,
    scope_context: Mapping[str, str],
) -> GapResolutionPlan:
    return GapResolutionPlan(
        requirement_id=result.requirement_id,
        parameter=result.parameter,
        assessment_state=result.assessment.state,
        status=GapResolutionStatus.HANDOFF_REQUIRED,
        action=action,
        evidence_ids=evidence_ids,
        executed_attempts=executed,
        unexecuted_attempts=unexecuted,
        handoff_required=True,
        human_validation_required=human_validation_required,
        scope_context=scope_context,
    )


def _validate_result_attempt_trace(
    result: RequirementResolutionResult,
) -> tuple[ResolutionAttemptKind, ...]:
    kinds = tuple(attempt.kind for attempt in result.attempts)
    if len(kinds) != len(set(kinds)):
        raise ValueError("requirement resolution contains duplicate canonical attempt kinds")
    canonical_subsequence = tuple(kind for kind in _CANONICAL_ATTEMPT_ORDER if kind in kinds)
    if kinds != canonical_subsequence:
        raise ValueError("requirement resolution attempts are not in canonical order")
    return kinds


def _validate_plan_attempt_partition(
    *,
    executed: Sequence[ResolutionAttemptKind],
    unexecuted: Sequence[ResolutionAttemptKind],
) -> None:
    executed_tuple = tuple(executed)
    unexecuted_tuple = tuple(unexecuted)
    if len(executed_tuple) != len(set(executed_tuple)):
        raise ValueError("gap resolution plan contains duplicate executed attempts")
    if len(unexecuted_tuple) != len(set(unexecuted_tuple)):
        raise ValueError("gap resolution plan contains duplicate unexecuted attempts")
    if set(executed_tuple).intersection(unexecuted_tuple):
        raise ValueError("executed and unexecuted attempts must be disjoint")
    if tuple(kind for kind in _CANONICAL_ATTEMPT_ORDER if kind in executed_tuple) != executed_tuple:
        raise ValueError("executed attempts must preserve canonical order")
    if tuple(kind for kind in _CANONICAL_ATTEMPT_ORDER if kind in unexecuted_tuple) != unexecuted_tuple:
        raise ValueError("unexecuted attempts must preserve canonical order")
    if set(executed_tuple).union(unexecuted_tuple) != set(_CANONICAL_ATTEMPT_ORDER):
        raise ValueError("executed and unexecuted attempts must partition the canonical order")


def _clean_ids(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            cleaned for value in values if (cleaned := str(value).strip())
        )
    )
