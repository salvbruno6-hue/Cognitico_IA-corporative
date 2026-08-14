"""Governance primitives for ELO specialist-agent execution."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping


class AutonomyLevel(StrEnum):
    OBSERVE = "L0"
    ANALYZE = "L1"
    RECOMMEND = "L2"
    APPROVAL = "L3"
    POLICY_BOUNDED = "L4"
    GOVERNED_AUTONOMY = "L5"


@dataclass(frozen=True, slots=True)
class AgentContract:
    agent_id: str
    version: str
    tenant_id: str
    domain: str
    capabilities: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    autonomy: AutonomyLevel = AutonomyLevel.OBSERVE
    policy: str = "default"
    active: bool = True
    provenance: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AgentTask:
    task_id: str
    agent_id: str
    tenant_id: str
    domain: str
    objective: str
    required_capability: str
    allowed_tools: tuple[str, ...] = ()
    requires_execution: bool = False
    policy: str = "default"
    context_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()


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


class AgentAuthorizationError(PermissionError):
    """Raised when an agent/task/tool exceeds registered authority."""


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[tuple[str, str], AgentContract] = {}

    def register(self, agent: AgentContract) -> None:
        self._agents[(agent.tenant_id, agent.agent_id)] = agent

    def authorize(self, task: AgentTask) -> AgentContract:
        agent = self._agents.get((task.tenant_id, task.agent_id))
        if not agent or not agent.active:
            raise AgentAuthorizationError("agent is unavailable for tenant")
        if agent.domain != task.domain:
            raise AgentAuthorizationError("agent/domain mismatch")
        if task.required_capability not in agent.capabilities:
            raise AgentAuthorizationError("capability is not authorized")
        if task.policy != agent.policy:
            raise AgentAuthorizationError("policy mismatch")
        if task.requires_execution and agent.autonomy not in {
            AutonomyLevel.APPROVAL,
            AutonomyLevel.POLICY_BOUNDED,
            AutonomyLevel.GOVERNED_AUTONOMY,
        }:
            raise AgentAuthorizationError("autonomy level cannot execute this task")
        if any(tool not in agent.tools for tool in task.allowed_tools):
            raise AgentAuthorizationError("tool is not authorized")
        return agent
