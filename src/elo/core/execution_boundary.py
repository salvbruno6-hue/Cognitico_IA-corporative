"""Governed execution boundary for ELO's Observe -> Analyze -> Execute -> Monitor cycle.

Execution is deliberately separate from cognitive recommendation. A caller must provide
an explicit authorization token and a correlation context; failed preconditions return a
non-executing outcome instead of attempting a best-effort action.
"""
from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping, Protocol


class ExecutionStatus(StrEnum):
    READY = "READY"
    BLOCKED = "BLOCKED"
    EXECUTED = "EXECUTED"
    MONITORING = "MONITORING"
    DEGRADED = "DEGRADED"


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str
    tenant_id: str
    principal_id: str
    action_id: str
    authorization_id: str | None
    evidence_ids: tuple[str, ...] = ()
    correlation_id: str | None = None
    expected_impact: str | None = None


@dataclass(frozen=True)
class ExecutionOutcome:
    request_id: str
    status: ExecutionStatus
    executed: bool
    reason: str
    provenance: Mapping[str, str]


class ExecutionAdapter(Protocol):
    def execute(self, request: ExecutionRequest) -> Mapping[str, str]: ...


def validate_execution_request(request: ExecutionRequest) -> ExecutionOutcome | None:
    """Return a blocking outcome when mandatory execution controls are absent."""
    missing: list[str] = []
    for name, value in (
        ("tenant_id", request.tenant_id),
        ("principal_id", request.principal_id),
        ("action_id", request.action_id),
        ("authorization_id", request.authorization_id),
        ("correlation_id", request.correlation_id),
    ):
        if not value:
            missing.append(name)
    if not request.evidence_ids:
        missing.append("evidence_ids")
    if missing:
        return ExecutionOutcome(
            request_id=request.request_id,
            status=ExecutionStatus.BLOCKED,
            executed=False,
            reason="missing_execution_controls:" + ",".join(missing),
            provenance={"execution": "not_attempted"},
        )
    return None


def execute_governed(request: ExecutionRequest, adapter: ExecutionAdapter) -> ExecutionOutcome:
    """Execute only after all governance controls pass; never silently downgrade them."""
    blocked = validate_execution_request(request)
    if blocked is not None:
        return blocked
    result = dict(adapter.execute(request))
    result.update(
        {
            "request_id": request.request_id,
            "tenant_id": request.tenant_id,
            "principal_id": request.principal_id,
            "authorization_id": request.authorization_id or "",
            "correlation_id": request.correlation_id or "",
            "execution": "executed",
        }
    )
    return ExecutionOutcome(
        request_id=request.request_id,
        status=ExecutionStatus.EXECUTED,
        executed=True,
        reason="authorized_execution_completed",
        provenance=result,
    )
