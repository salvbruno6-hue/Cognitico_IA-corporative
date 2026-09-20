"""Controlled evaluation of Hermes external memory-provider boundary."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_memory_provider_boundary import MemoryProviderDisposition, MemoryProviderSignal, assess_memory_provider

@dataclass(frozen=True)
class MemoryProviderEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix):
    return tuple(MemoryProviderSignal(
        provider_id=f"provider-{i}", tenant_scope="multiteiner",
        source_refs=(f"hermes:memory:{prefix.lower()}/{i}",),
        operation="read", evidence_digest=f"evidence-{i}",
        provenance_verified=True, explicit_activation=True,
        canonical_write=False, promotion_attempt=False
    ) for i in range(1,6))

def _rate(signals):
    return sum(assess_memory_provider(s).disposition is MemoryProviderDisposition.CANDIDATE for s in signals)/len(signals)

def _integrity(signals):
    return sum((a:=assess_memory_provider(s)).canonical_authority is False and a.mutation_permitted is False and a.promotion_permitted is False for s in signals)/len(signals)

def evaluate():
    baseline=_signals("BASE"); adapted=_signals("HERMES")
    b=_rate(baseline); a=_rate(adapted); i=_integrity(adapted)
    repeatable=_rate(_signals("REPEAT"))==a and i==1.0
    result="EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST"
    return MemoryProviderEvaluation(b,a,i,repeatable,result)
