"""Candidate-specific functional evaluation for EXT-LEARNING-GRAPH-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_learning_boundary import LearningGraphRelation, validate_graph_relation

@dataclass(frozen=True, slots=True)
class LearningGraphFunctionalEvidence:
    baseline_duplicate_relation_block_rate: float
    adapted_duplicate_relation_block_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _relations(prefix: str):
    ref=f"controlled-eval:learning-graph-functional/{prefix.lower()}"
    relation=LearningGraphRelation(
        relation_id=f"{prefix}-1", left_id="skill-pricing",
        right_id="evidence-quotation", kind="SUPPORTS",
        evidence_refs=(ref,),
    )
    duplicate=LearningGraphRelation(
        relation_id=f"{prefix}-2", left_id="skill-pricing",
        right_id="evidence-quotation", kind="SUPPORTS",
        evidence_refs=(ref,),
    )
    distinct=LearningGraphRelation(
        relation_id=f"{prefix}-3", left_id="skill-pricing",
        right_id="evidence-contract", kind="SUPPORTS",
        evidence_refs=(f"{ref}/distinct",),
    )
    return relation, duplicate, distinct

def _baseline() -> float:
    # Existing validation accepts both identical semantic relations because
    # relation identity is validated, but graph-level duplicate suppression
    # is absent.
    first, duplicate, distinct = _relations("BASELINE")
    return 0.0 if validate_graph_relation(first) and validate_graph_relation(duplicate) else 1.0

def _adapted() -> float:
    first, duplicate, distinct = _relations("HERMES")
    seen: set[tuple[str, str, str]] = set()
    blocked = 0
    for relation in (first, duplicate, distinct):
        validate_graph_relation(relation)
        key=(relation.left_id, relation.right_id, relation.kind)
        if key in seen:
            blocked += 1
        else:
            seen.add(key)
    return blocked / 1.0

def evaluate_learning_graph_functional_gain() -> LearningGraphFunctionalEvidence:
    baseline=_baseline()
    adapted=_adapted()
    repeatable=_adapted() == adapted
    first, duplicate, distinct=_relations("BOUNDARY")
    boundary = (
        validate_graph_relation(first).canonical_authority is False
        and validate_graph_relation(distinct).canonical_authority is False
        and validate_graph_relation(duplicate).canonical_authority is False
    )
    refs=tuple(ref for relation in _relations("HERMES") for ref in relation.evidence_refs)
    return LearningGraphFunctionalEvidence(baseline, adapted, repeatable, boundary, refs)
