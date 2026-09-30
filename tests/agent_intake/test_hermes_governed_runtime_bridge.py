from datetime import datetime, timedelta, timezone

import pytest

from elo.agent_intake.hermes_governed_runtime_bridge import (
    GovernedHermesRuntimeBridge,
    HermesGovernedRequest,
)
from elo.application.use_cases.orchestrator import AuthorizationDecision


class FakeHermes:
    def __init__(self, response=None):
        self.payloads = []
        self.response = response

    def execute(self, payload):
        self.payloads.append(payload)
        return self.response or {
            "request_id": payload["request_id"],
            "status": "completed",
            "evidence": [],
            "outcome": {},
        }


def _authorization(*, resource_id="EXT-TOOL-SEARCH-HERMES", valid=True):
    expiry = datetime.now(timezone.utc) + timedelta(minutes=10)
    if not valid:
        expiry = datetime.now(timezone.utc) - timedelta(minutes=1)
    return AuthorizationDecision(
        authorized=True,
        authority="elo-authz",
        identity_id="operator-1",
        role="CANONICAL_ADMIN",
        evidence_ref="auth-evidence-1",
        session_id="session-1",
        binding_id="binding-1",
        grant_id="grant-1",
        operation="execute",
        resource_id=resource_id,
        expires_at=expiry.isoformat(),
    )


def _request():
    return HermesGovernedRequest(
        request_id="exec-001",
        tenant_scope="tenant-test",
        mission_class="skill_execution",
        intent="execute governed skill",
        skill_id="EXT-TOOL-SEARCH-HERMES",
        decision_id="decision-001",
        authorized_capabilities=("skill:execute",),
        evidence_requirements=("candidate_evidence",),
        context={"domain": "FORGE"},
    )


def test_bridge_transports_canonical_authorization_without_creating_authority():
    client = FakeHermes()
    result = GovernedHermesRuntimeBridge(client).execute(
        _request(), _authorization()
    )

    assert result["request_id"] == "exec-001"
    payload = client.payloads[0]
    assert payload["context"]["skill_id"] == "EXT-TOOL-SEARCH-HERMES"
    assert payload["context"]["decision_id"] == "decision-001"
    assert payload["context"]["authorization_id"] == "grant-1"
    assert payload["context"]["authorization_evidence_ref"] == "auth-evidence-1"


def test_bridge_fails_closed_on_invalid_transport_authorization():
    with pytest.raises(PermissionError, match="elo-authz"):
        GovernedHermesRuntimeBridge(FakeHermes()).execute(
            _request(), _authorization(valid=False)
        )


def test_bridge_fails_closed_on_resource_mismatch():
    with pytest.raises(PermissionError, match="resource"):
        GovernedHermesRuntimeBridge(FakeHermes()).execute(
            _request(), _authorization(resource_id="OTHER-SKILL")
        )


def test_bridge_rejects_response_for_different_request():
    client = FakeHermes(response={"request_id": "other", "status": "completed"})
    with pytest.raises(ValueError, match="request_id"):
        GovernedHermesRuntimeBridge(client).execute(_request(), _authorization())
