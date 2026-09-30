"""Controlled pre-compression checkpoint guard for ELO.

This is a contract-only adapter inspired by Hermes MemoryProvider checkpoint
semantics. It never snapshots files, compresses context, mutates memory, or
delegates authority. It only decides whether a lossy compaction boundary may
proceed from an already-issued checkpoint receipt.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CAPABILITY_ID = "EXT-CHECKPOINT-HERMES"

CheckpointState = Literal["CONFIRMED", "UNCONFIRMED"]
CompressionDecision = Literal["ALLOW", "BLOCK"]


@dataclass(frozen=True, slots=True)
class CheckpointReceipt:
    """Immutable evidence that a checkpoint was durably confirmed."""

    checkpoint_id: str
    provider_id: str
    tenant_scope: str
    state: CheckpointState
    durable: bool
    evidence_id: str

    def __post_init__(self) -> None:
        if any(not value.strip() for value in (
            self.checkpoint_id,
            self.provider_id,
            self.tenant_scope,
            self.evidence_id,
        )):
            raise ValueError("checkpoint identity, provider, scope and evidence are required")


@dataclass(frozen=True, slots=True)
class CompressionBoundaryRequest:
    """Policy input for a potentially lossy context-compaction boundary."""

    request_id: str
    tenant_scope: str
    checkpoint_required: bool = False


@dataclass(frozen=True, slots=True)
class CompressionBoundaryDecision:
    """Pure decision result; it does not perform compression or persistence."""

    request_id: str
    capability_id: str
    decision: CompressionDecision
    reason: str
    checkpoint_id: str | None
    evidence_id: str | None
    authority_transfer: bool = False


def evaluate_compression_boundary(
    request: CompressionBoundaryRequest,
    *,
    checkpoint: CheckpointReceipt | None,
) -> CompressionBoundaryDecision:
    """Fail closed when required durable checkpoint evidence is absent.

    A positive result means only that the boundary contract is satisfied.
    It is not authorization to compress, mutate memory, or promote knowledge.
    """

    if not request.request_id.strip() or not request.tenant_scope.strip():
        raise ValueError("request identity and tenant scope are required")

    if not request.checkpoint_required:
        return CompressionBoundaryDecision(
            request.request_id,
            CAPABILITY_ID,
            "ALLOW",
            "checkpoint is not required by policy",
            None,
            None,
        )

    if checkpoint is None:
        return CompressionBoundaryDecision(
            request.request_id,
            CAPABILITY_ID,
            "BLOCK",
            "required checkpoint receipt is absent",
            None,
            None,
        )

    if checkpoint.tenant_scope != request.tenant_scope:
        return CompressionBoundaryDecision(
            request.request_id,
            CAPABILITY_ID,
            "BLOCK",
            "checkpoint scope does not match compression scope",
            checkpoint.checkpoint_id,
            checkpoint.evidence_id,
        )

    if checkpoint.state != "CONFIRMED" or not checkpoint.durable:
        return CompressionBoundaryDecision(
            request.request_id,
            CAPABILITY_ID,
            "BLOCK",
            "required checkpoint is not durably confirmed",
            checkpoint.checkpoint_id,
            checkpoint.evidence_id,
        )

    return CompressionBoundaryDecision(
        request.request_id,
        CAPABILITY_ID,
        "ALLOW",
        "required durable checkpoint is confirmed for the requested scope",
        checkpoint.checkpoint_id,
        checkpoint.evidence_id,
    )
