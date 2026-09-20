"""Controlled evaluation of Hermes learning-graph relation intake."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_learning_boundary import LearningGraphRelation, validate_graph_relation

@dataclass(frozen=True)
class LearningGraphEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _relations(prefix: str):
    return tuple(LearningGraphRelation(
        relation_id=f"{prefix}-{i}", left_id=f"skill-{i}",
        right_id=f"evidence-{i}", kind="SUPPORTS",
        evidence_refs=(f"evidence:{prefix.lower()}/{i}",)
    ) for i in range(1, 6))

def _rate(relations) -> float:
    accepted = 0
    for relation in relations:
        try:
            accepted += validate_graph_relation(relation).canonical_authority is False
        except ValueError:
            pass
    return accepted / len(relations)

def _integrity(relations) -> float:
    return sum(validate_graph_relation(r).canonical_authority is False for r in relations) / len(relations)

def evaluate() -> LearningGraphEvaluation:
    baseline = _relations("BASE")
    adapted = _relations("HERMES")
    baseline_rate = _rate(baseline)
    adapted_rate = _rate(adapted)
    integrity = _integrity(adapted)
    repeatable = _rate(_relations("REPEAT")) == adapted_rate and integrity == 1.0
    result = "EVOLUTION_GATE_REQUIRED" if adapted_rate > baseline_rate and repeatable else "RETEST"
    return LearningGraphEvaluation(baseline_rate, adapted_rate, integrity, repeatable, result)
