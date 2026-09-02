"""Governed agent runtime boundary for ELO.

This module intentionally provides orchestration primitives only. It does not
create a second cognitive core, memory authority, policy authority or model
provider registry.
"""
from dataclasses import dataclass, field
from typing import Mapping, Tuple


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


class GovernedAgentRuntime:
    """Create auditable run envelopes; execution remains capability-governed."""

    def start(self, run: AgentRun) -> AgentRun:
        if not run.tenant_id or not run.principal_id or not run.request_id:
            raise ValueError("tenant_id, principal_id and request_id are required")
        return run

    def authorize(self, run: AgentRun, status: str) -> AgentRun:
        return AgentRun(**{**run.__dict__, "authorization_status": status})

    def complete(self, run: AgentRun, outcome_status: str) -> AgentRun:
        return AgentRun(**{**run.__dict__, "outcome_status": outcome_status})
