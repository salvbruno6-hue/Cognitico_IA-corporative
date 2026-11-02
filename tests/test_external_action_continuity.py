import pytest

from elo.cognitive.external_action_continuity import (
    ExternalActionContinuityState,
    classify_external_action_continuity,
)


def decide(**overrides):
    values = dict(
        objective_validated=True,
        governance_approved=True,
        executor_authorized=True,
        external_policy_blocked=False,
        alternative_route_authorized=False,
        terminal_failure=False,
    )
    values.update(overrides)
    return classify_external_action_continuity(**values)


def test_external_block_preserves_objective_without_retrying_blocked_executor():
    result = decide(external_policy_blocked=True)
    assert result.state is ExternalActionContinuityState.EXTERNAL_ACTION_BLOCKED
    assert result.preserve_objective is True
    assert result.retry_same_executor is False


def test_independently_authorized_alternative_route_can_continue():
    result = decide(external_policy_blocked=True, alternative_route_authorized=True)
    assert result.state is ExternalActionContinuityState.CONTINUE_AUTHORIZED_ROUTE
    assert result.preserve_objective is True
    assert result.retry_same_executor is False


def test_alternative_route_never_substitutes_missing_governance():
    result = decide(governance_approved=False, external_policy_blocked=True, alternative_route_authorized=True)
    assert result.state is ExternalActionContinuityState.AUTHORIZATION_REQUIRED
    assert result.preserve_objective is False


def test_selected_executor_without_authorization_requires_authority():
    result = decide(executor_authorized=False)
    assert result.state is ExternalActionContinuityState.AUTHORIZATION_REQUIRED
    assert result.retry_same_executor is False


def test_terminal_failure_stops_continuation():
    result = decide(terminal_failure=True)
    assert result.state is ExternalActionContinuityState.TERMINAL_FAILURE
    assert result.preserve_objective is False


@pytest.mark.parametrize("field", [
    "objective_validated",
    "governance_approved",
    "executor_authorized",
    "external_policy_blocked",
    "alternative_route_authorized",
    "terminal_failure",
])
@pytest.mark.parametrize("bad", [None, 0, 1, "true", [], {}])
def test_malformed_controls_fail_closed(field, bad):
    result = decide(**{field: bad})
    assert result.state is ExternalActionContinuityState.INVALID
    assert result.preserve_objective is False
    assert result.retry_same_executor is False
