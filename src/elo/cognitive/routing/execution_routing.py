"""Unified cognitive routing decision.

Keeps capability, model and tool selection as separate concerns while
producing one auditable execution choice for the runtime.
"""

from dataclasses import dataclass
from typing import Any

from .model_selection import ModelCandidate, ModelSelector
from .tool_selection import ToolCandidate, ToolSelector


@dataclass(frozen=True)
class RoutingDecision:
    capability: str
    model_id: str | None
    tool_id: str | None
    rationale: str


class ExecutionRouter:
    def __init__(self, model_selector: ModelSelector, tool_selector: ToolSelector):
        self.model_selector = model_selector
        self.tool_selector = tool_selector

    def route(
        self,
        capability: str,
        *,
        models: list[ModelCandidate] | None = None,
        tools: list[ToolCandidate] | None = None,
        preferred_models: set[str] | None = None,
        minimum_model_score: float = 0.0,
        minimum_tool_score: float = 0.0,
    ) -> RoutingDecision:
        model = None
        tool = None
        if models:
            model = self.model_selector.select(
                capability, models,
                preferred=preferred_models,
                minimum_score=minimum_model_score,
            )
        if tools:
            tool = self.tool_selector.select(
                capability, tools,
                minimum_score=minimum_tool_score,
            )
        if model is None and tool is None:
            raise LookupError(f"no executable route for capability: {capability}")
        selected = [item for item in (model, tool) if item is not None]
        ids = ", ".join(item.model_id if hasattr(item, "model_id") else item.tool_id for item in selected)
        return RoutingDecision(
            capability=capability,
            model_id=model.model_id if model else None,
            tool_id=tool.tool_id if tool else None,
            rationale=f"selected by capability evidence: {ids}",
        )
