"""Collect repeated runtime observations before operational-outcome evaluation."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .hermes_functional_value_proof import FunctionalValueEvidence
from .runtime_operational_evidence import (
    InMemoryRuntimeEvidenceSink,
    RuntimeEvidenceSink,
    RuntimeOperationalEvidence,
)
from .runtime_operational_evidence_adapter import to_operational_outcome


@dataclass(frozen=True, slots=True)
class RuntimeEvidenceGroup:
    candidate_id: str
    owner: str
    metric: str
    direction: str
    observations: tuple[RuntimeOperationalEvidence, ...]

    @property
    def repeatable(self) -> bool:
        return len(self.observations) >= 2

    def to_operational_outcome(self) -> FunctionalValueEvidence:
        if not self.repeatable:
            raise ValueError("at least two distinct runtime executions are required")
        return to_operational_outcome(self.observations)


class RuntimeOperationalEvidenceCollector:
    """Ephemeral aggregation over the existing runtime evidence sink."""

    def __init__(self, *, sink: RuntimeEvidenceSink | None = None) -> None:
        self._sink = sink or InMemoryRuntimeEvidenceSink()
        self._observations: list[RuntimeOperationalEvidence] = []
        self._execution_ids: set[str] = set()

    def append(self, evidence: RuntimeOperationalEvidence) -> None:
        if evidence.execution_id in self._execution_ids:
            raise ValueError("duplicate execution_id")
        self._sink.append(evidence)
        self._execution_ids.add(evidence.execution_id)
        self._observations.append(evidence)

    def observations(self) -> tuple[RuntimeOperationalEvidence, ...]:
        return tuple(self._observations)

    def groups(self) -> tuple[RuntimeEvidenceGroup, ...]:
        grouped = defaultdict(list)
        for item in self._observations:
            key = (item.candidate_id, item.owner, item.metric, item.direction)
            grouped[key].append(item)
        return tuple(
            RuntimeEvidenceGroup(*key, tuple(items))
            for key, items in sorted(grouped.items())
        )

    def ready_groups(self) -> tuple[RuntimeEvidenceGroup, ...]:
        return tuple(group for group in self.groups() if group.repeatable)


__all__ = ["RuntimeEvidenceGroup", "RuntimeOperationalEvidenceCollector"]
