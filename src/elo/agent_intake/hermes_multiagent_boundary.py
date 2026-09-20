"""Candidate-only governance boundary for Hermes subagent delegation."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

CAPABILITY_ID = "EXT-MULTIAGENT-HERMES"

class DelegationDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class DelegationSignal:
    delegation_id: str
    tenant_scope: str
    parent_agent_id: str
    child_agent_id: str
    goal_digest: str
    source_refs: Tuple[str, ...]
    resource_scope: Tuple[str, ...] = ()
    output_schema_digest: str | None = None
    provenance_verified: bool = False
    isolated_context: bool = False
    child_authority: bool = False

@dataclass(frozen=True)
class DelegationAssessment:
    delegation_id: str
    child_agent_id: str
    disposition: DelegationDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    execution_permitted: bool = False
    promotion_permitted: bool = False

def assess_delegation(signal: DelegationSignal) -> DelegationAssessment:
    if not signal.delegation_id or not signal.tenant_scope or not signal.parent_agent_id or not signal.child_agent_id:
        return DelegationAssessment(signal.delegation_id, signal.child_agent_id, DelegationDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.goal_digest or not signal.source_refs or not signal.provenance_verified:
        return DelegationAssessment(signal.delegation_id, signal.child_agent_id, DelegationDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.isolated_context:
        return DelegationAssessment(signal.delegation_id, signal.child_agent_id, DelegationDisposition.OBSERVATION, tuple(signal.source_refs))
    if signal.child_authority:
        return DelegationAssessment(signal.delegation_id, signal.child_agent_id, DelegationDisposition.REJECTED, tuple(signal.source_refs))
    return DelegationAssessment(signal.delegation_id, signal.child_agent_id, DelegationDisposition.CANDIDATE, tuple(signal.source_refs))
