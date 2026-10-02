"""Runtime bridge for EXT-PROFILE-HERMES over the real agent-context execution boundary.

The adapter reuses AgentOrchestrator.dispatch and AgentTask.context_refs.
It records evidence only; it does not create profile authority or mutate
canonical/shared state.
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

CAPABILITY_ID = "EXT-PROFILE-HERMES"


@dataclass(frozen=True, slots=True)
class ProfileRuntimeObservation:
    contract: ProfileContract
    task: AgentTask
    observation: AgentObservation
    evidence: RuntimeOperationalEvidence


def execute_profile_with_runtime_evidence(
    signal: ProfileSignal,
    *,
    orchestrator: AgentOrchestrator,
    agent_id: str,
    required_capability: str,
    domain: str,
    executor: Callable[[AgentTask], AgentObservation],
    source_commit: str,
    runtime_trace: str,
    execution_id: str,
) -> ProfileRuntimeObservation | None:
    contract = adapt_profile(signal)
    if contract is None:
        return None

    task = AgentTask(
        task_id=f"{contract.profile_id}:{execution_id}",
        agent_id=agent_id,
        tenant_id=contract.tenant_scope,
        domain=domain,
        objective=f"bounded profile execution:{contract.profile_id}",
        required_capability=required_capability,
        context_refs=contract.source_refs,
        evidence_refs=contract.source_refs,
        requires_execution=True,
    )
    observation = orchestrator.dispatch(task, executor)
    provenance = observation.provenance
    integrity = (
        provenance.get("profile_id") == contract.profile_id
        and provenance.get("identity_digest") == contract.identity_digest
        and tuple(provenance.get("context_refs", ())) == contract.source_refs
        and observation.tenant_id == contract.tenant_scope
        and task.context_refs == contract.source_refs
    )
    evidence = create_runtime_evidence(
        execution_id=execution_id,
        candidate_id=CAPABILITY_ID,
        owner="ELO Agent Context & Delegation",
        runtime_entrypoint="AgentOrchestrator.dispatch",
        action_observed=True,
        metric="collision_free_profile_task_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0 if integrity else 0.0,
        attribution="candidate",
        provenance=RuntimeProvenance(commit=source_commit, runtime_trace=runtime_trace),
        regression=not integrity,
        repeatability=RepeatabilityEvidence(
            executions=1,
            successful=1 if integrity else 0,
            rate=1.0 if integrity else 0.0,
        ),
    )
    return ProfileRuntimeObservation(contract, task, observation, evidence)
