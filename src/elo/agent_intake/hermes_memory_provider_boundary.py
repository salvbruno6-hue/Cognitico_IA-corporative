"""Candidate-only boundary for Hermes external memory providers."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple
CAPABILITY_ID="EXT-MEMPROVIDER-HERMES"
class MemoryProviderDisposition(str,Enum):
    OBSERVATION="OBSERVATION"; CANDIDATE="CANDIDATE"; REJECTED="REJECTED"
@dataclass(frozen=True)
class MemoryProviderSignal:
    provider_id:str; tenant_scope:str; source_refs:Tuple[str,...]; operation:str; evidence_digest:str
    provenance_verified:bool=False; explicit_activation:bool=False; canonical_write:bool=False; promotion_attempt:bool=False
@dataclass(frozen=True)
class MemoryProviderAssessment:
    provider_id:str; disposition:MemoryProviderDisposition; evidence_refs:Tuple[str,...]
    canonical_authority:bool=False; mutation_permitted:bool=False; promotion_permitted:bool=False
def assess_memory_provider(s:MemoryProviderSignal)->MemoryProviderAssessment:
    if not s.provider_id or not s.tenant_scope or not s.operation or not s.evidence_digest:
        return MemoryProviderAssessment(s.provider_id,MemoryProviderDisposition.REJECTED,tuple(s.source_refs))
    if not s.source_refs or not s.provenance_verified:
        return MemoryProviderAssessment(s.provider_id,MemoryProviderDisposition.REJECTED,tuple(s.source_refs))
    if s.canonical_write or s.promotion_attempt:
        return MemoryProviderAssessment(s.provider_id,MemoryProviderDisposition.REJECTED,tuple(s.source_refs))
    if not s.explicit_activation:
        return MemoryProviderAssessment(s.provider_id,MemoryProviderDisposition.OBSERVATION,tuple(s.source_refs))
    return MemoryProviderAssessment(s.provider_id,MemoryProviderDisposition.CANDIDATE,tuple(s.source_refs))
