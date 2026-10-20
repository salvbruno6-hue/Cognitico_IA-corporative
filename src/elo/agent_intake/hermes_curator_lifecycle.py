"""Governed intake boundary for Hermes Curator lifecycle signals.

Hermes Curator may report deterministic skill-maintenance signals, but ELO
treats them as evidence only. No transition here mutates canonical knowledge.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

CAPABILITY_ID = "EXT-CURATOR-HERMES"

class LifecycleState(str, Enum):
    ACTIVE = "active"
    STALE = "stale"
    ARCHIVED = "archived"

class IntakeDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    RETIREMENT_CANDIDATE = "RETIREMENT_CANDIDATE"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class CuratorSignal:
    signal_id: str
    tenant_scope: str
    skill_id: str
    observed_state: LifecycleState
    source_refs: Tuple[str, ...]
    last_activity_at: str | None = None
    use_count: int = 0
    pinned: bool = False
    curator_managed: bool = False
    user_directed: bool = False

@dataclass(frozen=True)
class LifecycleAssessment:
    signal_id: str
    skill_id: str
    disposition: IntakeDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    mutation_permitted: bool = False

def assess_curator_signal(signal: CuratorSignal) -> LifecycleAssessment:
    """Convert Hermes maintenance telemetry into a non-authoritative ELO signal."""
    if not signal.signal_id or not signal.tenant_scope or not signal.skill_id:
        return LifecycleAssessment(signal.signal_id, signal.skill_id, IntakeDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.source_refs:
        return LifecycleAssessment(signal.signal_id, signal.skill_id, IntakeDisposition.REJECTED, ())
    if signal.pinned or not signal.curator_managed or signal.user_directed:
        return LifecycleAssessment(signal.signal_id, signal.skill_id, IntakeDisposition.OBSERVATION, tuple(signal.source_refs))
    if signal.observed_state is LifecycleState.STALE:
        return LifecycleAssessment(signal.signal_id, signal.skill_id, IntakeDisposition.REVIEW_REQUIRED, tuple(signal.source_refs))
    if signal.observed_state is LifecycleState.ARCHIVED:
        return LifecycleAssessment(signal.signal_id, signal.skill_id, IntakeDisposition.RETIREMENT_CANDIDATE, tuple(signal.source_refs))
    return LifecycleAssessment(signal.signal_id, signal.skill_id, IntakeDisposition.OBSERVATION, tuple(signal.source_refs))