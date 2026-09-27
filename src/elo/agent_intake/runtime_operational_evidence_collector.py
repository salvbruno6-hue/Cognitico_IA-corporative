"""Observational collector for repeated runtime operational evidence.

The collector owns no persistence or governance authority. It reuses the
configured RuntimeEvidenceSink for immutable observations and delegates
classification to the canonical runtime operational evidence adapter.
"""

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
class RuntimeEvidenceKey:
    candidate_id: str
    owner: str
    runtime_entrypoint: str
    metric: str
    direction: str


@dataclass(frozen=True, slots=True)
class RuntimeEvidenceGroup:
    candidate_id: str
    owner: str
    metric: str
    direction: str
    observations: tuple[RuntimeOperationalEvidence, ...]
    runtime_entrypoint: str

    @property
    def repeatable(self) -> bool:
        return len(self.observations) >= 2

    def to_operational_outcome(self) -> FunctionalValueEvidence:
        if not self.repeatable:
            raise ValueError("at least two distinct runtime executions are required")
        return to_operational_outcome(self.observations)


class RuntimeOperationalEvidenceCollector:
    """Ephemeral aggregation over the existing runtime evidence sink."""

    def __init__(self, sink: RuntimeEvidenceSink | None = None) -> None:
        self._sink = sink or InMemoryRuntimeEvidenceSink()
        self._observations: list[RuntimeOperationalEvidence] = []
        self._execution_ids: set[str] = set()

    def append(self, evidence: RuntimeOperationalEvidence) -> None:
        if evidence.execution_id in self._execution_ids:
            raise ValueError("duplicate execution_id")
        self._sink.append(evidence)
        self._execution_ids.add(evidence.execution_id)
        self._observations.append(evidence)

    def observe(self, evidence: RuntimeOperationalEvidence) -> None:
        self.append(evidence)

    def observations(
        self, key: RuntimeEvidenceKey | None = None
    ) -> tuple[RuntimeOperationalEvidence, ...]:
        observations = tuple(self._observations)
        if key is None:
            return observations
        return tuple(
            item
            for item in observations
            if item.candidate_id == key.candidate_id
            and item.owner == key.owner
            and item.runtime_entrypoint == key.runtime_entrypoint
            and item.metric == key.metric
            and item.direction == key.direction
        )

    def groups(self) -> tuple[RuntimeEvidenceGroup, ...]:
        grouped: dict[tuple[str, str, str, str, str], list[RuntimeOperationalEvidence]] = defaultdict(list)
        for item in self._observations:
            key = (
                item.candidate_id,
                item.owner,
                item.metric,
                item.direction,
                item.runtime_entrypoint,
            )
            grouped[key].append(item)
        return tuple(
            RuntimeEvidenceGroup(
                candidate_id=key[0],
                owner=key[1],
                metric=key[2],
                direction=key[3],
                observations=tuple(items),
                runtime_entrypoint=key[4],
            )
            for key, items in sorted(grouped.items())
        )

    def ready_groups(self) -> tuple[RuntimeEvidenceGroup, ...]:
        return tuple(group for group in self.groups() if group.repeatable)

    def outcome(self, key: RuntimeEvidenceKey) -> FunctionalValueEvidence:
        observations = self.observations(key)
        if not observations:
            raise ValueError("no runtime observations for evidence key")
        return to_operational_outcome(observations)


__all__ = [
    "RuntimeEvidenceGroup",
    "RuntimeEvidenceKey",
    "RuntimeOperationalEvidenceCollector",
]
