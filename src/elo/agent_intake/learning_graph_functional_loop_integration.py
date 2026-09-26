"""Governed functional-value probe for EXT-LEARNING-GRAPH-HERMES."""
from __future__ import annotations
from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_functional_value_proof import classify
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .hermes_learning_graph_functional_evaluation import evaluate_learning_graph_functional_gain
from .symbiont_adaptation import refine_capability

def run_learning_graph_functional_loop_probe() -> tuple[object, object]:
    candidate=build_candidate("EXT-LEARNING-GRAPH-HERMES")
    functional=evaluate_learning_graph_functional_gain()
    adaptation=refine_capability(
        "HERMES-MEMORY",
        {"controlled_test": True, "outcome": {
            "duplicate_relation_blocked": functional.adapted_duplicate_relation_block_rate == 1.0,
            "canonical_authority_blocked": functional.boundary_integrity,
        }},
    )
    measurement=CandidateMeasurement(
        candidate.candidate_id,
        {"duplicate_relation_block_rate": functional.baseline_duplicate_relation_block_rate},
        {"duplicate_relation_block_rate": functional.adapted_duplicate_relation_block_rate},
        (), functional.repeatable, "EVOLUTION_GATE_REQUIRED",
    )
    evidence=measurement_to_implementation_evidence(
        candidate, measurement,
        metric_directions={"duplicate_relation_block_rate":"maximize"},
        provenance_refs=functional.provenance_refs,
        boundary_integrity=functional.boundary_integrity,
    )
    handoff=advance_to_implementation(
        candidate, adaptation, evidence.baseline, evidence.adapted,
        metric_directions=evidence.metric_directions,
        repeatable=evidence.repeatable,
        regressions=evidence.regressions,
        provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
        functional_value_evidence=classify(
            "EXT-LEARNING-GRAPH-HERMES",
            baseline=functional.baseline_duplicate_relation_block_rate,
            adapted=functional.adapted_duplicate_relation_block_rate,
            metric="duplicate_relation_block_rate",
            direction="maximize",
            repeatable=functional.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled duplicate semantic learning-relation prevention",
            provenance_refs=functional.provenance_refs,
        ),
    )
    return handoff.implementation, evidence
