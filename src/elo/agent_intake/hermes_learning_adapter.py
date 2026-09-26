"""Bounded candidate-skill learning adapter."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_learning_boundary import LearningState, SkillLearningSignal, evaluate_skill_learning

@dataclass(frozen=True, slots=True)
class SkillLearningContract:
    signal_id: str
    tenant_scope: str
    skill_name: str
    instruction_digest: str
    source_refs: tuple[str, ...]
    state: LearningState
    promotion_authority: bool = False
    canonical_mutation: bool = False

class LearningAdapter:
    def adapt(self, signal: SkillLearningSignal) -> SkillLearningContract | None:
        decision=evaluate_skill_learning(signal)
        if not decision.admitted or decision.state is not LearningState.CANDIDATE:
            return None
        return SkillLearningContract(
            signal.signal_id, signal.tenant_scope, signal.skill_name,
            signal.instruction_digest, decision.evidence_refs, decision.state,
        )

def adapt_skill_learning(signal: SkillLearningSignal) -> SkillLearningContract | None:
    return LearningAdapter().adapt(signal)
