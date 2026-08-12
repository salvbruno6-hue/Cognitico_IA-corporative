"""Governed specialist-agent contracts for ELO-003."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class AutonomyLevel(str, Enum):
    OBSERVE = "L0"
    ANALYZE = "L1"
    RECOMMEND = "L2"
    APPROVAL = "L3"
    POLICY_BOUNDED = "L4"
    GOVERNED_AUTONOMY = "L5"


@dataclass(frozen=True, slots=True)
class AgentContract:
    agent_id: str
    agent_name: str
    agent_version: str
    tenant_scope: str
    domain: str
    capabilities: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    policy_profile: str = "default"
    autonomy_level: AutonomyLevel = AutonomyLevel.OBSERVE
    status: str = "ACTIVE"
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def can(self, capability: str) -> bool:
        return capability in self.capabilities


@dataclass(frozen=True, slots=True)
class AgentTask:
    task_id: str
    agent_id: str
    tenant_id: str
    domain: str
    objective: str
    context_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    constraints: Mapping[str, Any] = field(default_factory=dict)
    allowed_tools: tuple[str, ...] = ()
    required_output: str = "observation"
    time_budget_ms: int | None = None
    policy: str = "default"


@dataclass(frozen=True, slots=True)
class AgentObservation:
    observation_id: str
    agent_id: str
    tenant_id: str
    domain: str
    subject: str
    observation: str
    evidence_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    questions: tuple[str, ...] = ()
    recommended_next_step: str | None = None
    provenance: Mapping[str, Any] = field(default_factory=dict)
