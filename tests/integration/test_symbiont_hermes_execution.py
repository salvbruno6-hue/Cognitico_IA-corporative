from elo.cognitive.agents.hermes_contract import HermesExecutionRequest
from elo.cognitive.symbiont_hermes_bridge import SymbiontHermesBridge


def test_integration_symbiont_to_hermes_closes_with_evidence_and_outcome():
    request = HermesExecutionRequest(
        request_id="integration-symbiont-hermes-001",
        intent="executar missão governada de integração",
        context={"domain": "integration", "source": "elo-cognitive"},
        tenant_scope="integration-tenant",
        mission_class="skill_execution",
        authorized_capabilities=("skill:execute",),
        evidence_requirements=("execution", "outcome"),
    )

    def hermes_transport(endpoint, payload):
        assert endpoint == "http://hermes.integration.test"
        assert payload["request_id"] == request.request_id
        assert "skill:execute" in payload["authorized_capabilities"]
        return {
            "request_id": request.request_id,
            "status": "completed",
            "execution": {"runtime": "hermes", "boundary": "symbiont"},
            "evidence": ({"type": "skill_execution", "source": "hermes"},),
            "outcome": {"assessment": "success"},
            "skills_used": ("integration-proof-skill",),
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    receipt = SymbiontHermesBridge().execute(
        request,
        capability="skill:execute",
        endpoint="http://hermes.integration.test",
        transport=hermes_transport,
    )

    assert receipt.result.request_id == request.request_id
    assert receipt.result.status == "completed"
    assert receipt.result.evidence
    assert receipt.result.outcome["assessment"] == "success"
    assert receipt.result.learning_candidate["promotion_state"] == "candidate_only"
