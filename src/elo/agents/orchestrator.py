"""Policy-bounded orchestration for ELO specialist agents."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from . import AgentObservation, AgentTask, AutonomyLevel
from .registry import AgentRegistry


class AgentExecutionDenied(PermissionError):
    """Raised when a task exceeds the agent's registered authority."""


@dataclass(frozen=True, slots=True)
class ToolContract:
    tool_id: str
    capability: str
    domain: str
    tenant_scope: str
    enabled: bool = True


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[tuple[str, str], ToolContract] = {}

    def register(self, tool: ToolContract) -> None:
        self._tools[(tool.tenant_scope, tool.tool_id)] = tool

    def authorize(self, tenant_id: str, tool_id: str, capability: str) -> ToolContract:
        tool = self._tools.get((tenant_id, tool_id))
        if tool is None or not tool.enabled or tool.capability != capability:
            raise AgentExecutionDenied(f"tool {tool_id!r} is not authorized")
        return tool


class AgentOrchestrator:
    """Validates delegation; actual tool execution remains an injected boundary."""

    def __init__(self, agents: AgentRegistry, tools: ToolRegistry) -> None:
        self.agents = agents
        self.tools = tools

    def dispatch(self, task: AgentTask, execute: Callable[[AgentTask], AgentObservation]) -> AgentObservation:
        agent = self.agents.get(task.tenant_id, task.agent_id)
        if agent.domain != task.domain:
            raise AgentExecutionDenied("agent domain does not match task domain")
        if not agent.can(task.required_output):
            raise AgentExecutionDenied("agent is not authorized for required output")
        if task.allowed_tools:
            for tool_id in task.allowed_tools:
                if tool_id not in agent.tools:
                    raise AgentExecutionDenied(f"tool {tool_id!r} is not registered for agent")
                self.tools.authorize(task.tenant_id, tool_id, task.required_output)
        if agent.autonomy_level in {AutonomyLevel.OBSERVE, AutonomyLevel.ANALYZE, AutonomyLevel.RECOMMEND} and task.constraints.get("requires_execution"):
            raise AgentExecutionDenied("execution requires an approval-capable autonomy level")
        observation = execute(task)
        if observation.tenant_id != task.tenant_id or observation.agent_id != task.agent_id:
            raise AgentExecutionDenied("agent observation identity mismatch")
        return observation
