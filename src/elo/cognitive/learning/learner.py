from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearningObservation:
    capability: str
    outcome: float
    tenant_id: str | None = None
    source: str = "runtime"


class ExperienceLearner:
    def __init__(self) -> None:
        self._observations: list[LearningObservation] = []

    def observe(self, observation: LearningObservation) -> None:
        if not 0.0 <= observation.outcome <= 1.0:
            raise ValueError("outcome must be between 0 and 1")
        self._observations.append(observation)

    def mean(self, capability: str, *, tenant_id: str | None = None) -> float:
        items = [x for x in self._observations if x.capability == capability and x.tenant_id == tenant_id]
        return sum(x.outcome for x in items) / len(items) if items else 0.0

    def count(self, capability: str, *, tenant_id: str | None = None) -> int:
        return sum(1 for x in self._observations if x.capability == capability and x.tenant_id == tenant_id)
