"""Bounded, idempotent and evidence-bearing productivity execution contract."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol


class ProductivityExecutionError(ValueError):
    """Raised when a workflow cannot be safely executed or reported."""


@dataclass(frozen=True)
class ProductivityWorkflow:
    workflow_id: str
    tenant_id: str
    execution_id: str
    steps: tuple[str, ...]
    idempotency_key: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]


@dataclass(frozen=True)
class ProductivityOutcome:
    execution_id: str
    status: str
    evidence_ids: tuple[str, ...]
    observed_outcome: str


class ProductivityExecutor(Protocol):
    def execute(self, workflow: ProductivityWorkflow) -> ProductivityOutcome:
        """Execute a previously authorized workflow through an adapter."""


class NativeProductivityBoundary:
    """Validate workflow intent; adapters remain downstream executors."""

    _STATUSES = {"SUCCESS", "PARTIAL", "FAILED"}
    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    def prepare(
        self,
        *,
        workflow_id: str,
        tenant_id: str,
        execution_id: str,
        steps: tuple[str, ...] | list[str],
        idempotency_key: str,
        evidence_ids: tuple[str, ...] | list[str],
        provenance: Mapping[str, str],
    ) -> ProductivityWorkflow:
        if any(not str(v).strip() for v in (workflow_id, tenant_id, execution_id, idempotency_key)):
            raise ProductivityExecutionError("workflow identity, tenant, execution and idempotency key are required")
        if not steps:
            raise ProductivityExecutionError("at least one bounded workflow step is required")
        if any(key.lower() in self._SECRET_KEYS for key in provenance):
            raise ProductivityExecutionError("secret-bearing provenance is forbidden")
        return ProductivityWorkflow(
            workflow_id=workflow_id.strip(), tenant_id=tenant_id.strip(), execution_id=execution_id.strip(),
            steps=tuple(step.strip() for step in steps if step.strip()),
            idempotency_key=idempotency_key.strip(), evidence_ids=tuple(evidence_ids),
            provenance=dict(provenance),
        )

    def validate_outcome(self, workflow: ProductivityWorkflow, outcome: ProductivityOutcome) -> ProductivityOutcome:
        if outcome.execution_id != workflow.execution_id:
            raise ProductivityExecutionError("outcome execution identity does not match workflow")
        if outcome.status not in self._STATUSES:
            raise ProductivityExecutionError("invalid productivity outcome status")
        if outcome.status == "SUCCESS" and (not outcome.evidence_ids or not outcome.observed_outcome.strip()):
            raise ProductivityExecutionError("successful execution requires evidence and observed outcome")
        if outcome.status != "SUCCESS" and outcome.observed_outcome.strip().lower() in {"success", "ok", "completed"}:
            raise ProductivityExecutionError("non-success execution cannot report success")
        return outcome
