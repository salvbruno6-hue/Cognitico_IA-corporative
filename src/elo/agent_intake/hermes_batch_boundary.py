"""Governed intake boundary for Hermes batch processing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


CAPABILITY_ID = "EXT-BATCH-HERMES"


class BatchDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class BatchSignal:
    batch_id: str
    tenant_scope: str
    source_refs: Tuple[str, ...]
    task_digest: str
    item_count: int
    bounded: bool
    explicit_authorization: bool
    result_schema_digest: str
    canonical_mutation: bool
    promotion_attempt: bool


@dataclass(frozen=True, slots=True)
class BatchAssessment:
    batch_id: str
    disposition: BatchDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    execution_permitted: bool = False
    promotion_permitted: bool = False


def assess_batch(signal: BatchSignal) -> BatchAssessment:
    if (
        not signal.batch_id
        or not signal.tenant_scope
        or not signal.task_digest
        or signal.item_count <= 0
        or not signal.result_schema_digest
    ):
        return BatchAssessment(
            signal.batch_id, BatchDisposition.REJECTED, signal.source_refs
        )

    if not signal.source_refs or signal.canonical_mutation or signal.promotion_attempt:
        return BatchAssessment(
            signal.batch_id, BatchDisposition.REJECTED, signal.source_refs
        )

    if not signal.bounded or not signal.explicit_authorization:
        return BatchAssessment(
            signal.batch_id, BatchDisposition.OBSERVATION, signal.source_refs
        )

    return BatchAssessment(signal.batch_id, BatchDisposition.CANDIDATE, signal.source_refs)


__all__ = ["CAPABILITY_ID", "BatchAssessment", "BatchDisposition", "BatchSignal", "assess_batch"]
