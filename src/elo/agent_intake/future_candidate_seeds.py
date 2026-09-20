"""Prepare existing external capability records as future ELO candidates.

This adapter does not create a registry, approve a candidate, execute a runtime,
or mutate canonical ELO state. It converts an already bounded candidate-only
Hermes record into the existing ELOCapabilityCandidate contract so that a future
controlled evaluation can start from a complete provenance package.
"""

from __future__ import annotations

from elo.cognitive.symbiont_capability_absorption import (
    CapabilityState,
    ELOCapabilityCandidate,
)
from .hermes_current_extensions import HermesCandidate


def prepare_future_candidate(
    candidate: HermesCandidate,
    *,
    tenant_id: str,
    source_ref: str,
    source_commit: str,
    evidence_ids: tuple[str, ...],
    validation_contract: str,
) -> ELOCapabilityCandidate:
    """Materialize an in-memory ELO candidate from a bounded external candidate.

    The returned object is candidate-only. No repository, database, Evolution
    Gate, approval, deployment, or canonical mutation is performed.
    """
    required = (
        candidate.candidate_id,
        candidate.mechanism,
        candidate.owner,
        candidate.adaptation,
        tenant_id,
        source_ref,
        source_commit,
        validation_contract,
    )
    if not all(required):
        raise ValueError("future candidate requires identity, owner, contract and provenance")
    if not evidence_ids:
        raise ValueError("future candidate requires evidence references")
    if candidate.promotion_state != "candidate_only":
        raise ValueError("only candidate-only external records may be prepared")
    if candidate.canonical_mutation:
        raise ValueError("candidate with canonical mutation cannot be prepared")

    return ELOCapabilityCandidate(
        capability_id=candidate.candidate_id,
        tenant_id=tenant_id,
        domain=candidate.owner,
        title=candidate.mechanism,
        portable_principle=candidate.adaptation,
        interface_contract=f"candidate-only:{candidate.owner}",
        validation_contract=validation_contract,
        source_ref=source_ref,
        source_commit=source_commit,
        evidence_ids=evidence_ids,
        provenance={
            "origin": "hermes-future-candidate-adapter",
            "provider": "Hermes",
            "source_ref": source_ref,
            "source_commit": source_commit,
            "owner": candidate.owner,
        },
        state=CapabilityState.CANDIDATE,
    )


__all__ = ["prepare_future_candidate"]
