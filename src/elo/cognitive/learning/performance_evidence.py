"""Structured performance evidence used by adaptive cognitive routing.

Evidence is tenant-scoped and non-canonical. It can influence future ranking
only after the normal Forge/governance promotion path.
"""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PerformanceEvidence:
    tenant_id: str
    capability: str
    context_key: str
    model_id: str | None
    tool_id: str | None
    verified: bool
    quality: float
    reliability: float
    latency_ms: float
    cost: float
    provenance: str

    def validate(self) -> None:
        if not self.tenant_id or not self.capability or not self.context_key or not self.provenance:
            raise ValueError("tenant, capability, context and provenance are required")
        for name, value in (("quality", self.quality), ("reliability", self.reliability)):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.latency_ms < 0 or self.cost < 0:
            raise ValueError("latency and cost cannot be negative")
        if not self.verified:
            raise ValueError("unverified execution cannot become performance evidence")


@dataclass(frozen=True)
class PerformanceAggregate:
    capability: str
    model_id: str | None
    tool_id: str | None
    observations: int
    mean_quality: float
    mean_reliability: float
    mean_efficiency: float


def aggregate(evidence: list[PerformanceEvidence]) -> list[PerformanceAggregate]:
    """Aggregate only within identical tenant/capability/context/executor scope."""
    groups: dict[tuple[str, str, str, str | None, str | None], list[PerformanceEvidence]] = {}
    for item in evidence:
        item.validate()
        key = (item.tenant_id, item.capability, item.context_key, item.model_id, item.tool_id)
        groups.setdefault(key, []).append(item)

    result: list[PerformanceAggregate] = []
    for (_, capability, _, model_id, tool_id), items in groups.items():
        efficiency = [1.0 / (1.0 + x.latency_ms / 1000.0 + x.cost) for x in items]
        result.append(PerformanceAggregate(
            capability=capability,
            model_id=model_id,
            tool_id=tool_id,
            observations=len(items),
            mean_quality=sum(x.quality for x in items) / len(items),
            mean_reliability=sum(x.reliability for x in items) / len(items),
            mean_efficiency=sum(efficiency) / len(efficiency),
        ))
    return result


def to_routing_metadata(aggregate_result: PerformanceAggregate) -> dict[str, Any]:
    """Expose measured evidence as metadata; never promote it to Canon."""
    return {
        "observations": aggregate_result.observations,
        "quality": aggregate_result.mean_quality,
        "reliability": aggregate_result.mean_reliability,
        "efficiency": aggregate_result.mean_efficiency,
        "evidence_state": "measured",
        "promotion_state": "candidate",
    }
