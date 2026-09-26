"""Controlled three-phase evaluation of EXT-BATCH-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_batch_adapter import adapt_batch
from .hermes_batch_boundary import BatchDisposition, BatchSignal

CAPABILITY_ID="EXT-BATCH-HERMES"
PRIMARY_METRIC="bounded_batch_intake_integrity_rate"
METRIC_DIRECTION="maximize"

@dataclass(frozen=True, slots=True)
class BatchEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix):
    return tuple(BatchSignal(f"{prefix}-{i}","multiteiner",(f"hermes:batch:{prefix.lower()}/{i}",),
                             f"task-{i}",5,True,True,"schema-v1",False,False) for i in range(1,6))

def _integrity(contracts):
    return sum(c is not None and c.disposition is BatchDisposition.CANDIDATE
               and not c.execution_permitted and not c.canonical_authority and not c.promotion_permitted
               for c in contracts)/len(contracts)

def evaluate():
    baseline=0.0
    adapted_contracts=tuple(adapt_batch(s) for s in _signals("HERMES"))
    repeat_contracts=tuple(adapt_batch(s) for s in _signals("REPEAT"))
    adapted=sum(c is not None for c in adapted_contracts)/len(adapted_contracts)
    integrity=_integrity(adapted_contracts)
    repeatable=sum(c is not None for c in repeat_contracts)/len(repeat_contracts)==adapted and _integrity(repeat_contracts)==1.0
    result="EVOLUTION_GATE_REQUIRED" if adapted>baseline and repeatable and integrity==1.0 else "RETEST"
    return BatchEvaluation(baseline,adapted,integrity,repeatable,result)
