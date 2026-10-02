"""Runtime bridge for EXT-PROFILE-HERMES.

The candidate reuses the canonical AgentOrchestrator execution boundary. It
only constrains the task context to the verified profile contract and records
runtime observations; it does not create profile authority, memory, routing,
or promotion paths.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.agents.governance import AgentObservation, AgentTask
from elo.agents.orchestrator import AgentOrchestrator

from .hermes_profile_adapter import ProfileContract, adapt_profile
from .hermes_profile_boundary import ProfileSignal
from .runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)


@dataclass(frozen=True, slots=True)
class ProfileRuntimeObservation:
    profile: ProfileContract
    task: AgentTask
    observation: AgentObservation
    evidence: RuntimeOperationalEvidence


def dispatch_profile_with_runtime_evidence(
    signal: ProfileSignal,
    *,
    orchestrator: AgentOrchestrator,
    task: AgentTask,
    executor: Callable[[AgentTask], AgentObservation],
    source_commit: str,
    runtime_trace: str,
    execution_id: str,
) -> ProfileRuntimeObservation | None:
    """Dispatch one profile-bounded task through the existing orchestrator."""
    profile = adapt_profile(signal)
    if profile is None:
        return None

    if task.tenant_id != profile.tenant_scope:
        raise ValueError("profile/task tenant mismatch")
    if task.context_refs:
        raise ValueError("profile runtime requires an empty task context before binding")

    bound_task = AgentTask(
        task_id=task.task_id,
        agent_id=task.agent_id,
        tenant_id=task.tenant_id,
        domain=task.domain,
        objective=task.objective,
        required_capability=task.required_capability,
        allowed_tools=task.allowed_tools,
        requires_execution=task.requires_execution,
        policy=task.policy,
        context_refs=(f"profile:{profile.profile_id}",) + profile.source_refs,
        evidence_refs=task.evidence_refs + profile.source_refs,
    )

    observation = orchestrator.dispatch(bound_task, executor)
    context_integrity = (
        bound_task.tenant_id == profile.tenant_scope
        and bound_task.context_refs == (f"profile:{profile.profile_id}",) + profile.source_refs
        and observation.tenant_id == profile.tenant_scope
        and not profile.shared_canonical_memory
        and not profile.authority_transfer
        and not profile.execution_permitted
        and not profile.promotion_permitted
    )

    evidence = create_runtime_evidence(
        execution_id=execution_id,
        candidate_id="EXT-PROFILE-HERMES",
        owner="ELO Agent Context & Delegation",
        runtime_entrypoint="AgentOrchestrator.dispatch",
        action_observed=True,
        metric="collision_free_profile_task_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0 if context_integrity else 0.0,
        attribution="candidate",
        provenance=RuntimeProvenance(commit=source_commit, runtime_trace=runtime_trace),
        regression=not context_integrity,
        repeatability=RepeatabilityEvidence(
            executions=1,
            successful=1 if context_integrity else 0,
            rate=1.0 if context_integrity else 0.0,
        ),
    )
    return ProfileRuntimeObservation(profile, bound_task, observation, evidence)


__all__ = ["ProfileRuntimeObservation", "dispatch_profile_with_runtime_evidence"]
