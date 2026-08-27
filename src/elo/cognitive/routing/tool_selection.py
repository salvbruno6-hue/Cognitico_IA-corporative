"""Capability-aware tool selection for the ELO runtime boundary."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolCandidate:
    tool_id: str
    capabilities: frozenset[str]
    reliability: float = 0.0
    latency_ms: float = 0.0
    cost: float = 0.0
    evidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def score(self) -> float:
        latency = 1.0 / (1.0 + max(self.latency_ms, 0.0) / 1000.0)
        cost = 1.0 / (1.0 + max(self.cost, 0.0))
        return 0.50 * self.reliability + 0.30 * self.evidence + 0.10 * latency + 0.10 * cost


class ToolSelector:
    def select(self, capability: str, candidates: list[ToolCandidate], *, minimum_score: float = 0.0) -> ToolCandidate:
        eligible = [tool for tool in candidates if capability in tool.capabilities]
        ranked = sorted(eligible, key=ToolCandidate.score, reverse=True)
        if not ranked:
            raise LookupError(f"no tool supports capability: {capability}")
        if ranked[0].score() < minimum_score:
            raise LookupError(f"no tool meets minimum score for capability: {capability}")
        return ranked[0]
