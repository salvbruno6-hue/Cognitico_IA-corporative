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

def _relations(prefix):
    return tuple(LearningGraphRelation(
        relation_id=f"{prefix}-{i}", left_id=f"skill-{i}",
        right_id=f"evidence-{i}", kind="SUPPORTS",
        evidence_refs=(f"evidence:{prefix.lower()}/{i}",)
    ) for i in range(1,6))

def _rate(relations):
    accepted=0
    for r in relations:
        try:
            accepted += validate_graph_relation(r).canonical_authority is False
        except ValueError:
            pass
    return accepted/len(relations)

def _integrity(relations):
    return sum(validate_graph_relation(r).canonical_authority is False for r in relations)/len(relations)

def evaluate():
    baseline=_relations("BASE"); adapted=_relations("HERMES")
    b=_rate(baseline); a=_rate(adapted); i=_integrity(adapted)
    repeatable=_rate(_relations("REPEAT"))==a and i==1.0
    result="EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST"
    return LearningGraphEvaluation(b,a,i,repeatable,result)
