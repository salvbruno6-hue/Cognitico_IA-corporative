"""Empirical performance memory for governed symbiotic routing.

This module records evidence about execution configurations. It does not
replace the canonical ExecutionRouter and does not mutate routing policy.
"""
from dataclasses import dataclass, field
from typing import Mapping, Tuple


@dataclass(frozen=True)
class ExecutionSignature:
    mission_type: str
    specialist_id: str
    model_id: str
    tool_ids: Tuple[str, ...] = ()
    context_profile: str = "default"
    method_id: str = "default"


@dataclass(frozen=True)
class PerformanceObservation:
    observation_id: str
    tenant_id: str
    signature: ExecutionSignature
    result_status: str
    quality_score: float | None = None
    outcome_score: float | None = None
    latency_ms: float | None = None
    cost: float | None = None
    evidence_ids: Tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    @property
    def empirical_score(self) -> float | None:
        scores = [s for s in (self.quality_score, self.outcome_score) if s is not None]
        if not scores:
            return None
        return sum(scores) / len(scores)


class PerformanceMemory:
    """Tenant-scoped observations used as evidence for future routing."""

    def __init__(self) -> None:
        self._observations: dict[str, PerformanceObservation] = {}

    def record(self, observation: PerformanceObservation) -> PerformanceObservation:
        if not observation.observation_id or not observation.tenant_id:
            raise ValueError("observation_id and tenant_id are required")
        if observation.observation_id in self._observations:
            raise ValueError("observation_id already exists")
        self._observations[observation.observation_id] = observation
        return observation

    def list_for_mission(
        self, tenant_id: str, mission_type: str
    ) -> tuple[PerformanceObservation, ...]:
        return tuple(
            item
            for item in self._observations.values()
            if item.tenant_id == tenant_id and item.signature.mission_type == mission_type
        )

    def summarize(self, tenant_id: str, mission_type: str) -> Mapping[ExecutionSignature, float]:
        grouped: dict[ExecutionSignature, list[float]] = {}
        for item in self.list_for_mission(tenant_id, mission_type):
            score = item.empirical_score
            if score is not None:
                grouped.setdefault(item.signature, []).append(score)
        return {
            signature: sum(scores) / len(scores)
            for signature, scores in grouped.items()
        }
