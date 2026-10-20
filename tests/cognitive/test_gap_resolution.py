from __future__ import annotations

import pytest

from elo.cognitive.reasoning.gap_resolution import (
    GapResolutionAction,
    GapResolutionStatus,
    audit_gap_resolution_plan,
    plan_gap_resolution,
)
from elo.cognitive.reasoning.requirement_analysis import (
    ConfidenceBand,
    GapAssessment,
    RequirementState,
    ResolutionAttempt,
    ResolutionAttemptKind,
    ResolutionAttemptStatus,
)
from elo.cognitive.reasoning.requirement_resolution import RequirementResolutionResult


def _attempt(
    kind: ResolutionAttemptKind,
    *,
    evidence_ids: tuple[str, ...] = (),
    status: ResolutionAttemptStatus = ResolutionAttemptStatus.NOT_FOUND,
) -> ResolutionAttempt:
    if status is ResolutionAttemptStatus.RESOLVED and not evidence_ids:
        evidence_ids = (f"EV-{kind.value}",)
    return ResolutionAttempt(
        kind=kind,
        status=status,
        source_reference=f"fixture:{kind.value.lower()}",
        evidence_ids=evidence_ids,
    )


def _result(
    state: RequirementState,
    *,
    attempts: tuple[ResolutionAttempt, ...] = (),
    evidence_ids: tuple[str, ...] = (),
    human_validation_required: bool = False,
) -> RequirementResolutionResult:
    assessment = GapAssessment(
        requirement_id="R1",
        parameter="base.width",
        state=state,
        reasons=("fixture",),
        evidence_ids=evidence_ids,
        confidence=ConfidenceBand.UNVERIFIED,
        human_validation_required=human_validation_required,
    )
    return RequirementResolutionResult(
        requirement_id="R1",
        parameter="base.width",
        claims=(),
        attempts=attempts,
        assessment=assessment,
        scope_context={
            "retrieval.tenant_id": "tenant-a",
            "retrieval.domain": "budgeting",
            "retrieval.request_id": "REQ-1",
        },
    )


def test_resolved_requirement_needs_no_additional_action():
    result = _result(RequirementState.KNOWN, evidence_ids=("EV-1",))

    plan = plan_gap_resolution(result)

    assert plan.status is GapResolutionStatus.RESOLVED
    assert plan.action is GapResolutionAction.NONE
    assert plan.handoff_required is False
    assert plan.human_validation_required is False
    assert plan.can_execute is False
    assert plan.evidence_ids == ("EV-1",)
    assert plan.scope_context["retrieval.tenant_id"] == "tenant-a"


def test_gap_candidate_continues_only_unexecuted_canonical_attempts():
    attempts = (
        _attempt(ResolutionAttemptKind.RETRIEVAL),
        _attempt(ResolutionAttemptKind.RULE),
    )
    plan = plan_gap_resolution(
        _result(RequirementState.GAP_CANDIDATE, attempts=attempts)
    )

    assert plan.status is GapResolutionStatus.CONTINUE_RESOLUTION
    assert plan.action is GapResolutionAction.CONTINUE_CANONICAL_RESOLUTION
    assert plan.executed_attempts == (
        ResolutionAttemptKind.RETRIEVAL,
        ResolutionAttemptKind.RULE,
    )
    assert plan.unexecuted_attempts == (
        ResolutionAttemptKind.CALCULATION,
        ResolutionAttemptKind.INFERENCE,
    )
    assert plan.handoff_required is False
    assert plan.can_execute is False


def test_gap_candidate_after_all_attempts_is_rejected_as_inconsistent():
    attempts = tuple(_attempt(kind) for kind in ResolutionAttemptKind)

    with pytest.raises(ValueError, match="GAP_CANDIDATE is inconsistent"):
        plan_gap_resolution(
            _result(RequirementState.GAP_CANDIDATE, attempts=attempts)
        )


def test_noncanonical_attempt_order_is_rejected_before_planning():
    attempts = (
        _attempt(ResolutionAttemptKind.RULE),
        _attempt(ResolutionAttemptKind.RETRIEVAL),
    )

    with pytest.raises(ValueError, match="not in canonical order"):
        plan_gap_resolution(
            _result(RequirementState.GAP_CANDIDATE, attempts=attempts)
        )


def test_duplicate_attempt_kind_is_rejected_instead_of_silently_normalized():
    attempts = (
        _attempt(ResolutionAttemptKind.RETRIEVAL),
        _attempt(ResolutionAttemptKind.RETRIEVAL),
    )

    with pytest.raises(ValueError, match="duplicate canonical attempt kinds"):
        plan_gap_resolution(
            _result(RequirementState.GAP_CANDIDATE, attempts=attempts)
        )


def test_confirmed_gap_requests_new_evidence_after_all_attempts_are_exhausted():
    attempts = tuple(
        _attempt(kind, evidence_ids=(f"EV-{kind.value}",))
        for kind in ResolutionAttemptKind
    )
    result = _result(
        RequirementState.GAP_CONFIRMED,
        attempts=attempts,
        evidence_ids=("EV-GAP",),
        human_validation_required=True,
    )

    plan = plan_gap_resolution(result)

    assert plan.status is GapResolutionStatus.HANDOFF_REQUIRED
    assert plan.action is GapResolutionAction.REQUEST_NEW_EVIDENCE
    assert plan.executed_attempts == tuple(ResolutionAttemptKind)
    assert plan.unexecuted_attempts == ()
    assert plan.handoff_required is True
    assert plan.human_validation_required is True
    assert plan.evidence_ids == ("EV-GAP",)
    assert plan.can_execute is False


def test_confirmed_gap_before_all_attempts_is_rejected_as_inconsistent():
    result = _result(
        RequirementState.GAP_CONFIRMED,
        attempts=(_attempt(ResolutionAttemptKind.RETRIEVAL),),
        human_validation_required=True,
    )

    with pytest.raises(ValueError, match="before every canonical resolution attempt"):
        plan_gap_resolution(result)


def test_confirmed_gap_rejects_any_resolved_attempt():
    attempts = (
        _attempt(ResolutionAttemptKind.RETRIEVAL),
        _attempt(
            ResolutionAttemptKind.RULE,
            status=ResolutionAttemptStatus.RESOLVED,
        ),
        _attempt(ResolutionAttemptKind.CALCULATION),
        _attempt(ResolutionAttemptKind.INFERENCE),
    )
    result = _result(
        RequirementState.GAP_CONFIRMED,
        attempts=attempts,
        human_validation_required=True,
    )

    with pytest.raises(ValueError, match="attempt is RESOLVED"):
        plan_gap_resolution(result)


def test_inference_requires_human_validation_handoff():
    plan = plan_gap_resolution(
        _result(
            RequirementState.HUMAN_VALIDATION_REQUIRED,
            evidence_ids=("EV-INFERENCE",),
            human_validation_required=True,
        )
    )

    assert plan.status is GapResolutionStatus.HANDOFF_REQUIRED
    assert plan.action is GapResolutionAction.VALIDATE_INFERENCE
    assert plan.human_validation_required is True
    assert plan.can_execute is False


def test_assumption_requires_governed_review():
    plan = plan_gap_resolution(
        _result(
            RequirementState.ASSUMPTION_REQUIRED,
            evidence_ids=("EV-ASSUMPTION",),
            human_validation_required=True,
        )
    )

    assert plan.status is GapResolutionStatus.HANDOFF_REQUIRED
    assert plan.action is GapResolutionAction.REVIEW_GOVERNED_ASSUMPTION
    assert plan.human_validation_required is True


def test_conflict_requires_investigation_and_never_silent_resolution():
    plan = plan_gap_resolution(
        _result(
            RequirementState.CONFLICT,
            evidence_ids=("EV-A", "EV-B"),
            human_validation_required=True,
        )
    )

    assert plan.status is GapResolutionStatus.HANDOFF_REQUIRED
    assert plan.action is GapResolutionAction.INVESTIGATE_CONFLICT
    assert plan.evidence_ids == ("EV-A", "EV-B")
    assert plan.can_execute is False


def test_missing_state_requests_evidence_without_becoming_confirmed_gap():
    plan = plan_gap_resolution(_result(RequirementState.MISSING))

    assert plan.assessment_state is RequirementState.MISSING
    assert plan.action is GapResolutionAction.REQUEST_NEW_EVIDENCE
    assert plan.status is GapResolutionStatus.HANDOFF_REQUIRED
    assert plan.can_execute is False


def test_automatic_state_with_pending_human_gate_is_not_marked_resolved():
    plan = plan_gap_resolution(
        _result(
            RequirementState.RETRIEVED,
            evidence_ids=("EV-RETRIEVED",),
            human_validation_required=True,
        )
    )

    assert plan.status is GapResolutionStatus.HANDOFF_REQUIRED
    assert plan.action is GapResolutionAction.REVIEW_HUMAN_GATE
    assert plan.human_validation_required is True
    assert plan.can_execute is False


def test_audit_is_bounded_and_preserves_only_governed_resolution_context():
    plan = plan_gap_resolution(
        _result(
            RequirementState.HUMAN_VALIDATION_REQUIRED,
            evidence_ids=("EV-1", "EV-1", "  ", "EV-2"),
            human_validation_required=True,
        )
    )

    audit = audit_gap_resolution_plan(plan)

    assert audit == {
        "requirement_id": "R1",
        "parameter": "base.width",
        "assessment_state": "HUMAN_VALIDATION_REQUIRED",
        "status": "HANDOFF_REQUIRED",
        "action": "VALIDATE_INFERENCE",
        "evidence_ids": ("EV-1", "EV-2"),
        "executed_attempts": (),
        "unexecuted_attempts": (
            "RETRIEVAL",
            "RULE",
            "CALCULATION",
            "INFERENCE",
        ),
        "handoff_required": True,
        "human_validation_required": True,
        "scope_context": {
            "retrieval.tenant_id": "tenant-a",
            "retrieval.domain": "budgeting",
            "retrieval.request_id": "REQ-1",
        },
        "can_execute": False,
    }
    assert "reasons" not in audit
    assert "metadata" not in audit


def test_so203_confirmed_gap_becomes_evidence_request_not_fabricated_resolution():
    attempts = tuple(_attempt(kind) for kind in ResolutionAttemptKind)
    result = RequirementResolutionResult(
        requirement_id="SO-203.26:R4",
        parameter="panel.count",
        claims=(),
        attempts=attempts,
        assessment=GapAssessment(
            requirement_id="SO-203.26:R4",
            parameter="panel.count",
            state=RequirementState.GAP_CONFIRMED,
            reasons=("all governed paths exhausted",),
            evidence_ids=("SO203-ATTEMPTS",),
            confidence=ConfidenceBand.UNVERIFIED,
            human_validation_required=True,
        ),
    )

    plan = plan_gap_resolution(result)

    assert plan.action is GapResolutionAction.REQUEST_NEW_EVIDENCE
    assert plan.status is GapResolutionStatus.HANDOFF_REQUIRED
    assert plan.assessment_state is RequirementState.GAP_CONFIRMED
    assert plan.can_execute is False
