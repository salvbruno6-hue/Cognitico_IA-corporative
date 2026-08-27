"""Structured, tenant-scoped performance evidence for adaptive routing.

Evidence is non-canonical. Runtime observations may inform routing only after
passing the existing Forge/governance promotion path.
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
    tenant_id: str
    capability: str
    context_key: str
    model_id: str | None
    tool_id: str | None
    observations: int
    mean_quality: float
    mean_reliability: float
    mean_efficiency: float
    confidence: float

    @property
    def evidence_state(self) -> str:
        return "measured" if self.observations else "none"

    @property
    def promotion_state(self) -> str:
        return "candidate" if self.observations > 0 else "none"


def aggregate(
    evidence: list[PerformanceEvidence],
    *,
    minimum_observations: int = 1,
) -> list[PerformanceAggregate]:
    """Aggregate without crossing tenant, context, capability or executor scope."""
    if minimum_observations < 1:
        raise ValueError("minimum_observations must be at least 1")

    groups: dict[tuple[str, str, str, str | None, str | None], list[PerformanceEvidence]] = {}
    for item in evidence:
        item.validate()
        key = (item.tenant_id, item.capability, item.context_key, item.model_id, item.tool_id)
        groups.setdefault(key, []).append(item)

    result: list[PerformanceAggregate] = []
    for (tenant_id, capability, context_key, model_id, tool_id), items in groups.items():
        if len(items) < minimum_observations:
            continue
        efficiency = [1.0 / (1.0 + x.latency_ms / 1000.0 + x.cost) for x in items]
        observations = len(items)
        # Confidence rises with repeated verified observations and is bounded at 1.
        confidence = min(1.0, observations / (observations + 4.0))
        result.append(PerformanceAggregate(
            tenant_id=tenant_id,
            capability=capability,
            context_key=context_key,
            model_id=model_id,
            tool_id=tool_id,
            observations=observations,
            mean_quality=sum(x.quality for x in items) / observations,
            mean_reliability=sum(x.reliability for x in items) / observations,
            mean_efficiency=sum(efficiency) / observations,
            confidence=confidence,
        ))
    return result


def to_routing_metadata(aggregate_result: PerformanceAggregate) -> dict[str, Any]:
    """Expose measured evidence while preserving tenant scope and promotion gate."""
    return {
        "tenant_id": aggregate_result.tenant_id,
        "capability": aggregate_result.capability,
        "context_key": aggregate_result.context_key,
        "model_id": aggregate_result.model_id,
        "tool_id": aggregate_result.tool_id,
        "observations": aggregate_result.observations,
        "quality": aggregate_result.mean_quality,
        "reliability": aggregate_result.mean_reliability,
        "efficiency": aggregate_result.mean_efficiency,
        "confidence": aggregate_result.confidence,
        "evidence_state": aggregate_result.evidence_state,
        "promotion_state": aggregate_result.promotion_state,
    }
