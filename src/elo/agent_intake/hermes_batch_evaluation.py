"""Controlled evaluation of the Hermes batch-processing boundary."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_batch_boundary import BatchDisposition, BatchSignal, assess_batch

CAPABILITY_ID = "EXT-BATCH-HERMES"

@dataclass(frozen=True)
class BatchEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str):
    return tuple(BatchSignal(
        batch_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        source_refs=(f"hermes:batch:{prefix.lower()}/{i}",),
        task_digest=f"task-{i}", item_count=5, bounded=True,
        explicit_authorization=True, result_schema_digest="schema-v1",
        canonical_mutation=False, promotion_attempt=False
    ) for i in range(1, 6))

def _rate(signals) -> float:
    return sum(assess_batch(s).disposition is BatchDisposition.CANDIDATE for s in signals) / len(signals)

def _integrity(signals) -> float:
    return sum(
        (a := assess_batch(s)).canonical_authority is False
        and a.execution_permitted is False
        and a.promotion_permitted is False
        for s in signals
    ) / len(signals)

def evaluate() -> BatchEvaluation:
    baseline = _signals("BASE")
    adapted = _signals("HERMES")
    baseline_rate = _rate(baseline)
    adapted_rate = _rate(adapted)
    integrity = _integrity(adapted)
    repeatable = _rate(_signals("REPEAT")) == adapted_rate and integrity == 1.0
    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"
    return BatchEvaluation(baseline_rate, adapted_rate, integrity, repeatable, result)
