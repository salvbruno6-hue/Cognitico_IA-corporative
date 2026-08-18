from dataclasses import dataclass

from elo.core.execution_boundary import (
    ExecutionStatus,
    ExecutionRequest,
    execute_governed,
    validate_execution_request,
)


@dataclass
class Adapter:
    calls: int = 0

    def execute(self, request):
        self.calls += 1
        return {"adapter": "test", "action": request.action_id}


def test_execution_is_blocked_without_authorization_or_evidence():
    request = ExecutionRequest(
        request_id="REQ-1",
        tenant_id="TENANT-1",
        principal_id="USER-1",
        action_id="ACTION-1",
        authorization_id=None,
        correlation_id="CORR-1",
    )
    adapter = Adapter()

    outcome = execute_governed(request, adapter)

    assert outcome.status == ExecutionStatus.BLOCKED
    assert outcome.executed is False
    assert adapter.calls == 0
    assert "authorization_id" in outcome.reason
    assert "evidence_ids" in outcome.reason


def test_valid_execution_requires_explicit_controls_and_preserves_provenance():
    request = ExecutionRequest(
        request_id="REQ-2",
        tenant_id="TENANT-1",
        principal_id="USER-1",
        action_id="ACTION-1",
        authorization_id="AUTH-1",
        evidence_ids=("EV-1",),
        correlation_id="CORR-2",
    )
    adapter = Adapter()

    assert validate_execution_request(request) is None
    outcome = execute_governed(request, adapter)

    assert outcome.status == ExecutionStatus.EXECUTED
    assert outcome.executed is True
    assert adapter.calls == 1
    assert outcome.provenance["authorization_id"] == "AUTH-1"
    assert outcome.provenance["correlation_id"] == "CORR-2"


def test_execution_never_falls_back_to_untracked_best_effort():
    request = ExecutionRequest(
        request_id="REQ-3",
        tenant_id="TENANT-1",
        principal_id="USER-1",
        action_id="ACTION-1",
        authorization_id="AUTH-1",
        evidence_ids=(),
        correlation_id="CORR-3",
    )
    adapter = Adapter()

    outcome = execute_governed(request, adapter)

    assert outcome.executed is False
    assert outcome.provenance["execution"] == "not_attempted"
    assert adapter.calls == 0
