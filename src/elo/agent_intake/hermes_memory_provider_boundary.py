"""Candidate-only boundary for Hermes external memory providers."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

CAPABILITY_ID = "EXT-MEMPROVIDER-HERMES"

class MemoryProviderDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class MemoryProviderSignal:
    provider_id: str
    tenant_scope: str
    source_refs: Tuple[str, ...]
    operation: str
    evidence_digest: str
    provenance_verified: bool = False
    explicit_activation: bool = False
    canonical_write: bool = False
    promotion_attempt: bool = False

@dataclass(frozen=True)
class MemoryProviderAssessment:
    provider_id: str
    disposition: MemoryProviderDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    mutation_permitted: bool = False
    promotion_permitted: bool = False

def assess_memory_provider(signal: MemoryProviderSignal) -> MemoryProviderAssessment:
    if not signal.provider_id or not signal.tenant_scope or not signal.operation or not signal.evidence_digest:
        return MemoryProviderAssessment(signal.provider_id, MemoryProviderDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.source_refs or not signal.provenance_verified:
        return MemoryProviderAssessment(signal.provider_id, MemoryProviderDisposition.REJECTED, tuple(signal.source_refs))
    if signal.canonical_write or signal.promotion_attempt:
        return MemoryProviderAssessment(signal.provider_id, MemoryProviderDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.explicit_activation:
        return MemoryProviderAssessment(signal.provider_id, MemoryProviderDisposition.OBSERVATION, tuple(signal.source_refs))
    return MemoryProviderAssessment(signal.provider_id, MemoryProviderDisposition.CANDIDATE, tuple(signal.source_refs))
