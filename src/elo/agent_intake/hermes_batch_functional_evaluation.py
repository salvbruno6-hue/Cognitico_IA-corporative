"""Candidate-specific functional evaluation for EXT-BATCH-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_batch_adapter import adapt_batch
from .hermes_batch_boundary import BatchSignal

@dataclass(frozen=True, slots=True)
class BatchFunctionalEvidence:
    baseline_collision_free_batch_task_rate: float
    adapted_collision_free_batch_task_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _signals(prefix: str) -> tuple[BatchSignal, ...]:
    return tuple(
        BatchSignal(
            f"{prefix}-{i}", "multiteiner",
            (f"controlled-eval:batch-functional/{prefix.lower()}/{i}",),
            "same-task", 5, True, True, "schema-v1", False, False,
        )
        for i in (1, 2)
    )

def _baseline(signals: tuple[BatchSignal, ...]) -> float:
    # Naive batch-task identity omits batch_id, so concurrent batches for the
    # same tenant/task collide.
    keys = tuple((s.tenant_scope, s.task_digest) for s in signals)
    return float(len(set(keys)) == len(keys))

def _adapted(signals: tuple[BatchSignal, ...]) -> float:
    contracts = tuple(adapt_batch(s) for s in signals)
    keys = tuple(
        (c.tenant_scope, c.task_digest, c.batch_id, c.result_schema_digest)
        for c in contracts if c is not None
    )
    return float(
        len(keys) == len(signals)
        and len(set(keys)) == len(keys)
        and all(not c.execution_permitted and not c.canonical_authority and not c.promotion_permitted
                for c in contracts if c is not None)
    )

def evaluate_batch_functional_gain() -> BatchFunctionalEvidence:
    baseline_signals = _signals("BASELINE")
    adapted_signals = _signals("HERMES")
    baseline = _baseline(baseline_signals)
    adapted = _adapted(adapted_signals)
    repeatable = _adapted(_signals("REPEAT")) == adapted
    contracts = tuple(adapt_batch(s) for s in adapted_signals)
    boundary = all(
        c is not None
        and not c.execution_permitted
        and not c.canonical_authority
        and not c.promotion_permitted
        for c in contracts
    )
    refs = tuple(ref for s in adapted_signals for ref in s.source_refs)
    return BatchFunctionalEvidence(baseline, adapted, repeatable, boundary, refs)
