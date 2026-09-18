"""Evidence-backed confidence calibration for closed decision outcomes."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationObservation:
    confidence: float
    outcome_score: float
    decision_id: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not 0.0 <= self.outcome_score <= 1.0:
            raise ValueError("outcome_score must be between 0 and 1")
        if not self.decision_id:
            raise ValueError("decision_id is required")


class ConfidenceCalibration:
    """Accumulates observations without rewriting historical confidence."""

    def __init__(self, bins: int = 10) -> None:
        if bins < 2:
            raise ValueError("bins must be >= 2")
        self._bins = bins
        self._observations: list[CalibrationObservation] = []

    def add(self, observation: CalibrationObservation) -> None:
        self._observations.append(observation)

    def observations(self) -> tuple[CalibrationObservation, ...]:
        return tuple(self._observations)

    def reliability(self) -> tuple[dict[str, float | int], ...]:
        result = []
        for index in range(self._bins):
            low = index / self._bins
            high = (index + 1) / self._bins
            bucket = [
                item for item in self._observations
                if low <= item.confidence < high
                or (index == self._bins - 1 and low <= item.confidence <= high)
            ]
            if not bucket:
                continue
            result.append({
                "lower": low,
                "upper": high,
                "count": len(bucket),
                "mean_confidence": sum(x.confidence for x in bucket) / len(bucket),
                "mean_outcome": sum(x.outcome_score for x in bucket) / len(bucket),
            })
        return tuple(result)
