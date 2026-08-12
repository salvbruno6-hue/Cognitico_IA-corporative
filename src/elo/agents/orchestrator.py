"""Governed dispatch boundary for specialist agents."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from .governance import AgentRegistry, AgentTask, AgentAuthorizationError

@dataclass(frozen=True, slots=True)
class ToolContract:
    tool_id: str; tenant_id: str; domain: str; capability: str; enabled: bool=True

class ToolRegistry:
    def __init__(self): self._tools={}
    def register(self, tool): self._tools[(tool.tenant_id,tool.tool_id)]=tool
    def authorize(self, task, tool_id):
        tool=self._tools.get((task.tenant_id,tool_id))
        if not tool or not tool.enabled or tool.domain!=task.domain or tool.capability!=task.required_capability:
            raise AgentAuthorizationError("tool is not authorized for task")
        return tool

class AgentOrchestrator:
    def __init__(self, agents: AgentRegistry, tools: ToolRegistry): self.agents=agents; self.tools=tools
    def dispatch(self, task: AgentTask, executor: Callable[[AgentTask], object]):
        self.agents.authorize(task)
        for tool_id in task.allowed_tools: self.tools.authorize(task,tool_id)
        return executor(task)
