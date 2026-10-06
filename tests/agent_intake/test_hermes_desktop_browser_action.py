from elo.agent_intake.hermes_desktop_browser_action import (
    BrowserActionKind,
    BrowserDisposition,
    DesktopBrowserAction,
    assess_browser_action,
)


def make_action(**overrides):
    values = dict(
        request_id="req-1",
        tenant_id="tenant-1",
        principal_id="principal-1",
        mission_id="mission-1",
        url="https://example.com/catalog",
        domain_scope="example.com",
        action_kind=BrowserActionKind.NAVIGATE_READ,
        provenance_ref="evidence:browser-1",
    )
    values.update(overrides)
    return DesktopBrowserAction(**values)


def test_read_navigation_is_candidate_only():
    result = assess_browser_action(make_action())
    assert result.disposition is BrowserDisposition.CANDIDATE_ONLY
    assert result.execution_permitted is False


def test_mutating_browser_action_is_blocked():
    result = assess_browser_action(make_action(action_kind=BrowserActionKind.SUBMIT))
    assert result.disposition is BrowserDisposition.BLOCKED
    assert result.execution_permitted is False


def test_missing_provenance_is_blocked():
    result = assess_browser_action(make_action(provenance_ref=""))
    assert result.disposition is BrowserDisposition.BLOCKED


def test_invalid_target_is_blocked():
    result = assess_browser_action(make_action(url="javascript:alert(1)"))
    assert result.disposition is BrowserDisposition.BLOCKED


def test_authorization_does_not_create_execution_authority():
    result = assess_browser_action(make_action(authorization_id="auth-1"))
    assert result.disposition is BrowserDisposition.CANDIDATE_ONLY
    assert result.execution_permitted is False
