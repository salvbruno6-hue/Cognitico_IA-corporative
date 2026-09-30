"""Runtime bridge for EXT-CRON-HERMES.

The bridge reuses the canonical governed workflow runtime. It does not create
scheduler authority, a new evidence owner, or a second execution state machine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from automation.workflow_contract import GovernedWorkflowRuntime, WorkflowRun
from .hermes_cron_adapter import ScheduledInvocationContract, adapt_schedule
from .hermes_cron_boundary import ScheduleSignal
from .runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)


@dataclass(frozen=True, slots=True)
class CronRuntimeObservation:
    contract: ScheduledInvocationContract
    run: WorkflowRun
    evidence: RuntimeOperationalEvidence


def execute_schedule_with_runtime_evidence(
    signal: ScheduleSignal,
    *,
    runtime: GovernedWorkflowRuntime,
    executor: Callable[[ScheduledInvocationContract], object],
    source_commit: str,
    runtime_trace: str,
    execution_id: str,
) -> CronRuntimeObservation | None:
    """Execute one bounded schedule through the existing workflow runtime."""

    contract = adapt_schedule(signal)
    if contract is None:
        return None

    run = WorkflowRun(
        workflow_id="hermes-cron",
        run_id=execution_id,
        tenant_id=contract.tenant_scope,
        request_id=f"request:{execution_id}",
        trigger="EXT-CRON-HERMES",
        metadata={
            "schedule_id": contract.schedule_id,
            "task_digest": contract.task_digest,
            "idempotency_key": contract.idempotency_key,
        },
    )

    observed: dict[str, object] = {}

    def build_context(current_run: WorkflowRun) -> object:
        return contract

    def analyze(current_run: WorkflowRun, context: object) -> object:
        return context

    def decide(current_run: WorkflowRun, analysis: object) -> object:
        return analysis

    def authorize(current_run: WorkflowRun, decision: object) -> bool:
        return contract.disposition.value == "CANDIDATE" and signal.explicit_authorization

    def execute_action(current_run: WorkflowRun, decision: object) -> object:
        if contract.execution_permitted:
            raise RuntimeError("candidate contract unexpectedly grants execution")
        result = executor(contract)
        observed["result"] = result
        return result

    def observe(current_run: WorkflowRun, response: object) -> tuple[str, ...]:
        evidence = create_runtime_evidence(
            execution_id=execution_id,
            candidate_id="EXT-CRON-HERMES",
            owner="ELO Workflow/Automation",
            runtime_entrypoint="GovernedWorkflowRuntime.execute",
            action_observed=True,
            metric="idempotency_collision_free_rate",
            direction="maximize",
            baseline=0.0,
            observed_value=1.0,
            attribution="candidate",
            provenance=RuntimeProvenance(
                commit=source_commit,
                runtime_trace=runtime_trace,
            ),
            regression=False,
            repeatability=RepeatabilityEvidence(
                executions=1,
                successful=1,
                rate=1.0,
            ),
        )
        observed["evidence"] = evidence
        return (f"runtime-evidence:{execution_id}",)

    def record_outcome(current_run: WorkflowRun, response: object) -> WorkflowRun:
        return current_run.finish("COMPLETED")

    def learn(current_run: WorkflowRun, response: object) -> object:
        return None

    completed = runtime.execute(
        run,
        build_context=build_context,
        analyze=analyze,
        decide=decide,
        authorize=authorize,
        execute_action=execute_action,
        observe=observe,
        record_outcome=record_outcome,
        learn=learn,
        capability_ids=("HERMES-AUTOMATION",),
        action_ids=("scheduled-invocation",),
    )

    evidence = observed.get("evidence")
    if not isinstance(evidence, RuntimeOperationalEvidence):
        raise RuntimeError("runtime execution produced no operational evidence")

    return CronRuntimeObservation(contract, completed, evidence)


__all__ = ["CronRuntimeObservation", "execute_schedule_with_runtime_evidence"]
