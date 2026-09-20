"""Governed intake contract for Hermes-style skill learning signals."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

CAPABILITY_ID = "EXT-LEARN-HERMES"
LearningState = Literal["OBSERVED", "EVIDENCED", "CANDIDATE", "REJECTED"]

@dataclass(frozen=True, slots=True)
class SkillLearningSignal:
    signal_id: str
    tenant_scope: str
    source_refs: tuple[str, ...]
    skill_name: str
    instruction_digest: str
    user_directed: bool
    verified: bool
    state: LearningState = "OBSERVED"

@dataclass(frozen=True, slots=True)
class LearningAdmissionDecision:
    signal_id: str
    capability_id: str
    state: LearningState
    admitted: bool
    reason: str
    evidence_refs: tuple[str, ...]
    promotion_authority: bool = False

def evaluate_skill_learning(signal: SkillLearningSignal) -> LearningAdmissionDecision:
    if not signal.signal_id.strip() or not signal.tenant_scope.strip():
        raise ValueError("signal identity and tenant scope are required")
    if not signal.skill_name.strip() or not signal.instruction_digest.strip():
        raise ValueError("skill name and instruction digest are required")
    if not signal.source_refs:
        return LearningAdmissionDecision(signal.signal_id, CAPABILITY_ID, "REJECTED", False, "learning signal has no source provenance", ())
    if not signal.verified:
        return LearningAdmissionDecision(signal.signal_id, CAPABILITY_ID, "OBSERVED", False, "unverified skill learning remains an observation", signal.source_refs)
    return LearningAdmissionDecision(signal.signal_id, CAPABILITY_ID, "CANDIDATE", True, "verified skill-learning signal admitted as candidate-only evidence", signal.source_refs)
