"""Evidence-first resolution for OKR strategic state.

Layer: cognitive
Owner: EvidenceRepository (authority) / strategic-objective-domain (consumer)
Status: implemented
Authority: implementation
Related: elo.evidence, elo.contracts.okr

No OKR-specific evidence store exists. This module resolves evidence identities
through the canonical tenant-scoped EvidenceRepository and reports missing
references explicitly.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.contracts.okr import KeyResult
from elo.evidence import Evidence, EvidenceRepository


@dataclass(frozen=True, slots=True)
class OkrEvidenceState:
    state: str
    evidence: tuple[Evidence, ...]
    missing_refs: tuple[str, ...]


class OkrEvidenceResolver:
    def __init__(self, repository: EvidenceRepository) -> None:
        self._repository = repository

    def resolve_refs(self, *, tenant_id: str, evidence_refs: tuple[str, ...]) -> OkrEvidenceState:
        observed: list[Evidence] = []
        missing: list[str] = []
        for ref in dict.fromkeys(evidence_refs):
            item = self._repository.get(ref, tenant_id=tenant_id)
            if item is None:
                missing.append(ref)
            else:
                observed.append(item)

        if not evidence_refs:
            state = "SEM_DADO"
        elif missing and observed:
            state = "PARCIAL"
        elif missing:
            state = "NAO_COMPROVADO"
        else:
            state = "COMPROVADO"
        return OkrEvidenceState(state=state, evidence=tuple(observed), missing_refs=tuple(missing))

    def key_result_baseline(self, key_result: KeyResult) -> OkrEvidenceState:
        return self.resolve_refs(
            tenant_id=key_result.tenant_id,
            evidence_refs=key_result.baseline_evidence_refs,
        )

    def key_result_target(self, key_result: KeyResult) -> OkrEvidenceState:
        return self.resolve_refs(
            tenant_id=key_result.tenant_id,
            evidence_refs=key_result.target_evidence_refs,
        )


__all__ = ["OkrEvidenceResolver", "OkrEvidenceState"]
