"""Bounded batch-evaluation intake adapter."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_batch_boundary import BatchDisposition, BatchSignal, assess_batch

@dataclass(frozen=True, slots=True)
class BatchIntakeContract:
    batch_id: str
    tenant_scope: str
    task_digest: str
    item_count: int
    result_schema_digest: str
    source_refs: tuple[str, ...]
    disposition: BatchDisposition
    execution_permitted: bool = False
    canonical_authority: bool = False
    promotion_permitted: bool = False

class BatchAdapter:
    def adapt(self, signal: BatchSignal) -> BatchIntakeContract | None:
        assessment=assess_batch(signal)
        if assessment.disposition is not BatchDisposition.CANDIDATE:
            return None
        return BatchIntakeContract(signal.batch_id,signal.tenant_scope,signal.task_digest,signal.item_count,
                                   signal.result_schema_digest,assessment.evidence_refs,assessment.disposition)

def adapt_batch(signal: BatchSignal) -> BatchIntakeContract | None:
    return BatchAdapter().adapt(signal)
