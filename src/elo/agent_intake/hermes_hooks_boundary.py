"""Governed intake boundary for Hermes lifecycle hooks."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


CAPABILITY_ID = "EXT-HOOK-HERMES"


class HookDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class HookSignal:
    hook_id: str
    tenant_scope: str
    source_refs: Tuple[str, ...]
    event_name: str
    handler_digest: str
    explicit_activation: bool
    mutates_canonical_state: bool
    bypasses_governance: bool


@dataclass(frozen=True, slots=True)
class HookAssessment:
    hook_id: str
    disposition: HookDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    execution_permitted: bool = False
    mutation_permitted: bool = False


def assess_hook(signal: HookSignal) -> HookAssessment:
    if (
        not signal.hook_id
        or not signal.tenant_scope
        or not signal.event_name
        or not signal.handler_digest
    ):
        return HookAssessment(signal.hook_id, HookDisposition.REJECTED, signal.source_refs)

    if (
        not signal.source_refs
        or signal.mutates_canonical_state
        or signal.bypasses_governance
    ):
        return HookAssessment(signal.hook_id, HookDisposition.REJECTED, signal.source_refs)

    if not signal.explicit_activation:
        return HookAssessment(signal.hook_id, HookDisposition.OBSERVATION, signal.source_refs)

    return HookAssessment(signal.hook_id, HookDisposition.CANDIDATE, signal.source_refs)


__all__ = ["CAPABILITY_ID", "HookAssessment", "HookDisposition", "HookSignal", "assess_hook"]
