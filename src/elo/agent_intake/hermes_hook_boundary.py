"""Governed boundary for the Hermes lifecycle-hook candidate."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
CAPABILITY_ID = "EXT-HOOK-HERMES"
class HookDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"
@dataclass(frozen=True, slots=True)
class HookSignal:
    signal_id: str
    tenant_scope: str
    lifecycle_event: str
    source_refs: tuple[str, ...]
    provenance_verified: bool
    guardrail_triggered: bool
    execution_authority: bool = False
    canonical_mutation: bool = False
    authorization_bypass: bool = False
@dataclass(frozen=True, slots=True)
class HookAssessment:
    disposition: HookDisposition
    evidence_refs: tuple[str, ...]
    canonical_authority: bool = False
    execution_authority: bool = False
    merge_permitted: bool = False
def assess_hook(signal: HookSignal) -> HookAssessment:
    if not signal.signal_id or not signal.tenant_scope or not signal.lifecycle_event:
        return HookAssessment(HookDisposition.REJECTED, ())
    if not signal.source_refs or not signal.provenance_verified:
        return HookAssessment(HookDisposition.REJECTED, signal.source_refs)
    if signal.execution_authority or signal.canonical_mutation or signal.authorization_bypass:
        return HookAssessment(HookDisposition.REJECTED, signal.source_refs)
    refs = signal.source_refs + (signal.signal_id,)
    if signal.guardrail_triggered:
        return HookAssessment(HookDisposition.CANDIDATE, refs)
    return HookAssessment(HookDisposition.OBSERVATION, refs)
