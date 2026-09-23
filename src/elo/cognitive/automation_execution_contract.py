"""Governed automation contracts for the canonical ELO execution loop.

These contracts are process boundaries only. They do not authorize themselves,
execute work, write learning memory, promote knowledge, or mutate canonical
state.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class ExecutionStatus(StrEnum):
    REQUESTED = "REQUESTED"
    AUTHORIZED = "AUTHORIZED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    ESCALATED = "ESCALATED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    execution_id: str
    tenant_id: str
    source_observation_id: str
    decision_id: str
    action: str
    scope: str
    evidence_ids: tuple[str, ...]
    authorized_by: str | None
    authorization_status: str
    automation_id: str
    status: ExecutionStatus = ExecutionStatus.REQUESTED

    def __post_init__(self) -> None:
        if not all(
            (
                self.execution_id,
                self.tenant_id,
                self.source_observation_id,
                self.decision_id,
                self.action,
                self.scope,
                self.automation_id,
            )
        ):
            raise ValueError("execution request requires identity, action, scope and automation")
        if not self.evidence_ids:
            raise ValueError("execution request requires evidence")
        if self.status is ExecutionStatus.AUTHORIZED and not self.authorized_by:
            raise ValueError("authorized execution requires authorized_by")
        if self.authorization_status not in {"PENDING", "AUTHORIZED", "REJECTED"}:
            raise ValueError("unsupported authorization status")


@dataclass(frozen=True, slots=True)
class ExecutionAuthorization:
    execution_id: str
    authorized: bool
    authorized_by: str
    scope: str
    reason: str
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not all((self.execution_id, self.authorized_by, self.scope, self.reason)):
            raise ValueError("authorization requires identity, actor, scope and reason")
        if self.authorized and not self.evidence_ids:
            raise ValueError("authorization requires evidence")


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    execution_id: str
    automation_id: str
    status: ExecutionStatus
    result_ref: str | None
    evidence_ids: tuple[str, ...]
    started_at: str | None
    finished_at: str | None
    message: str = ""
    metadata: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if not self.execution_id or not self.automation_id:
            raise ValueError("execution result requires identity")
        if self.status in {ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.ROLLED_BACK} and not self.evidence_ids:
            raise ValueError("terminal execution results require evidence")
        if self.status is ExecutionStatus.COMPLETED and not self.result_ref:
            raise ValueError("completed execution requires result_ref")


@dataclass(frozen=True, slots=True)
class AutomationEvidence:
    evidence_id: str
    execution_id: str
    source_ref: str
    source_kind: str
    observed_at: str
    summary: str
    attributes: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if not all((self.evidence_id, self.execution_id, self.source_ref, self.source_kind, self.observed_at, self.summary)):
            raise ValueError("automation evidence requires identity, provenance and summary")
        if self.source_kind.lower() not in {"runtime", "benchmark", "repository", "pr", "issue", "human"}:
            raise ValueError("unsupported automation evidence source kind")


__all__ = [
    "AutomationEvidence",
    "ExecutionAuthorization",
    "ExecutionRequest",
    "ExecutionResult",
    "ExecutionStatus",
]
