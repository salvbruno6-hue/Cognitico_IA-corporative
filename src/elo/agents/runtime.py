"""Governed agent runtime boundary for ELO.

The runtime composes existing canonical capabilities. It does not create a
second cognitive core, memory authority, policy authority, or provider registry.
"""
from dataclasses import dataclass, field
from typing import Callable, Mapping, Tuple


BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class AgentRun:
    run_id: str
    tenant_id: str
    principal_id: str
    request_id: str
    agent_id: str
    capability_ids: Tuple[str, ...] = ()
    evidence_ids: Tuple[str, ...] = ()
    authorization_status: str = "NOT_EVALUATED"
    outcome_status: str = "PENDING"
    provenance: Mapping[str, str] = field(default_factory=dict)
    response: object | None = None


class GovernedAgentRuntime:
    """Coordinate an agent run through injected canonical capabilities."""

    def start(self, run: AgentRun) -> AgentRun:
        if not run.tenant_id or not run.principal_id or not run.request_id:
            raise ValueError("tenant_id, principal_id and request_id are required")
        return run

    def execute(
        self,
        run: AgentRun,
        *,
        select_capabilities: Callable[[AgentRun], Tuple[str, ...]],
        collect_evidence: Callable[[AgentRun], Tuple[str, ...]],
        reason: Callable[[AgentRun], object],
        authorize: Callable[[AgentRun, object], bool],
        execute_action: Callable[[AgentRun, object], object],
        record_outcome: Callable[[AgentRun, object], AgentRun],
    ) -> AgentRun:
        """Execute only after capability, evidence, reasoning and authorization gates."""
        run = self.start(run)
        capabilities = tuple(select_capabilities(run))
        run = AgentRun(**{**run.__dict__, "capability_ids": capabilities})

        evidence = tuple(collect_evidence(run))
        run = AgentRun(**{**run.__dict__, "evidence_ids": evidence})
        if not evidence:
            return AgentRun(**{**run.__dict__, "outcome_status": BLOCKED})

        reasoning = reason(run)
        allowed = authorize(run, reasoning)
        run = AgentRun(
            **{
                **run.__dict__,
                "authorization_status": "ALLOW" if allowed else "DENY",
            }
        )
        if not allowed:
            return AgentRun(**{**run.__dict__, "outcome_status": BLOCKED})

        result = execute_action(run, reasoning)
        completed = AgentRun(
            **{**run.__dict__, "outcome_status": "COMPLETED", "response": result}
        )
        return record_outcome(completed, result)

    def authorize(self, run: AgentRun, status: str) -> AgentRun:
        return AgentRun(**{**run.__dict__, "authorization_status": status})

    def complete(self, run: AgentRun, outcome_status: str) -> AgentRun:
        return AgentRun(**{**run.__dict__, "outcome_status": outcome_status})
