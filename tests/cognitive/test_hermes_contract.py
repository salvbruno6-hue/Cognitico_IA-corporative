import pytest

from elo.cognitive.agents.hermes_contract import (
    HermesExecutionRequest,
    HermesExecutionResult,
)


def test_request_contains_governed_execution_context():
    request = HermesExecutionRequest(
        request_id="req-1",
        intent="executar uma missão autorizada",
        context={"domain": "commercial", "scope": "tenant"},
        tenant_scope="tenant-a",
        mission_class="analysis",
        authorized_capabilities=("read_context", "execute_workflow"),
        method="governed_method",
        evidence_requirements=("provenance", "outcome"),
    )

    payload = request.to_dict()
    assert payload["contract_version"] == "1.0"
    assert payload["authorized_capabilities"] == ("read_context", "execute_workflow")
    assert "project_ref" not in payload
    assert "project_id" not in payload


def test_request_rejects_infrastructure_identifiers():
    with pytest.raises(ValueError, match="infrastructure field"):
        HermesExecutionRequest(
            request_id="req-2",
            intent="consulta",
            context={"project_ref": "must-not-cross-boundary"},
            tenant_scope="tenant-a",
            mission_class="query",
            authorized_capabilities=("read_context",),
        )


def test_result_is_evidence_not_canonical_decision():
    result = HermesExecutionResult(
        request_id="req-1",
        status="completed",
        evidence=({"type": "execution", "source": "hermes"},),
        skills_used=("example-skill",),
        learning_candidate={"promotion_state": "candidate_only"},
    )

    payload = result.to_dict()
    assert payload["status"] == "completed"
    assert payload["learning_candidate"]["promotion_state"] == "candidate_only"
    assert "decision" not in payload
    assert "canonical_knowledge" not in payload


def test_result_rejects_infrastructure_identifiers():
    with pytest.raises(ValueError, match="infrastructure field"):
        HermesExecutionResult(
            request_id="req-3",
            status="completed",
            evidence=({"project_id": "must-not-cross-boundary"},),
        )
