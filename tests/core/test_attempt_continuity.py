from elo.core.attempt_continuity import (
    AttemptContinuityRequest,
    ContinuityDecision,
    FailureClass,
    evaluate_attempt_continuity,
)


def req(failure: FailureClass, *, retry_count: int = 0, max_retries: int = 2, authorization_id: str = "auth-1"):
    return AttemptContinuityRequest(
        request_id="req-1",
        attempt_id="attempt-1",
        owner_id="execution-boundary",
        authorization_id=authorization_id,
        failure_class=failure,
        retry_count=retry_count,
        max_retries=max_retries,
    )


def test_transient_transport_preserves_same_attempt_and_existing_authorization():
    result = evaluate_attempt_continuity(req(FailureClass.TRANSIENT_TRANSPORT))
    assert result.decision is ContinuityDecision.RETRY_SAME_ATTEMPT
    assert result.preserve_attempt is True
    assert result.preserve_authorization is True


def test_owner_draining_and_retired_are_retryable_within_budget():
    for failure in (FailureClass.OWNER_DRAINING, FailureClass.OWNER_RETIRED):
        assert evaluate_attempt_continuity(req(failure)).decision is ContinuityDecision.RETRY_SAME_ATTEMPT


def test_authorization_scope_and_evidence_refusals_never_become_retry():
    for failure in (
        FailureClass.AUTHORIZATION_DENIED,
        FailureClass.SCOPE_DENIED,
        FailureClass.EVIDENCE_INCOMPLETE,
    ):
        result = evaluate_attempt_continuity(req(failure))
        assert result.decision is ContinuityDecision.STOP_BLOCKED
        assert result.preserve_authorization is False


def test_retry_budget_is_bounded():
    result = evaluate_attempt_continuity(req(FailureClass.TRANSIENT_TRANSPORT, retry_count=2, max_retries=2))
    assert result.decision is ContinuityDecision.STOP_EXHAUSTED
    assert result.preserve_attempt is False


def test_terminal_failure_is_not_retryable():
    assert evaluate_attempt_continuity(req(FailureClass.TERMINAL)).decision is ContinuityDecision.STOP_TERMINAL


def test_missing_authorization_fails_closed():
    result = evaluate_attempt_continuity(req(FailureClass.TRANSIENT_TRANSPORT, authorization_id=""))
    assert result.decision is ContinuityDecision.INVALID
    assert result.preserve_authorization is False


def test_invalid_retry_budget_fails_closed():
    assert evaluate_attempt_continuity(req(FailureClass.TRANSIENT_TRANSPORT, retry_count=-1)).decision is ContinuityDecision.INVALID
