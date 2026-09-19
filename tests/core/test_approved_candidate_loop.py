from elo.core.approved_candidate_loop import (
    ApprovedCandidate,
    ApprovedCandidateLoop,
    CandidateApprovalState,
    ImplementationDecision,
    PostApprovalState,
)


def candidate(candidate_id="cand-001", state=CandidateApprovalState.APPROVED):
    return ApprovedCandidate(
        candidate_id=candidate_id,
        skill_id="symbiont.example",
        approval_state=state,
        implementation_ref="src/elo/example.py",
    )


def test_approved_candidates_activate_after_approved_implementation_decision():
    result = ApprovedCandidateLoop().activate(
        decision=ImplementationDecision(
            decision_id="decision-001",
            state="approved",
            approved_candidate_ids=("cand-001",),
        ),
        candidates=(candidate(),),
    )

    assert len(result) == 1
    assert result[0].state is PostApprovalState.OBSERVING
    assert result[0].candidate_id == "cand-001"


def test_loop_is_fail_closed_for_unapproved_candidate():
    try:
        ApprovedCandidateLoop().activate(
            decision=ImplementationDecision(
                decision_id="decision-002",
                state="approved",
                approved_candidate_ids=("cand-002",),
            ),
            candidates=(candidate("cand-002", CandidateApprovalState.BLOCKED),),
        )
    except ValueError as exc:
        assert "not approved" in str(exc)
    else:
        raise AssertionError("blocked candidate must not activate")


def test_loop_does_not_activate_before_implementation_decision():
    try:
        ApprovedCandidateLoop().activate(
            decision=ImplementationDecision(
                decision_id="decision-003",
                state="proposed",
                approved_candidate_ids=("cand-001",),
            ),
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
    )
    try:
        ApprovedCandidateLoop().activate(
            decision=ImplementationDecision(
                decision_id="decision-004",
                state="approved",
                approved_candidate_ids=("cand-004",),
            ),
            candidates=(invalid,),
        )
    except ValueError as exc:
        assert "implementation reference" in str(exc)
    else:
        raise AssertionError("missing implementation reference must block activation")
