"""Tenant-aware registry for specialist agents."""
from __future__ import annotations

from . import AgentContract


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[tuple[str, str], AgentContract] = {}

    def register(self, agent: AgentContract) -> None:
        key = (agent.tenant_scope, agent.agent_id)
        existing = self._agents.get(key)
        if existing and existing.agent_version != agent.agent_version:
            raise ValueError(f"agent {agent.agent_id} already registered with another version")
        self._agents[key] = agent

    def get(self, tenant_id: str, agent_id: str) -> AgentContract:
        try:
            return self._agents[(tenant_id, agent_id)]
        except KeyError as exc:
            raise KeyError(f"agent {agent_id!r} is not registered for tenant {tenant_id!r}") from exc

    def authorize(self, tenant_id: str, agent_id: str, *, capability: str, tool_id: str | None = None) -> AgentContract:
        agent = self.get(tenant_id, agent_id)
        if agent.status != "ACTIVE":
            raise PermissionError("agent is not active")
        if not agent.can(capability):
            raise PermissionError(f"agent is not authorized for capability {capability!r}")
        if tool_id is not None and tool_id not in agent.tools:
            raise PermissionError(f"agent is not authorized for tool {tool_id!r}")
        return agent
