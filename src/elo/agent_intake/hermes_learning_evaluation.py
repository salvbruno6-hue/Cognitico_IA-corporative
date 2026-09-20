"""Controlled evaluation of Hermes-style skill learning intake."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_learning_boundary import SkillLearningSignal, evaluate_skill_learning

@dataclass(frozen=True)
class SkillLearningEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str):
    return tuple(SkillLearningSignal(
        signal_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        source_refs=(f"hermes:learn:{prefix.lower()}/{i}",),
        skill_name=f"skill-{i}", instruction_digest=f"digest-{i}",
        user_directed=True, verified=True
    ) for i in range(1, 6))

def _rate(signals) -> float:
    return sum(evaluate_skill_learning(s).admitted for s in signals) / len(signals)

def _integrity(signals) -> float:
    return sum(evaluate_skill_learning(s).promotion_authority is False for s in signals) / len(signals)

def evaluate() -> SkillLearningEvaluation:
    baseline = _signals("BASE")
    adapted = _signals("HERMES")
    baseline_rate = _rate(baseline)
    adapted_rate = _rate(adapted)
    integrity = _integrity(adapted)
    repeatable = _rate(_signals("REPEAT")) == adapted_rate and integrity == 1.0
    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"
    return SkillLearningEvaluation(baseline_rate, adapted_rate, integrity, repeatable, result)
