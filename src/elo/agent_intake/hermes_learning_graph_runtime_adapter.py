"""Governed runtime bridge for EXT-LEARNING-GRAPH-HERMES.

The bridge reuses the existing learning-relation contract. It performs only
runtime validation and semantic duplicate detection; it does not persist,
promote, authorize, or mutate canonical learning state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .hermes_learning_boundary import LearningGraphRelation, validate_graph_relation
from .runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeOperationalEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)

CAPABILITY_ID = "EXT-LEARNING-GRAPH-HERMES"
OWNER = "ELO Evolution Memory"


@dataclass(frozen=True, slots=True)
class LearningGraphRuntimeResult:
    accepted: tuple[LearningGraphRelation, ...]
    blocked_duplicates: tuple[LearningGraphRelation, ...]
    evidence: RuntimeOperationalEvidence


def _semantic_key(relation: LearningGraphRelation) -> tuple[str, str, str]:
    return (relation.left_id, relation.right_id, relation.kind)


def evaluate_learning_graph_runtime(
    relations: Iterable[LearningGraphRelation],
    *,
    tenant_id: str,
    correlation_id: str,
    runtime_commit: str,
    runtime_trace: str,
    execution_id: str,
    repeatability: RepeatabilityEvidence,
) -> LearningGraphRuntimeResult:
    """Validate relation intake and emit observational runtime evidence.

    Tenant/correlation identity is required at the runtime boundary. Relation
    validation remains delegated to the existing learning-graph contract.
    """
    if not tenant_id.strip() or not correlation_id.strip():
        raise ValueError("tenant_id and correlation_id are required")

    seen: set[tuple[str, str, str]] = set()
    accepted: list[LearningGraphRelation] = []
    blocked: list[LearningGraphRelation] = []

    for relation in relations:
        validated = validate_graph_relation(relation)
        key = _semantic_key(validated)
        if key in seen:
            blocked.append(validated)
            continue
        seen.add(key)
        accepted.append(validated)

    # The observed metric is the actual duplicate-blocking result of this
    # runtime invocation. It is deliberately not treated as promotion.
    total = len(accepted) + len(blocked)
    observed = (len(blocked) / total) if total else 0.0
    evidence = create_runtime_evidence(
        execution_id=execution_id,
        candidate_id=CAPABILITY_ID,
        owner=OWNER,
        runtime_entrypoint="evaluate_learning_graph_runtime",
        action_observed=True,
        metric="duplicate_relation_block_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=observed,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit=runtime_commit,
            runtime_trace=f"{runtime_trace}:tenant={tenant_id}:correlation={correlation_id}",
        ),
        regression=False,
        repeatability=repeatability,
    )
    return LearningGraphRuntimeResult(tuple(accepted), tuple(blocked), evidence)


__all__ = ["LearningGraphRuntimeResult", "evaluate_learning_graph_runtime"]
