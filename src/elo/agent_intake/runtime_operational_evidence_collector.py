"""Observational collector for repeated runtime operational evidence.

The collector owns no persistence or governance authority. It reuses the
configured RuntimeEvidenceSink for immutable observations and delegates
classification to the canonical runtime operational evidence adapter.
"""

from __future__ import annotations

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


class RuntimeOperationalEvidenceCollector:
    """Collect real executions without becoming a learning or promotion owner."""

    def __init__(self, sink: RuntimeEvidenceSink | None = None) -> None:
        self._sink = sink or InMemoryRuntimeEvidenceSink()

    def observe(self, evidence: RuntimeOperationalEvidence) -> None:
        self._sink.append(evidence)

    def observations(self, key: RuntimeEvidenceKey) -> tuple[RuntimeOperationalEvidence, ...]:
        list_items = getattr(self._sink, "list", None)
        if list_items is None:
            raise TypeError("collector requires a readable RuntimeEvidenceSink")
        return tuple(
            item
            for item in list_items()
            if item.candidate_id == key.candidate_id
            and item.owner == key.owner
            and item.runtime_entrypoint == key.runtime_entrypoint
            and item.metric == key.metric
            and item.direction == key.direction
        )

    def outcome(self, key: RuntimeEvidenceKey) -> FunctionalValueEvidence:
        observations = self.observations(key)
        if not observations:
            raise ValueError("no runtime observations for evidence key")
        return to_operational_outcome(observations)


__all__ = ["RuntimeEvidenceKey", "RuntimeOperationalEvidenceCollector"]
