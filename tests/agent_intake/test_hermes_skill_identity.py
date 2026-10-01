import pytest

from elo.cognitive.agents.hermes_contract import HermesExecutionRequest


def _request(*, context=None, capabilities=("skill:execute",)):
    return HermesExecutionRequest(
        request_id="skill-identity-test",
        intent="controlled test",
        context=context or {},
        tenant_scope="tenant-test",
        mission_class="controlled_test",
        authorized_capabilities=capabilities,
    )


@pytest.mark.parametrize("capability", ["skill:create", "skill:execute"])
def test_skill_capability_requires_skill_and_decision_identity(capability):
    with pytest.raises(ValueError, match="skill_id is required"):
        _request(capabilities=(capability,))


def test_skill_capability_requires_decision_identity():
    with pytest.raises(ValueError, match="decision_id is required"):
        _request(context={"skill_id": "skill:test"})


def test_skill_capability_accepts_both_identity_fields():
    request = _request(
        context={"skill_id": "skill:test", "decision_id": "decision:test"}
    )
    assert request.context["skill_id"] == "skill:test"
    assert request.context["decision_id"] == "decision:test"


def test_non_skill_capability_does_not_require_skill_identity():
    request = _request(capabilities=("hermes:runtime_probe",))
    assert "skill_id" not in request.context
    assert "decision_id" not in request.context


@pytest.mark.parametrize(
    "context",
    [
        {"skill_id": ""},
        {"skill_id": "   ", "decision_id": "decision:test"},
        {"skill_id": "skill:test", "decision_id": ""},
        {"skill_id": "skill:test", "decision_id": "   "},
    ],
)
def test_skill_identity_rejects_blank_values(context):
    with pytest.raises(ValueError):
        _request(context=context)
