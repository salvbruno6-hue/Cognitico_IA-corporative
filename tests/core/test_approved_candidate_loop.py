from elo.core.approved_candidate_loop import (
    ApprovedCandidate,
    ApprovedCandidateLoop,
    CandidateApprovalState,
    PostApprovalState,
)
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.systemic_primitives import DecisionRecord


def lifecycle(decision_id="decision-001", state=DecisionState.APPROVED):
    return DecisionLifecycle(
        decision=DecisionRecord(
            decision_id=decision_id,
            decision="implementar skill aprovada",
            rationale="decisão governada",
        ),
        state=state,
    )


def candidate(candidate_id="cand-001", state=CandidateApprovalState.APPROVED):
    return ApprovedCandidate(
        candidate_id=candidate_id,
        skill_id="symbiont.example",
        approval_state=state,
        implementation_ref="src/elo/example.py",
        implementation_decision_id="decision-001",
    )


def test_approved_candidates_activate_after_approved_implementation_decision():
    result = ApprovedCandidateLoop().activate(
        lifecycle=lifecycle(),
        candidates=(candidate(),),
    )

    assert len(result) == 1
    assert result[0].state is PostApprovalState.OBSERVING
    assert result[0].candidate_id == "cand-001"


def test_loop_is_fail_closed_for_unapproved_candidate():
    try:
        ApprovedCandidateLoop().activate(
            lifecycle=lifecycle(),
            candidates=(candidate("cand-002", CandidateApprovalState.BLOCKED),),
        )
    except ValueError as exc:
        assert "not approved" in str(exc)
    else:
        raise AssertionError("blocked candidate must not activate")


def test_loop_does_not_activate_before_implementation_decision():
    try:
        ApprovedCandidateLoop().activate(
            lifecycle=lifecycle(state=DecisionState.PROPOSED),
            candidates=(candidate(),),
        )
    except ValueError as exc:
        assert "must be approved" in str(exc)
    else:
        raise AssertionError("unapproved implementation decision must not activate")


def test_loop_requires_implementation_reference():
    invalid = ApprovedCandidate(
        candidate_id="cand-004",
        skill_id="symbiont.example",
        approval_state=CandidateApprovalState.APPROVED,
        implementation_ref="",
        implementation_decision_id="decision-001",
    )
    try:
        ApprovedCandidateLoop().activate(
            lifecycle=lifecycle(),
            candidates=(invalid,),
        )
    except ValueError as exc:
        assert "implementation reference" in str(exc)
    else:
        raise AssertionError("missing implementation reference must block activation")


def test_loop_ignores_candidates_bound_to_another_decision():
    other = ApprovedCandidate(
        candidate_id="cand-other",
        skill_id="symbiont.other",
        approval_state=CandidateApprovalState.APPROVED,
        implementation_ref="src/elo/other.py",
        implementation_decision_id="decision-other",
    )
    result = ApprovedCandidateLoop().activate(
        lifecycle=lifecycle(),
        candidates=(other,),
    )
    assert result == ()
