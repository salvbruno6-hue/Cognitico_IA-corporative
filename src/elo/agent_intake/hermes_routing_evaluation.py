"""Controlled evaluation of Hermes provider-routing boundary."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_routing_boundary import RoutingDisposition, RoutingSignal, assess_routing

@dataclass(frozen=True)
class RoutingEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix):
    return tuple(RoutingSignal(
        route_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        source_refs=(f"hermes:routing:{prefix.lower()}/{i}",),
        primary_provider="provider-a", fallback_providers=("provider-b",),
        credential_pool_strategy="bounded-pool-v1", provenance_verified=True,
        explicit_policy=True
    ) for i in range(1,6))

def _rate(signals):
    return sum(assess_routing(s).disposition is RoutingDisposition.CANDIDATE for s in signals)/len(signals)

def _integrity(signals):
    return sum((a:=assess_routing(s)).canonical_authority is False and a.execution_permitted is False and a.governance_bypass_permitted is False for s in signals)/len(signals)

def evaluate():
    baseline=_signals("BASE"); adapted=_signals("HERMES")
    b=_rate(baseline); a=_rate(adapted); i=_integrity(adapted)
    repeatable=_rate(_signals("REPEAT"))==a and i==1.0
    result="EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST"
    return RoutingEvaluation(b,a,i,repeatable,result)
