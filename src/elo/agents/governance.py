"""Governance primitives for ELO specialist-agent execution."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

class AutonomyLevel(StrEnum):
    OBSERVE="L0"; ANALYZE="L1"; RECOMMEND="L2"; APPROVAL="L3"; POLICY_BOUNDED="L4"; GOVERNED_AUTONOMY="L5"

@dataclass(frozen=True, slots=True)
class AgentContract:
    agent_id: str; version: str; tenant_id: str; domain: str
    capabilities: tuple[str,...]=(); tools: tuple[str,...]=(); autonomy: AutonomyLevel=AutonomyLevel.OBSERVE; policy: str="default"; active: bool=True

@dataclass(frozen=True, slots=True)
class AgentTask:
    task_id: str; agent_id: str; tenant_id: str; domain: str; objective: str; required_capability: str
    allowed_tools: tuple[str,...]=(); requires_execution: bool=False; policy: str="default"

class AgentAuthorizationError(PermissionError): pass

class AgentRegistry:
    def __init__(self): self._agents={}
    def register(self, agent): self._agents[(agent.tenant_id,agent.agent_id)]=agent
    def authorize(self, task):
        agent=self._agents.get((task.tenant_id,task.agent_id))
        if not agent or not agent.active: raise AgentAuthorizationError("agent is unavailable for tenant")
        if agent.domain!=task.domain: raise AgentAuthorizationError("agent/domain mismatch")
        if task.required_capability not in agent.capabilities: raise AgentAuthorizationError("capability is not authorized")
        if task.policy!=agent.policy: raise AgentAuthorizationError("policy mismatch")
        if task.requires_execution and agent.autonomy not in {AutonomyLevel.APPROVAL,AutonomyLevel.POLICY_BOUNDED,AutonomyLevel.GOVERNED_AUTONOMY}: raise AgentAuthorizationError("autonomy level cannot execute this task")
        if any(tool not in agent.tools for tool in task.allowed_tools): raise AgentAuthorizationError("tool is not authorized")
        return agent
