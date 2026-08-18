"""Deterministic operational resilience checks for ELO-156.

These tests validate repository-local control semantics without requiring live
providers or production credentials. They do not convert external evidence
requirements into PASS.
"""

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    SUCCESS = "SUCCESS"
    RETRY = "RETRY"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"
    RECOVERED = "RECOVERED"


@dataclass(frozen=True)
class Attempt:
    authorized: bool
    provider_available: bool
    transient_failure: bool
    evidence_complete: bool


def execute_with_resilience(attempts: list[Attempt], max_retries: int = 2) -> Outcome:
    """Model the governed boundary without invoking an external adapter."""
    if not attempts:
        return Outcome.BLOCKED

    for index, attempt in enumerate(attempts):
        if not attempt.authorized or not attempt.evidence_complete:
            return Outcome.BLOCKED
        if not attempt.provider_available:
            if index < min(max_retries, len(attempts) - 1):
                continue
            return Outcome.DEGRADED
        if attempt.transient_failure:
            if index < min(max_retries, len(attempts) - 1):
                continue
            return Outcome.DEGRADED
        return Outcome.RECOVERED if index else Outcome.SUCCESS

    return Outcome.DEGRADED


def test_unauthorized_execution_is_blocked_before_retry():
    attempts = [
        Attempt(False, False, True, True),
        Attempt(False, True, False, True),
    ]
    assert execute_with_resilience(attempts) is Outcome.BLOCKED


def test_incomplete_evidence_is_blocked_before_execution():
    attempts = [Attempt(True, True, False, False)]
    assert execute_with_resilience(attempts) is Outcome.BLOCKED


def test_transient_failure_recovers_within_retry_budget():
    attempts = [
        Attempt(True, True, True, True),
        Attempt(True, True, False, True),
    ]
    assert execute_with_resilience(attempts) is Outcome.RECOVERED


def test_provider_failure_degrades_after_retry_budget():
    attempts = [
        Attempt(True, False, False, True),
        Attempt(True, False, False, True),
        Attempt(True, False, False, True),
    ]
    assert execute_with_resilience(attempts, max_retries=2) is Outcome.DEGRADED


def test_empty_attempts_are_blocked():
    assert execute_with_resilience([]) is Outcome.BLOCKED
