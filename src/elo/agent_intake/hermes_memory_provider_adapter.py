"""Bounded external-memory provider request adapter.

The adapter materializes a retrieval-only contract behind ELO Memory. It does
not activate providers, write memory, transfer memory authority, or promote
knowledge.
"""
from __future__ import annotations

from dataclasses import dataclass

from .hermes_memory_provider_boundary import (
    MemoryProviderDisposition,
    MemoryProviderSignal,
    assess_memory_provider,
)


@dataclass(frozen=True, slots=True)
class MemoryProviderRequestContract:
    provider_id: str
    tenant_scope: str
    operation: str
    evidence_digest: str
    source_refs: tuple[str, ...]
    disposition: MemoryProviderDisposition
    memory_authority: bool = False
    mutation_permitted: bool = False
    promotion_permitted: bool = False


class MemoryProviderAdapter:
    def adapt(self, signal: MemoryProviderSignal) -> MemoryProviderRequestContract | None:
        assessment = assess_memory_provider(signal)
        if assessment.disposition is not MemoryProviderDisposition.CANDIDATE:
            return None
        return MemoryProviderRequestContract(
            provider_id=signal.provider_id,
            tenant_scope=signal.tenant_scope,
            operation=signal.operation,
            evidence_digest=signal.evidence_digest,
            source_refs=assessment.evidence_refs,
            disposition=assessment.disposition,
        )


def adapt_memory_provider(signal: MemoryProviderSignal) -> MemoryProviderRequestContract | None:
    return MemoryProviderAdapter().adapt(signal)


__all__ = [
    "MemoryProviderAdapter",
    "MemoryProviderRequestContract",
    "adapt_memory_provider",
]
