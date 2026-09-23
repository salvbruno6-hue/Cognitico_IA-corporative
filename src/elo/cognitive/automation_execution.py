"""Process adapter that closes the automation execution/evidence boundary.

The executor validates authorization and delegates the actual operation to an
injected callable. It never decides learning, evolution, promotion or canonical
mutation.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace

from .automation_execution_contract import (
    AutomationEvidence,
    ExecutionAuthorization,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
)


@dataclass(frozen=True, slots=True)
class AutomationExecution:
    result: ExecutionResult
    evidence: tuple[AutomationEvidence, ...]


ExecutionCallable = Callable[[ExecutionRequest], AutomationExecution]


def authorize_execution(
    request: ExecutionRequest,
    authorization: ExecutionAuthorization,
) -> ExecutionRequest:
    if request.execution_id != authorization.execution_id:
        raise ValueError("authorization does not match execution")
    if authorization.scope != request.scope:
        raise ValueError("authorization scope does not match request")
    if not authorization.authorized:
        return replace(
            request,
            status=ExecutionStatus.BLOCKED,
            authorization_status="REJECTED",
        )
    return replace(
        request,
        authorized_by=authorization.authorized_by,
        authorization_status="AUTHORIZED",
        status=ExecutionStatus.AUTHORIZED,
    )


def execute_automation(
    request: ExecutionRequest,
    executor: ExecutionCallable,
) -> AutomationExecution:
    if request.authorization_status != "AUTHORIZED" or request.status is not ExecutionStatus.AUTHORIZED:
        raise ValueError("automation execution requires explicit authorization")

    outcome = executor(request)

    if outcome.result.execution_id != request.execution_id:
        raise ValueError("execution result does not match request")
    if outcome.result.automation_id != request.automation_id:
        raise ValueError("execution result does not match automation")

    evidence_ids = tuple(ev.evidence_id for ev in outcome.evidence)
    if outcome.result.evidence_ids != evidence_ids:
        raise ValueError("execution result evidence_ids do not match returned evidence")

    if outcome.result.status is ExecutionStatus.COMPLETED and not outcome.evidence:
        raise ValueError("completed automation requires returned evidence")
    if any(ev.execution_id != request.execution_id for ev in outcome.evidence):
        raise ValueError("automation evidence does not match execution")
    return outcome


def evidence_from_result(outcome: AutomationExecution) -> tuple[AutomationEvidence, ...]:
    """Return only explicit automation evidence; no result-to-learning inference."""
    return tuple(outcome.evidence)


__all__ = [
    "AutomationExecution",
    "AutomationEvidence",
    "ExecutionAuthorization",
    "ExecutionCallable",
    "ExecutionRequest",
    "ExecutionResult",
    "ExecutionStatus",
    "authorize_execution",
    "execute_automation",
    "evidence_from_result",
]
