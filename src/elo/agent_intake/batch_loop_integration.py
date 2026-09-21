"""Governed implementation-loop probe for EXT-BATCH-HERMES."""
from __future__ import annotations
from .hermes_current_extensions import build_candidate, CandidateMeasurement
from .hermes_batch_boundary import BatchSignal, assess_batch
from .hermes_batch_evaluation import evaluate
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .implementation_loop import run_implementation_loop
from .symbiont_adaptation import refine_capability

def run_batch_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-BATCH-HERMES")
    evaluation = evaluate()
    baseline = {"bounded_batch_candidate_rate": evaluation.baseline_rate}
    adapted = {"bounded_batch_candidate_rate": evaluation.adapted_rate}
    signal = BatchSignal(
        "batch-loop", "multiteiner", ("controlled-eval:batch-loop",),
        "task-digest-v1", 5, True, True, "schema-v1", False, False,
    )
    boundary = assess_batch(signal)
    adaptation = refine_capability(
        "HERMES-DELEGATION",
        {"controlled_test": True, "outcome": {"bounded": True, "boundary": True}},
    )
    measurement = CandidateMeasurement(
        candidate.candidate_id, baseline, adapted, (), evaluation.repeatable, evaluation.result
    )
    evidence = measurement_to_implementation_evidence(
        candidate, measurement,
        metric_directions={"bounded_batch_candidate_rate": "maximize"},
        provenance_refs=boundary.evidence_refs,
        boundary_integrity=(
            not boundary.canonical_authority
            and not boundary.execution_permitted
            and not boundary.promotion_permitted
        ),
    )
    decision = run_implementation_loop(
        candidate, adaptation, evidence.baseline, evidence.adapted,
        repeatable=evidence.repeatable, regressions=evidence.regressions,
        metric_directions=evidence.metric_directions,
    )
    return decision, evidence
