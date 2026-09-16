"""Bounded insistence/recovery runtime for governed ELO experiences.

This module orchestrates attempts after a capability decision has already been
made by the cognitive/governance layer. It does not resolve capabilities,
authorize execution, mutate canonical knowledge, or promote learning.

Core rule: insist on the objective, not on the method.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Callable


class AttemptOutcome(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_PROGRESS = "PARTIAL_PROGRESS"
    NO_PROGRESS = "NO_PROGRESS"
    BLOCKED = "BLOCKED"
    CONFLICT = "CONFLICT"
    AUTHORITY_REQUIRED = "AUTHORITY_REQUIRED"


class InsistenceAction(str, Enum):
    RETRY = "RETRY"
    REFRESH = "REFRESH"
    REPLAN = "REPLAN"
    HANDOFF = "HANDOFF"
    STOP = "STOP"


@dataclass(frozen=True)
class AttemptResult:
    outcome: AttemptOutcome
    observed: str
    progress_signature: str = ""
    evidence_signature: str = ""
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class InsistenceState:
    objective: str
    attempt_no: int = 0
    previous_action: InsistenceAction | None = None
    progress_signature: str = ""
    evidence_signature: str = ""
    no_progress_count: int = 0
    repeated_signature_count: int = 0


@dataclass(frozen=True)
class InsistenceDecision:
    action: InsistenceAction
    reason: str
    state: InsistenceState


@dataclass(frozen=True)
class InsistenceRun:
    objective: str
    terminal_outcome: AttemptOutcome | None
    terminal_action: InsistenceAction
    attempts: tuple[AttemptResult, ...]
    decisions: tuple[InsistenceDecision, ...]


def decide_next_attempt(
    state: InsistenceState,
    result: AttemptResult,
    *,
    max_attempts: int = 5,
    no_progress_limit: int = 2,
) -> InsistenceDecision:
    """Choose a bounded recovery action from an observed attempt.

    The function is deterministic and recommendation-only. It cannot execute,
    select a capability, or change canonical authority.
    """
    if max_attempts < 1 or no_progress_limit < 1:
        raise ValueError("max_attempts and no_progress_limit must be positive")

    next_attempt = state.attempt_no + 1
    same_signature = (
        bool(result.progress_signature)
        and result.progress_signature == state.progress_signature
        and result.evidence_signature == state.evidence_signature
    )
    repeated = state.repeated_signature_count + 1 if same_signature else 0
    no_progress = state.no_progress_count + 1 if result.outcome == AttemptOutcome.NO_PROGRESS else 0

    next_state = InsistenceState(
        objective=state.objective,
        attempt_no=next_attempt,
        previous_action=None,
        progress_signature=result.progress_signature,
        evidence_signature=result.evidence_signature,
        no_progress_count=no_progress,
        repeated_signature_count=repeated,
    )

    if result.outcome == AttemptOutcome.SUCCESS:
        return InsistenceDecision(InsistenceAction.STOP, "SUCCESS closes the experience", next_state)
    if result.outcome in (AttemptOutcome.BLOCKED, AttemptOutcome.CONFLICT, AttemptOutcome.AUTHORITY_REQUIRED):
        return InsistenceDecision(InsistenceAction.HANDOFF, f"{result.outcome.value} requires governed handoff", next_state)
    if next_attempt >= max_attempts:
        return InsistenceDecision(InsistenceAction.STOP, "maximum bounded attempts reached", next_state)
    if repeated >= 2:
        return InsistenceDecision(InsistenceAction.STOP, "repeated identical progress/evidence signature detected", next_state)
    if result.outcome == AttemptOutcome.NO_PROGRESS:
        if no_progress >= no_progress_limit:
            return InsistenceDecision(InsistenceAction.REPLAN, "NO_PROGRESS limit reached; change the method", next_state)
        return InsistenceDecision(InsistenceAction.REFRESH, "NO_PROGRESS requires refreshed evidence/context", next_state)
    if result.outcome == AttemptOutcome.PARTIAL_PROGRESS:
        return InsistenceDecision(InsistenceAction.RETRY, "partial progress supports a bounded retry", next_state)
    return InsistenceDecision(InsistenceAction.REPLAN, "unclassified progress requires a new governed plan", next_state)


AttemptExecutor = Callable[[InsistenceAction, InsistenceState], AttemptResult]


def run_insistence_experience(
    *,
    objective: str,
    execute: AttemptExecutor,
    max_attempts: int = 5,
    no_progress_limit: int = 2,
) -> InsistenceRun:
    """Run a bounded experience until success, handoff, or controlled stop.

    ``execute`` is the already-governed experience boundary. This runtime only
    supplies the recovery action and state; it does not decide which capability
    exists or grant authority to it.
    """
    if not objective.strip():
        raise ValueError("objective is required")

    state = InsistenceState(objective=objective)
    attempts: list[AttemptResult] = []
    decisions: list[InsistenceDecision] = []
    action = InsistenceAction.RETRY

    while True:
        result = execute(action, state)
        attempts.append(result)
        decision = decide_next_attempt(
            state,
            result,
            max_attempts=max_attempts,
            no_progress_limit=no_progress_limit,
        )
        decisions.append(decision)
        state = replace(decision.state, previous_action=decision.action)

        if decision.action in (InsistenceAction.STOP, InsistenceAction.HANDOFF):
            return InsistenceRun(
                objective=objective,
                terminal_outcome=result.outcome,
                terminal_action=decision.action,
                attempts=tuple(attempts),
                decisions=tuple(decisions),
            )
        action = decision.action
