"""Symbiont classification for externally blocked governed actions.

This module does not grant authority, execute an action, create credentials, or
bypass an external policy. It preserves objective continuity by distinguishing
an unavailable executor path from a failed ELO decision.
"""

from dataclasses import dataclass
from enum import StrEnum


class ExternalActionContinuityState(StrEnum):
    CONTINUE_AUTHORIZED_ROUTE = "CONTINUE_AUTHORIZED_ROUTE"
    EXTERNAL_ACTION_BLOCKED = "EXTERNAL_ACTION_BLOCKED"
    AUTHORIZATION_REQUIRED = "AUTHORIZATION_REQUIRED"
    TERMINAL_FAILURE = "TERMINAL_FAILURE"
    INVALID = "INVALID"


@dataclass(frozen=True)
class ExternalActionContinuityDecision:
    state: ExternalActionContinuityState
    reason: str
    preserve_objective: bool
    retry_same_executor: bool


def classify_external_action_continuity(
    *,
    objective_validated: bool,
    governance_approved: bool,
    executor_authorized: bool,
    external_policy_blocked: bool,
    alternative_route_authorized: bool,
    terminal_failure: bool = False,
) -> ExternalActionContinuityDecision:
    """Classify continuity without manufacturing or transferring authority.

    An external policy refusal is never converted into retry permission. An
    alternative route is eligible only when it independently carries explicit
    authorization. The objective may remain pending while the current executor
    is blocked.
    """
    values = (
        objective_validated,
        governance_approved,
        executor_authorized,
        external_policy_blocked,
        alternative_route_authorized,
        terminal_failure,
    )
    if any(type(value) is not bool for value in values):
        return ExternalActionContinuityDecision(
            ExternalActionContinuityState.INVALID,
            "continuity controls must be native booleans",
            False,
            False,
        )

    if not objective_validated or not governance_approved:
        return ExternalActionContinuityDecision(
            ExternalActionContinuityState.AUTHORIZATION_REQUIRED,
            "objective validation and governance approval are required",
            False,
            False,
        )

    if terminal_failure:
        return ExternalActionContinuityDecision(
            ExternalActionContinuityState.TERMINAL_FAILURE,
            "terminal failure prevents automatic continuation",
            False,
            False,
        )

    if external_policy_blocked:
        if alternative_route_authorized:
            return ExternalActionContinuityDecision(
                ExternalActionContinuityState.CONTINUE_AUTHORIZED_ROUTE,
                "current executor is externally blocked; an independently authorized route may continue the same objective",
                True,
                False,
            )
        return ExternalActionContinuityDecision(
            ExternalActionContinuityState.EXTERNAL_ACTION_BLOCKED,
            "current executor is externally blocked and no independently authorized route is available",
            True,
            False,
        )

    if not executor_authorized:
        return ExternalActionContinuityDecision(
            ExternalActionContinuityState.AUTHORIZATION_REQUIRED,
            "the selected executor lacks explicit authorization",
            True,
            False,
        )

    return ExternalActionContinuityDecision(
        ExternalActionContinuityState.CONTINUE_AUTHORIZED_ROUTE,
        "the selected executor is explicitly authorized",
        True,
        False,
    )
