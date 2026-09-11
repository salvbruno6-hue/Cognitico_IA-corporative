import pytest

from elo.cognitive.agents.hermes_contract import HermesExecutionRequest
from elo.cognitive.symbiont_hermes_bridge import SymbiontHermesBridge


def _request(capabilities=("skill:execute",)):
    return HermesExecutionRequest(
        request_id="symbiont-hermes-001",
        intent="executar capacidade autorizada",
        context={"domain": "test"},
        tenant_scope="tenant-test",
        mission_class="skill_execution",
        authorized_capabilities=capabilities,
        evidence_requirements=("execution", "outcome"),
    )


def test_symbiont_forwards_only_an_authorized_capability():
    seen = {}

    def transport(endpoint, payload):
        seen["endpoint"] = endpoint
        seen["payload"] = payload
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"runtime": "hermes"},
            "evidence": ({"type": "skill_execution"},),
            "outcome": {"result": "ok"},
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    receipt = SymbiontHermesBridge().execute(
        _request(),
        capability="skill:execute",
        endpoint="http://hermes.test",
        transport=transport,
    )

    assert receipt.request_id == "symbiont-hermes-001"
    assert receipt.capability == "skill:execute"
    assert seen["endpoint"] == "http://hermes.test"
    assert seen["payload"]["authorized_capabilities"] == ("skill:execute",)
    assert receipt.result.outcome["result"] == "ok"


def test_symbiont_rejects_capability_not_authorized_by_elo():
    with pytest.raises(ValueError, match="not authorized"):
        SymbiontHermesBridge().execute(
            _request(("skill:read",)),
            capability="skill:execute",
            endpoint="http://hermes.test",
            transport=lambda *_: {},
        )


def test_symbiont_rejects_result_without_required_outcome():
    def transport(endpoint, payload):
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"runtime": "hermes"},
        }

    with pytest.raises(ValueError, match="outcome evidence"):
        SymbiontHermesBridge().execute(
            _request(),
            capability="skill:execute",
            endpoint="http://hermes.test",
            transport=transport,
        )


def test_symbiont_preserves_candidate_only_learning_boundary():
    def transport(endpoint, payload):
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"runtime": "hermes"},
            "evidence": ({"type": "execution"},),
            "outcome": {"result": "ok"},
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    receipt = SymbiontHermesBridge().execute(
        _request(),
        capability="skill:execute",
        endpoint="http://hermes.test",
        transport=transport,
    )

    assert receipt.result.learning_candidate["promotion_state"] == "candidate_only"
