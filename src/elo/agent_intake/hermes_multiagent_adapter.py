"""Bounded delegation adapter for EXT-MULTIAGENT-HERMES.

The runtime bridge composes this candidate with the existing governed
AgentOrchestrator. It does not create a child-agent authority, scheduler,
promotion path, or canonical mutation path.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.agents.governance import AgentAuthorizationError, AgentObservation, AgentTask
from elo.agents.orchestrator import AgentOrchestrator
from .hermes_multiagent_boundary import DelegationDisposition, DelegationSignal, assess_delegation
from .runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)


@dataclass(frozen=True, slots=True)
class DelegatedWorkItem:
    delegation_id: str
    tenant_scope: str
    parent_agent_id: str
    child_agent_id: str
    goal_digest: str
    resource_scope: tuple[str, ...]
    source_refs: tuple[str, ...]
    isolated_context: bool
    child_authority: bool = False
    promotion_permitted: bool = False


@dataclass(frozen=True, slots=True)
class MultiagentRuntimeObservation:
    work_item: DelegatedWorkItem
    child_task: AgentTask
    observation: AgentObservation
    evidence: RuntimeOperationalEvidence


class MultiagentAdapter:
    """Materialize a bounded delegation contract without spawning a child."""

    def adapt(self, signal: DelegationSignal) -> DelegatedWorkItem | None:
        assessment = assess_delegation(signal)
        if assessment.disposition is not DelegationDisposition.CANDIDATE:
            return None
        return DelegatedWorkItem(
            delegation_id=signal.delegation_id,
            tenant_scope=signal.tenant_scope,
            parent_agent_id=signal.parent_agent_id,
            child_agent_id=signal.child_agent_id,
            goal_digest=signal.goal_digest,
            resource_scope=signal.resource_scope,
            source_refs=assessment.evidence_refs,
            isolated_context=signal.isolated_context,
        )


def dispatch_delegation_with_runtime_evidence(
    signal: DelegationSignal,
    *,
    orchestrator: AgentOrchestrator,
    parent_task: AgentTask,
    child_required_capability: str,
    executor: Callable[[AgentTask], AgentObservation],
    source_commit: str,
    runtime_trace: str,
    execution_id: str,
) -> MultiagentRuntimeObservation | None:
    """Execute one bounded delegation through the existing agent runtime boundary.

    The parent is authorized first. The child task receives only the candidate's
    verified resource scope and provenance refs. Execution remains owned by the
    existing AgentOrchestrator.
    """
    work_item = MultiagentAdapter().adapt(signal)
    if work_item is None:
        return None

    if parent_task.agent_id != work_item.parent_agent_id or parent_task.tenant_id != work_item.tenant_scope:
        raise AgentAuthorizationError("delegation parent does not match authorized parent task")

    orchestrator.agents.authorize(parent_task)

    child_task = AgentTask(
        task_id=work_item.delegation_id,
        agent_id=work_item.child_agent_id,
        tenant_id=work_item.tenant_scope,
        domain=parent_task.domain,
        objective=work_item.goal_digest,
        required_capability=child_required_capability,
        allowed_tools=(),
        requires_execution=True,
        policy=parent_task.policy,
        context_refs=work_item.resource_scope,
        evidence_refs=work_item.source_refs + (work_item.delegation_id,),
    )
    observation = orchestrator.dispatch(child_task, executor)

    contract_integrity = (
        work_item.isolated_context
        and child_task.context_refs == work_item.resource_scope
        and observation.agent_id == work_item.child_agent_id
        and observation.tenant_id == work_item.tenant_scope
    )
    evidence = create_runtime_evidence(
        execution_id=execution_id,
        candidate_id="EXT-MULTIAGENT-HERMES",
        owner="ELO Agent Delegation",
        runtime_entrypoint="AgentOrchestrator.dispatch",
        action_observed=True,
        metric="delegated_context_contract_integrity",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0 if contract_integrity else 0.0,
        attribution="candidate",
        provenance=RuntimeProvenance(commit=source_commit, runtime_trace=runtime_trace),
        regression=not contract_integrity,
        repeatability=RepeatabilityEvidence(executions=1, successful=1 if contract_integrity else 0, rate=1.0 if contract_integrity else 0.0),
    )
    return MultiagentRuntimeObservation(work_item, child_task, observation, evidence)


def adapt_delegation(signal: DelegationSignal) -> DelegatedWorkItem | None:
    return MultiagentAdapter().adapt(signal)


__all__ = [
    "DelegatedWorkItem",
    "MultiagentAdapter",
    "MultiagentRuntimeObservation",
    "adapt_delegation",
    "dispatch_delegation_with_runtime_evidence",
]
