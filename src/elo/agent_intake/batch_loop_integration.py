"""Governed implementation-loop probe for EXT-BATCH-HERMES.

The candidate enters the shared ELO governed mediator. This adapter does not
own an implementation state machine or approval authority.
"""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_batch_adapter import adapt_batch
from .hermes_batch_boundary import BatchSignal
from .hermes_batch_evaluation import evaluate
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def run_batch_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-BATCH-HERMES")
    evaluation = evaluate()
    signals = tuple(
        BatchSignal(
            f"batch-loop-{i}", "multiteiner",
            (f"controlled-eval:batch-loop/{i}",),
            f"task-{i}", 5, True, True, "schema-v1", False, False
        ) for i in range(1, 6)
    )
    contracts = tuple(adapt_batch(signal) for signal in signals)
    refs = tuple(ref for contract in contracts if contract is not None for ref in contract.source_refs)
    boundary_integrity = all(
        contract is not None
        and not contract.execution_permitted
        and not contract.canonical_authority
        and not contract.promotion_permitted
        for contract in contracts
    )
    adaptation = refine_capability(
        "HERMES-DELEGATION",
        {"controlled_test": True, "outcome": {
            "batch_bounded": boundary_integrity,
            "execution_blocked": boundary_integrity,
            "promotion_blocked": boundary_integrity,
        }},
    )
    measurement = CandidateMeasurement(
        candidate.candidate_id,
        {"bounded_batch_intake_integrity_rate": evaluation.baseline_rate},
        {"bounded_batch_intake_integrity_rate": evaluation.adapted_rate},
        (), evaluation.repeatable, evaluation.result,
    )
    evidence = measurement_to_implementation_evidence(
        candidate, measurement,
        metric_directions={"bounded_batch_intake_integrity_rate": "maximize"},
        provenance_refs=refs, boundary_integrity=boundary_integrity,
    )
    handoff = advance_to_implementation(
        candidate, adaptation, evidence.baseline, evidence.adapted,
        metric_directions=evidence.metric_directions, repeatable=evidence.repeatable,
        regressions=evidence.regressions, provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
    )
    return handoff.implementation, evidence

