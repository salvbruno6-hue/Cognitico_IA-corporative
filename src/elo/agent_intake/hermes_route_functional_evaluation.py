"""Candidate-specific functional evaluation for EXT-ROUTE-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_routing_adapter import adapt_routing
from .hermes_routing_boundary import RoutingSignal

@dataclass(frozen=True, slots=True)
class RoutingFunctionalEvidence:
    baseline_unsafe_route_admission_block_rate: float
    adapted_unsafe_route_admission_block_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _signals(prefix: str) -> tuple[RoutingSignal, ...]:
    # These requests carry an explicit governance-bypass flag. A real route
    # admission task must reject them rather than materialize a route plan.
    return tuple(
        RoutingSignal(
            f"{prefix}-{i}",
            "multiteiner",
            (f"controlled-eval:route-functional/{prefix.lower()}/{i}",),
            "provider-a",
            ("provider-b",),
            "bounded-pool-v1",
            True, True, False, True,
        )
        for i in (1, 2)
    )

def _baseline(signals: tuple[RoutingSignal, ...]) -> float:
    # Failure mode: naive route admission ignores the governance-bypass flag.
    admitted = tuple(bool(s.primary_provider and s.tenant_scope) for s in signals)
    return float(sum(not value for value in admitted) / len(admitted))

def _adapted(signals: tuple[RoutingSignal, ...]) -> float:
    contracts = tuple(adapt_routing(s) for s in signals)
    return sum(contract is None for contract in contracts) / len(contracts)

def evaluate_route_functional_gain() -> RoutingFunctionalEvidence:
    baseline_signals = _signals("BASELINE")
    adapted_signals = _signals("HERMES")
    baseline = _baseline(baseline_signals)
    adapted = _adapted(adapted_signals)
    repeatable = _adapted(_signals("REPEAT")) == adapted
    boundary = all(
        adapt_routing(signal) is None
        for signal in adapted_signals
    )
    refs = tuple(ref for signal in adapted_signals for ref in signal.source_refs)
    return RoutingFunctionalEvidence(
        baseline, adapted, repeatable, boundary, refs
    )
