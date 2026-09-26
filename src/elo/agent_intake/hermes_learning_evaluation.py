"""Controlled three-phase evaluation of EXT-LEARN-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_learning_adapter import adapt_skill_learning
from .hermes_learning_boundary import LearningState, SkillLearningSignal

CAPABILITY_ID="EXT-LEARN-HERMES"
PRIMARY_METRIC="bounded_skill_learning_candidate_integrity_rate"
METRIC_DIRECTION="maximize"

@dataclass(frozen=True, slots=True)
class SkillLearningEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str):
    return tuple(SkillLearningSignal(
        f"{prefix}-{i}","multiteiner",(f"hermes:learn:{prefix.lower()}/{i}",),
        f"skill-{i}",f"digest-{i}",True,True
    ) for i in range(1,6))

def _integrity(contracts):
    return sum(c is not None and c.state is LearningState.CANDIDATE
               and c.promotion_authority is False and c.canonical_mutation is False
               for c in contracts)/len(contracts)

def evaluate():
    baseline=0.0
    adapted_contracts=tuple(adapt_skill_learning(s) for s in _signals("HERMES"))
    repeat_contracts=tuple(adapt_skill_learning(s) for s in _signals("REPEAT"))
    adapted=sum(c is not None for c in adapted_contracts)/len(adapted_contracts)
    integrity=_integrity(adapted_contracts)
    repeatable=sum(c is not None for c in repeat_contracts)/len(repeat_contracts)==adapted and _integrity(repeat_contracts)==1.0
    result="EVOLUTION_GATE_REQUIRED" if adapted>baseline and repeatable and integrity==1.0 else "RETEST"
    return SkillLearningEvaluation(baseline,adapted,integrity,repeatable,result)
