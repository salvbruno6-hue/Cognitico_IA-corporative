"""Governed workflow runtime boundary for ELO.

External schedulers/orchestrators remain replaceable adapters. The workflow
runtime composes existing canonical ELO capabilities and never becomes a
source of truth, policy authority, or second cognitive core.
"""
from dataclasses import dataclass, field
from typing import Callable, Mapping

VALID_STATES = {"BLOCKED", "FAILED", "PARTIAL", "COMPLETED", "REQUIRES_HUMAN_REVIEW"}
BLOCKED = "BLOCKED"


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
    capability_ids: tuple[str, ...] = ()
    action_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    response: object | None = None

    def start(self) -> "WorkflowRun":
        if not self.workflow_id or not self.run_id or not self.tenant_id or not self.request_id or not self.trigger:
            raise ValueError("workflow_id, run_id, tenant_id, request_id and trigger are required")
        return self

    def finish(self, status: str) -> "WorkflowRun":
        if status not in VALID_STATES:
            raise ValueError(f"invalid workflow status: {status}")
        return WorkflowRun(**{**self.__dict__, "outcome_status": status})


class GovernedWorkflowRuntime:
    """Coordinate TRIGGER through LEARN using injected canonical boundaries."""

    def execute(
        self,
        run: WorkflowRun,
        *,
        build_context: Callable[[WorkflowRun], object],
        analyze: Callable[[WorkflowRun, object], object],
        decide: Callable[[WorkflowRun, object], object],
        authorize: Callable[[WorkflowRun, object], bool],
        execute_action: Callable[[WorkflowRun, object], object],
        observe: Callable[[WorkflowRun, object], tuple[str, ...]],
        record_outcome: Callable[[WorkflowRun, object], WorkflowRun],
        learn: Callable[[WorkflowRun, object], object],
        capability_ids: tuple[str, ...] = (),
        action_ids: tuple[str, ...] = (),
    ) -> WorkflowRun:
        run = run.start()
        run = WorkflowRun(**{**run.__dict__, "capability_ids": tuple(capability_ids), "action_ids": tuple(action_ids)})
        context = build_context(run)
        analysis = analyze(run, context)
        decision = decide(run, analysis)
        allowed = authorize(run, decision)
        run = WorkflowRun(**{**run.__dict__, "authorization_status": "ALLOW" if allowed else "DENY"})
        if not allowed:
            return run.finish(BLOCKED)
        response = execute_action(run, decision)
        evidence_ids = tuple(observe(run, response))
        run = WorkflowRun(**{**run.__dict__, "evidence_ids": evidence_ids, "response": response})
        run = record_outcome(run, response)
        if run.outcome_status not in VALID_STATES:
            raise ValueError(f"record_outcome returned invalid workflow status: {run.outcome_status}")
        learn(run, response)
        return run
