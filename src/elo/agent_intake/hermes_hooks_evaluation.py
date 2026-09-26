"""Controlled evaluation of Hermes lifecycle-hook intake boundary."""
from __future__ import annotations
from dataclasses import dataclass
from src.elo.agent_intake.hermes_hooks_boundary import HookSignal, assess_hook, HookDisposition

@dataclass(frozen=True)
class HookEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix):
    return tuple(HookSignal(
        hook_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        source_refs=(f"hermes:hook:{prefix.lower()}/{i}",),
        event_name="lifecycle", handler_digest=f"digest-{i}",
        explicit_activation=True, mutates_canonical_state=False,
        bypasses_governance=False
    ) for i in range(1,6))

def _rate(signals):
    return sum(assess_hook(s).disposition is HookDisposition.CANDIDATE for s in signals)/len(signals)

def _integrity(signals):
    return sum((a:=assess_hook(s)).canonical_authority is False and a.execution_permitted is False and a.mutation_permitted is False for s in signals)/len(signals)

def evaluate():
    baseline=_signals("BASE"); adapted=_signals("HERMES")
    b=_rate(baseline); a=_rate(adapted); i=_integrity(adapted)
    repeatable=_rate(_signals("REPEAT"))==a and i==1.0
    result="EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST"
    return HookEvaluation(b,a,i,repeatable,result)
