"""Non-authoritative timing observations for the ELO cognitive response path.

This module measures execution stages only. It does not authorize, route,
persist canonical knowledge, select providers, or change cognitive decisions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol


@dataclass(frozen=True, slots=True)
class CognitiveTimingObservation:
    stage: str
    duration_ms: float
    correlation_id: str = ""
    requirement_key: str = ""
    candidate_count: int = 0
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.stage.strip():
            raise ValueError("timing stage is required")
        if self.duration_ms < 0:
            raise ValueError("duration_ms cannot be negative")
        if self.candidate_count < 0:
            raise ValueError("candidate_count cannot be negative")


class CognitiveTimingSink(Protocol):
    def record(self, observation: CognitiveTimingObservation) -> None: ...


class InMemoryCognitiveTimingSink:
    """Ephemeral collector for tests/diagnostics; never a persistence authority."""

    def __init__(self) -> None:
        self._observations: list[CognitiveTimingObservation] = []

    def record(self, observation: CognitiveTimingObservation) -> None:
        self._observations.append(observation)

    @property
    def observations(self) -> tuple[CognitiveTimingObservation, ...]:
        return tuple(self._observations)


__all__ = [
    "CognitiveTimingObservation",
    "CognitiveTimingSink",
    "InMemoryCognitiveTimingSink",
]
