"""Bounded delegation adapter for EXT-MULTIAGENT-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_multiagent_boundary import DelegationDisposition, DelegationSignal, assess_delegation

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

def adapt_delegation(signal: DelegationSignal) -> DelegatedWorkItem | None:
    return MultiagentAdapter().adapt(signal)

__all__ = ["DelegatedWorkItem", "MultiagentAdapter", "adapt_delegation"]
