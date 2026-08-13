from elo.core.emergency_override import EmergencyOverrideRequest, OverrideStatus


def request(**overrides):
    values = {
        "commit_sha": "abc123",
        "failure_class": "INFRASTRUCTURE_FAILURE",
        "reason": "CI unavailable",
        "architecture_compatible": True,
        "human_approved": True,
        "risk_accepted": True,
        "follow_up_required": True,
    }
    values.update(overrides)
    return EmergencyOverrideRequest(**values)


def test_approves_only_explicit_infrastructure_override():
    assert request().evaluate() is OverrideStatus.APPROVED
    assert request().validation_status == "UNKNOWN"
    assert request().merge_metadata["override"] == "GOVERNED"


def test_test_failure_is_denied():
    assert request(failure_class="TEST_FAILURE").evaluate() is OverrideStatus.DENIED


def test_architectural_conflict_is_denied():
    assert request(failure_class="ARCHITECTURAL_CONFLICT").evaluate() is OverrideStatus.DENIED


def test_security_failure_is_denied():
    assert request(failure_class="SECURITY_FAILURE").evaluate() is OverrideStatus.DENIED


def test_missing_human_approval_is_pending():
    assert request(human_approved=False).evaluate() is OverrideStatus.PENDING


def test_override_requires_follow_up():
    assert request(follow_up_required=False).evaluate() is OverrideStatus.DENIED
