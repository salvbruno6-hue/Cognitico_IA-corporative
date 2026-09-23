"""Bridge from an authorized automation result into the canonical lab boundary.

This module only assembles the existing SymbiontLabObservation contract from
explicit execution evidence and explicit laboratory fields.
"""

from __future__ import annotations

from dataclasses import dataclass

from .automation_execution_contract import AutomationEvidence, ExecutionResult, ExecutionStatus
from .symbionte_lab import SymbiontLabObservation


@dataclass(frozen=True, slots=True)
class AutomationLabHandoff:
    observation: SymbiontLabObservation
    execution: ExecutionResult


def prepare_automation_lab_handoff(
    execution: ExecutionResult,
    evidence: tuple[AutomationEvidence, ...],
    *,
    tenant_id: str,
    decision_id: str,
    observation_id: str,
    source_commit: str,
    hypothesis: str,
    baseline: str,
    experiment: str,
    result: str,
    regression_status: str,
    generalization_status: str,
    risk: str,
    scope: str,
    existing_owner: str | None = None,
) -> AutomationLabHandoff:
    if execution.status is not ExecutionStatus.COMPLETED:
        raise ValueError("laboratory handoff requires a completed execution")
    if not execution.result_ref:
        raise ValueError("laboratory handoff requires execution result_ref")
    if not evidence:
        raise ValueError("laboratory handoff requires automation evidence")
    if any(item.execution_id != execution.execution_id for item in evidence):
        raise ValueError("automation evidence does not match execution")
    evidence_ids = tuple(dict.fromkeys(item.evidence_id for item in evidence))
    if set(execution.evidence_ids) != set(evidence_ids):
        raise ValueError("execution evidence_ids must match returned evidence")

    observation = SymbiontLabObservation(
        observation_id=observation_id,
        tenant_id=tenant_id,
        domain="AUTOMATION_EXECUTION",
        decision_id=decision_id,
        expected_outcome=hypothesis,
        observed_outcome=result,
        evidence_ids=evidence_ids,
        source_ref=execution.result_ref,
        source_commit=source_commit,
        hypothesis=hypothesis,
        baseline=baseline,
        experiment=experiment,
        result=result,
        regression_status=regression_status,
        generalization_status=generalization_status,
        risk=risk,
        existing_owner=existing_owner,
        scope=scope,
        tenant_scope=tenant_id,
        source_kind="runtime",
    )
    return AutomationLabHandoff(observation=observation, execution=execution)
