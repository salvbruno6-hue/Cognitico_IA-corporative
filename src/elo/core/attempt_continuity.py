"""Owner-bound attempt continuity for the canonical ELO ExecutionBoundary.

This module classifies whether an already-admitted execution attempt may be retried.
It does not authorize execution, dispatch work, create a new runtime owner, or mutate
Hermes. Authorization and execution remain owned by the canonical ExecutionBoundary.
"""
from dataclasses import dataclass
from enum import StrEnum


class ContinuityDecision(StrEnum):
    RETRY_SAME_ATTEMPT = "RETRY_SAME_ATTEMPT"
    STOP_BLOCKED = "STOP_BLOCKED"
    STOP_TERMINAL = "STOP_TERMINAL"
    STOP_EXHAUSTED = "STOP_EXHAUSTED"
    INVALID = "INVALID"


class FailureClass(StrEnum):
    TRANSIENT_TRANSPORT = "transient_transport"
    OWNER_DRAINING = "owner_draining"
    OWNER_RETIRED = "owner_retired"
    AUTHORIZATION_DENIED = "authorization_denied"
    SCOPE_DENIED = "scope_denied"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    TERMINAL = "terminal"


_TRANSIENT = {
    FailureClass.TRANSIENT_TRANSPORT,
    FailureClass.OWNER_DRAINING,
    FailureClass.OWNER_RETIRED,
}
_BLOCKING = {
    FailureClass.AUTHORIZATION_DENIED,
    FailureClass.SCOPE_DENIED,
    FailureClass.EVIDENCE_INCOMPLETE,
}


@dataclass(frozen=True)
class AttemptContinuityRequest:
    request_id: str
    attempt_id: str
    owner_id: str
    authorization_id: str
    failure_class: FailureClass
    retry_count: int
    max_retries: int


@dataclass(frozen=True)
class AttemptContinuityResult:
    decision: ContinuityDecision
    preserve_attempt: bool
    preserve_authorization: bool
    reason: str


def evaluate_attempt_continuity(request: AttemptContinuityRequest) -> AttemptContinuityResult:
    """Classify continuity without granting or refreshing authority."""
    if not all((request.request_id, request.attempt_id, request.owner_id, request.authorization_id)):
        return AttemptContinuityResult(ContinuityDecision.INVALID, False, False, "missing_identity_or_authority")
    # bool is intentionally rejected even though it subclasses int in Python.
    if (
        type(request.retry_count) is not int
        or type(request.max_retries) is not int
        or request.retry_count < 0
        or request.max_retries < 0
    ):
        return AttemptContinuityResult(ContinuityDecision.INVALID, False, False, "invalid_retry_budget")
    if request.failure_class in _BLOCKING:
        return AttemptContinuityResult(ContinuityDecision.STOP_BLOCKED, False, False, "governance_refusal_is_not_retryable")
    if request.failure_class is FailureClass.TERMINAL:
        return AttemptContinuityResult(ContinuityDecision.STOP_TERMINAL, False, False, "terminal_failure")
    if request.failure_class in _TRANSIENT:
        if request.retry_count >= request.max_retries:
            return AttemptContinuityResult(ContinuityDecision.STOP_EXHAUSTED, False, False, "retry_budget_exhausted")
        return AttemptContinuityResult(
            ContinuityDecision.RETRY_SAME_ATTEMPT,
            True,
            True,
            "transient_failure_preserves_existing_admission",
        )
    return AttemptContinuityResult(ContinuityDecision.INVALID, False, False, "unknown_failure_class")
