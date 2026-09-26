"""Controlled three-phase evaluation of EXT-MEMPROVIDER-HERMES."""
from __future__ import annotations

from dataclasses import dataclass

from .hermes_memory_provider_adapter import adapt_memory_provider
from .hermes_memory_provider_boundary import MemoryProviderDisposition, MemoryProviderSignal

CAPABILITY_ID = "EXT-MEMPROVIDER-HERMES"
PRIMARY_METRIC = "bounded_memory_provider_request_integrity_rate"
METRIC_DIRECTION = "maximize"


@dataclass(frozen=True, slots=True)
class MemoryProviderEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str


def _signals(prefix: str) -> tuple[MemoryProviderSignal, ...]:
    return tuple(
        MemoryProviderSignal(
            f"provider-{i}", "multiteiner",
            (f"hermes:memory:{prefix.lower()}/{i}",),
            "retrieve", f"sha256:{prefix.lower()}-{i}",
            True, True, False, False,
        )
        for i in range(1, 6)
    )


def _integrity(contracts) -> float:
    return sum(
        contract is not None
        and contract.disposition is MemoryProviderDisposition.CANDIDATE
        and contract.memory_authority is False
        and contract.mutation_permitted is False
        and contract.promotion_permitted is False
        for contract in contracts
    ) / len(contracts)


def evaluate() -> MemoryProviderEvaluation:
    baseline = 0.0
    adapted_contracts = tuple(adapt_memory_provider(signal) for signal in _signals("HERMES"))
    repeat_contracts = tuple(adapt_memory_provider(signal) for signal in _signals("REPEAT"))
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
    return MemoryProviderEvaluation(baseline, adapted, integrity, repeatable, result)
