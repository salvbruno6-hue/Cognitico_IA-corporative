"""Minimal governed workflow execution envelope.

External schedulers/orchestrators remain replaceable adapters.
"""
from dataclasses import dataclass, field
from typing import Mapping


VALID_STATES = {"BLOCKED", "FAILED", "PARTIAL", "COMPLETED", "REQUIRES_HUMAN_REVIEW"}


@dataclass(frozen=True)
class WorkflowRun:
    workflow_id: str
    run_id: str
    tenant_id: str
    request_id: str
    trigger: str
    authorization_status: str = "NOT_EVALUATED"
    outcome_status: str = "PENDING"
    metadata: Mapping[str, str] = field(default_factory=dict)

    def finish(self, status: str) -> "WorkflowRun":
        if status not in VALID_STATES:
            raise ValueError(f"invalid workflow status: {status}")
        return WorkflowRun(**{**self.__dict__, "outcome_status": status})
