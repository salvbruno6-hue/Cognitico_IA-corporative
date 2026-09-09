import pytest

from elo.cognitive.agents.hermes_contract import HermesExecutionRequest
from elo.cognitive.agents.hermes_runtime import execute_via_hermes


def _request(capability="skill:execute"):
    return HermesExecutionRequest(
        request_id="elo-hermes-001",
        intent="executar habilidade governada",
        context={"domain": "test", "scope": "integration"},
        tenant_scope="tenant-test",
        mission_class="skill_execution",
        authorized_capabilities=(capability,),
        evidence_requirements=("execution", "outcome"),
    )


def test_elo_sends_authorized_mission_and_receives_evidence():
    seen = {}

    def hermes_transport(endpoint, payload):
        seen["endpoint"] = endpoint
        seen["payload"] = payload
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"runtime": "hermes", "mode": "skill"},
            "evidence": ({"type": "skill_execution", "source": "hermes"},),
            "skills_used": ("proof-skill",),
            "outcome": {"result": "HERMES_EXECUTED"},
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    result = execute_via_hermes(_request(), endpoint="http://hermes.test", transport=hermes_transport)

    assert seen["endpoint"] == "http://hermes.test"
    assert seen["payload"]["authorized_capabilities"] == ("skill:execute",)
    assert result.status == "completed"
    assert result.skills_used == ("proof-skill",)
    assert result.outcome["result"] == "HERMES_EXECUTED"


def test_elo_rejects_mismatched_hermes_request_id():
    def transport(endpoint, payload):
        return {"request_id": "other", "status": "completed"}

    with pytest.raises(ValueError, match="request_id"):
        execute_via_hermes(_request(), endpoint="http://hermes.test", transport=transport)


def test_elo_preserves_non_canonical_learning_boundary():
    def transport(endpoint, payload):
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    result = execute_via_hermes(_request(), endpoint="http://hermes.test", transport=transport)
    assert result.learning_candidate["promotion_state"] == "candidate_only"
