"""Candidate-only governance boundary for Hermes Git worktree isolation."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

CAPABILITY_ID = "EXT-WORKTREE-HERMES"

class WorktreeDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class WorktreeSignal:
    signal_id: str
    tenant_scope: str
    worktree_id: str
    source_refs: Tuple[str, ...]
    base_ref: str
    isolated: bool
    dirty_state: bool = False
    branch_ref: str | None = None
    provenance_verified: bool = False

@dataclass(frozen=True)
class WorktreeAssessment:
    signal_id: str
    worktree_id: str
    disposition: WorktreeDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    merge_permitted: bool = False

def assess_worktree(signal: WorktreeSignal) -> WorktreeAssessment:
    if not signal.signal_id or not signal.tenant_scope or not signal.worktree_id or not signal.base_ref:
        return WorktreeAssessment(signal.signal_id, signal.worktree_id, WorktreeDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.source_refs or not signal.provenance_verified or not signal.isolated:
        return WorktreeAssessment(signal.signal_id, signal.worktree_id, WorktreeDisposition.REJECTED, tuple(signal.source_refs))
    if signal.dirty_state:
        return WorktreeAssessment(signal.signal_id, signal.worktree_id, WorktreeDisposition.OBSERVATION, tuple(signal.source_refs))
    return WorktreeAssessment(signal.signal_id, signal.worktree_id, WorktreeDisposition.CANDIDATE, tuple(signal.source_refs))
