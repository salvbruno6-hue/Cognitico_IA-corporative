"""Controlled three-phase evaluation of EXT-ROUTE-HERMES."""
from __future__ import annotations

from dataclasses import dataclass

from .hermes_routing_adapter import adapt_routing
from .hermes_routing_boundary import RoutingDisposition, RoutingSignal

CAPABILITY_ID = "EXT-ROUTE-HERMES"
PRIMARY_METRIC = "bounded_routing_plan_integrity_rate"
METRIC_DIRECTION = "maximize"


@dataclass(frozen=True, slots=True)
class RoutingEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str


def _signals(prefix: str) -> tuple[RoutingSignal, ...]:
    return tuple(
        RoutingSignal(
            f"{prefix}-{i}", "multiteiner",
            (f"hermes:routing:{prefix.lower()}/{i}",),
            "provider-a", ("provider-b",), "bounded-pool-v1",
            True, True, False, False,
        )
        for i in range(1, 6)
    )


def _integrity(contracts) -> float:
    return sum(
        contract is not None
        and contract.disposition is RoutingDisposition.CANDIDATE
        and contract.execution_permitted is False
        and contract.canonical_authority is False
        and contract.governance_bypass_permitted is False
        for contract in contracts
    ) / len(contracts)


def evaluate() -> RoutingEvaluation:
    baseline = 0.0
    adapted_contracts = tuple(adapt_routing(signal) for signal in _signals("HERMES"))
    repeat_contracts = tuple(adapt_routing(signal) for signal in _signals("REPEAT"))
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
    return RoutingEvaluation(baseline, adapted, integrity, repeatable, result)
