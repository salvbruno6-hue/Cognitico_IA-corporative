"""Bounded isolated profile descriptor adapter."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_profile_boundary import ProfileDisposition, ProfileSignal, assess_profile

@dataclass(frozen=True, slots=True)
class ProfileContract:
    profile_id: str
    tenant_scope: str
    identity_digest: str
    source_refs: tuple[str, ...]
    disposition: ProfileDisposition
    shared_canonical_memory: bool = False
    authority_transfer: bool = False
    execution_permitted: bool = False
    promotion_permitted: bool = False

class ProfileAdapter:
    def adapt(self, signal: ProfileSignal) -> ProfileContract | None:
        assessment = assess_profile(signal)
        if assessment.disposition is not ProfileDisposition.CANDIDATE:
            return None
        return ProfileContract(
            signal.profile_id, signal.tenant_scope, signal.identity_digest,
            assessment.evidence_refs, assessment.disposition,
        )

def adapt_profile(signal: ProfileSignal) -> ProfileContract | None:
    return ProfileAdapter().adapt(signal)
