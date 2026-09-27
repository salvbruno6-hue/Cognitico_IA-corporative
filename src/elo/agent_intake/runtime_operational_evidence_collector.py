"""Collect repeated runtime observations before operational-outcome evaluation.

This collector is an ephemeral aggregation boundary over the existing runtime
evidence sink. It does not create a persistence authority, Evolution Gate,
learning store, or promotion path.

Each append represents one runtime execution. Operational outcome evaluation is
available only after two or more distinct execution_ids for the same
candidate/owner/metric/direction tuple. The existing adapter remains the sole
conversion into FunctionalValueEvidence.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .runtime_operational_evidence import (
    InMemoryRuntimeEvidenceSink,
    RuntimeEvidenceSink,
    RuntimeOperationalEvidence,
)
from .runtime_operational_evidence_adapter import to_operational_outcome
from .hermes_functional_value_proof import FunctionalValueEvidence


@dataclass(frozen=True, slots=True)
class RuntimeEvidenceGroup:
    """One candidate-owned metric stream observed across runtime executions."""

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
    """Buffer independent runtime observations and expose ready evidence groups."""

    def __init__(self, *, sink: RuntimeEvidenceSink | None = None) -> None:
        self._sink = sink or InMemoryRuntimeEvidenceSink()

    def append(self, evidence: RuntimeOperationalEvidence) -> None:
        """Record one actual runtime observation; duplicate executions are rejected."""
        self._sink.append(evidence)

    def observations(self) -> tuple[RuntimeOperationalEvidence, ...]:
        return self._sink.list() if isinstance(self._sink, InMemoryRuntimeEvidenceSink) else ()

    def groups(self) -> tuple[RuntimeEvidenceGroup, ...]:
        grouped: dict[
            tuple[str, str, str, str],
            list[RuntimeOperationalEvidence],
        ] = defaultdict(list)
        for item in self.observations():
            grouped[
                (item.candidate_id, item.owner, item.metric, item.direction)
            ].append(item)

        return tuple(
            RuntimeEvidenceGroup(
                candidate_id=candidate_id,
                owner=owner,
                metric=metric,
                direction=direction,
                observations=tuple(items),
            )
            for (candidate_id, owner, metric, direction), items in sorted(grouped.items())
        )

    def ready_groups(self) -> tuple[RuntimeEvidenceGroup, ...]:
        """Return only streams with at least two independent runtime executions."""
        return tuple(group for group in self.groups() if group.repeatable)


__all__ = ["RuntimeEvidenceGroup", "RuntimeOperationalEvidenceCollector"]
