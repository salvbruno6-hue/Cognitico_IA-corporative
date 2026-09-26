"""Controlled three-phase evaluation of EXT-CRON-HERMES."""
from __future__ import annotations

from dataclasses import dataclass

from .hermes_cron_adapter import adapt_schedule
from .hermes_cron_boundary import ScheduleDisposition, ScheduleSignal

CAPABILITY_ID = "EXT-CRON-HERMES"
PRIMARY_METRIC = "bounded_schedule_registration_integrity_rate"
METRIC_DIRECTION = "maximize"


@dataclass(frozen=True, slots=True)
class CronEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str


def _signals(prefix: str) -> tuple[ScheduleSignal, ...]:
    return tuple(
        ScheduleSignal(
            f"{prefix}-{i}", "multiteiner", f"task-{i}",
            (f"hermes:cron:{prefix.lower()}/{i}",),
            "0 8 * * *", "elo", True, True, True, False
        )
        for i in range(1, 6)
    )


def _adapted_rate(signals: tuple[ScheduleSignal, ...]) -> float:
    contracts = tuple(adapt_schedule(signal) for signal in signals)
    return sum(contract is not None for contract in contracts) / len(contracts)


def _integrity(contracts) -> float:
    return sum(
        contract is not None
        and contract.disposition is ScheduleDisposition.CANDIDATE
        and contract.execution_permitted is False
        and contract.canonical_authority is False
        and bool(contract.idempotency_key)
        for contract in contracts
    ) / len(contracts)


def evaluate() -> CronEvaluation:
    baseline = 0.0
    adapted_contracts = tuple(adapt_schedule(signal) for signal in _signals("HERMES"))
    repeat_contracts = tuple(adapt_schedule(signal) for signal in _signals("REPEAT"))
    adapted = sum(contract is not None for contract in adapted_contracts) / len(adapted_contracts)
    integrity = _integrity(adapted_contracts)
    repeatable = (
        sum(contract is not None for contract in repeat_contracts) / len(repeat_contracts) == adapted
        and _integrity(repeat_contracts) == 1.0
    )
    result = (
        "EVOLUTION_GATE_REQUIRED"
        if adapted > baseline and repeatable and integrity == 1.0
        else "RETEST"
    )
    return CronEvaluation(baseline, adapted, integrity, repeatable, result)
