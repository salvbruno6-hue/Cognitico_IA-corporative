"""Deterministic forecasting faculty for governed ELO budgeting.

This is a Core faculty, not an execution authority. It requires explicit,
proven historical observations and returns a GAP when evidence is insufficient.
The algorithm is intentionally provider-neutral and reproducible.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Mapping, Sequence


class ForecastStatus(StrEnum):
    COMPLETE = "COMPLETE"
    GAP = "GAP"


@dataclass(frozen=True, slots=True)
class ForecastObservation:
    period: str
    value: Decimal
    source_id: str
    provenance: Mapping[str, str]

    @classmethod
    def create(
        cls,
        *,
        period: str,
        value: Decimal | int | float | str,
        source_id: str,
        provenance: Mapping[str, str],
    ) -> "ForecastObservation":
        if not period or not source_id or not provenance:
            raise ValueError("period, source_id and provenance are required")
        try:
            parsed = Decimal(str(value))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("forecast value must be numeric") from exc
        if parsed < 0:
            raise ValueError("negative forecast observations are not accepted by the baseline")
        return cls(period, parsed, source_id, dict(provenance))


@dataclass(frozen=True, slots=True)
class ForecastResult:
    status: ForecastStatus
    target_period: str
    forecast: Decimal | None
    method: str
    observation_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    provenance: tuple[Mapping[str, str], ...]
    gap: str | None = None

    @property
    def reproducible(self) -> bool:
        return self.status is ForecastStatus.COMPLETE and bool(self.evidence_ids and self.provenance)


class GovernedForecastFaculty:
    """Provide a bounded moving-average forecast from governed observations."""

    METHOD = "ARITHMETIC_MEAN_V1"

    @classmethod
    def forecast(
        cls,
        *,
        observations: Sequence[ForecastObservation],
        target_period: str,
        window: int = 3,
    ) -> ForecastResult:
        if not target_period:
            raise ValueError("target_period is required")
        if window < 1:
            raise ValueError("window must be positive")
        if len(observations) < window:
            return ForecastResult(
                status=ForecastStatus.GAP,
                target_period=target_period,
                forecast=None,
                method=cls.METHOD,
                observation_ids=tuple(item.period for item in observations),
                evidence_ids=tuple(item.source_id for item in observations),
                provenance=tuple(dict(item.provenance) for item in observations),
                gap=f"at least {window} governed observations are required",
            )

        selected = tuple(observations[-window:])
        total = sum((item.value for item in selected), Decimal("0"))
        result = (total / Decimal(window)).quantize(Decimal("0.01"))
        return ForecastResult(
            status=ForecastStatus.COMPLETE,
            target_period=target_period,
            forecast=result,
            method=cls.METHOD,
            observation_ids=tuple(item.period for item in selected),
            evidence_ids=tuple(dict.fromkeys(item.source_id for item in selected)),
            provenance=tuple(dict(item.provenance) for item in selected),
        )
