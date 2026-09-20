"""Controlled evaluation of Hermes batch-processing boundary."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_batch_boundary import BatchDisposition, BatchSignal, assess_batch

CAPABILITY_ID="EXT-BATCH-HERMES"

@dataclass(frozen=True)
class BatchEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix):
    return tuple(BatchSignal(
        batch_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        source_refs=(f"hermes:batch:{prefix.lower()}/{i}",),
        task_digest=f"task-{i}", item_count=5, bounded=True,
        explicit_authorization=True, result_schema_digest="schema-v1",
        canonical_mutation=False, promotion_attempt=False
    ) for i in range(1,6))

def _rate(signals):
    return sum(assess_batch(s).disposition is BatchDisposition.CANDIDATE for s in signals)/len(signals)

def _integrity(signals):
    return sum((a:=assess_batch(s)).canonical_authority is False and a.execution_permitted is False and a.promotion_permitted is False for s in signals)/len(signals)

def evaluate():
    baseline=_signals("BASE"); adapted=_signals("HERMES")
    b=_rate(baseline); a=_rate(adapted); i=_integrity(adapted)
    repeatable=_rate(_signals("REPEAT"))==a and i==1.0
    result="EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST"
    return BatchEvaluation(b,a,i,repeatable,result)
