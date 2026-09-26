"""Candidate-specific functional evaluation for EXT-MEMPROVIDER-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_memory_provider_adapter import adapt_memory_provider
from .hermes_memory_provider_boundary import MemoryProviderSignal

@dataclass(frozen=True, slots=True)
class MemoryProviderFunctionalEvidence:
    baseline_identity_preservation_rate: float
    adapted_identity_preservation_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _signals(prefix: str) -> tuple[MemoryProviderSignal, ...]:
    return tuple(
        MemoryProviderSignal(
            f"provider-{i}", "multiteiner",
            (f"controlled-eval:memprovider-functional/{prefix.lower()}/{i}",),
            "retrieve", f"sha256:{prefix.lower()}-{i}",
            True, True, False, False,
        )
        for i in (1, 2)
    )

def _baseline(signals: tuple[MemoryProviderSignal, ...]) -> float:
    # Failure mode: a naive retrieval request identity keyed only by tenant +
    # operation conflates distinct provider/evidence contexts.
    identities = tuple((s.tenant_scope, s.operation) for s in signals)
    expected = tuple((s.provider_id, s.evidence_digest) for s in signals)
    return float(len(set(identities)) == len(expected))

def _adapted(signals: tuple[MemoryProviderSignal, ...]) -> float:
    contracts = tuple(adapt_memory_provider(s) for s in signals)
    identities = tuple(
        (c.provider_id, c.evidence_digest)
        for c in contracts if c is not None
    )
    expected = tuple((s.provider_id, s.evidence_digest) for s in signals)
    return float(
        len(identities) == len(signals)
        and len(set(identities)) == len(identities)
        and identities == expected
    )

def evaluate_memory_provider_functional_gain() -> MemoryProviderFunctionalEvidence:
    baseline_signals = _signals("BASELINE")
    adapted_signals = _signals("HERMES")
    baseline = _baseline(baseline_signals)
    adapted = _adapted(adapted_signals)
    repeatable = _adapted(_signals("REPEAT")) == adapted
    contracts = tuple(adapt_memory_provider(s) for s in adapted_signals)
    boundary = all(
        c is not None
        and not c.memory_authority
        and not c.mutation_permitted
        and not c.promotion_permitted
        for c in contracts
    )
    refs = tuple(ref for s in adapted_signals for ref in s.source_refs)
    return MemoryProviderFunctionalEvidence(
        baseline, adapted, repeatable, boundary, refs
    )
