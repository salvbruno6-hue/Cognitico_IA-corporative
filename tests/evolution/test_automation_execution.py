from elo.cognitive.automation_execution_contract import (
    AutomationEvidence,
    ExecutionAuthorization,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
)
from elo.cognitive.automation_execution import (
    AutomationExecution,
    authorize_execution,
    execute_automation,
)


def request():
    return ExecutionRequest(
        execution_id="exe-1",
        tenant_id="tenant-1",
        source_observation_id="obs-1",
        decision_id="decision-1",
        action="bounded experiment",
        scope="EVOLUÇÃO_DE_CAPACIDADES",
        evidence_ids=("ev-1",),
        authorized_by=None,
        authorization_status="PENDING",
        automation_id="automation-test",
    )


def evidence():
    return AutomationEvidence(
        evidence_id="ev-result",
        execution_id="exe-1",
        source_ref="benchmark://exe-1",
        source_kind="benchmark",
        observed_at="2026-09-23T00:00:00Z",
        summary="explicit experiment result",
    )


def test_authorization_is_required():
    auth = ExecutionAuthorization(
        execution_id="exe-1", authorized=False, authorized_by="elo",
        scope="EVOLUÇÃO_DE_CAPACIDADES", reason="blocked",
    )
    blocked = authorize_execution(request(), auth)
    assert blocked.status is ExecutionStatus.BLOCKED
    try:
        execute_automation(blocked, lambda _: None)
    except ValueError:
        pass
    else:
        raise AssertionError("execution without authorization must fail")


def test_authorized_execution_returns_explicit_evidence():
    auth = ExecutionAuthorization(
        execution_id="exe-1", authorized=True, authorized_by="elo",
        scope="EVOLUÇÃO_DE_CAPACIDADES", reason="approved", evidence_ids=("ev-1",),
    )
    authorized = authorize_execution(request(), auth)
    outcome = execute_automation(
        authorized,
        lambda req: AutomationExecution(
            result=ExecutionResult(
                execution_id=req.execution_id,
                automation_id=req.automation_id,
                status=ExecutionStatus.COMPLETED,
                result_ref="benchmark://exe-1",
                evidence_ids=("ev-result",),
                started_at="2026-09-23T00:00:00Z",
                finished_at="2026-09-23T00:01:00Z",
            ),
            evidence=(evidence(),),
        ),
    )
    assert outcome.result.status is ExecutionStatus.COMPLETED
    assert outcome.evidence[0].evidence_id == "ev-result"


def test_completed_execution_without_evidence_is_blocked():
    auth = ExecutionAuthorization(
        execution_id="exe-1", authorized=True, authorized_by="elo",
        scope="EVOLUÇÃO_DE_CAPACIDADES", reason="approved", evidence_ids=("ev-1",),
    )
    authorized = authorize_execution(request(), auth)
    try:
        execute_automation(
            authorized,
            lambda req: AutomationExecution(
                result=ExecutionResult(
                    execution_id=req.execution_id, automation_id=req.automation_id,
                    status=ExecutionStatus.COMPLETED, result_ref="benchmark://exe-1",
                    evidence_ids=(), started_at=None, finished_at=None,
                ),
                evidence=(),
            ),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("completed execution without evidence must fail")
