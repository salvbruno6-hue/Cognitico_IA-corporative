"""Governed functional-value probe for EXT-CONTEXTREF-HERMES."""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_functional_value_proof import classify
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .hermes_context_reference_functional_evaluation import evaluate
from .symbiont_adaptation import refine_capability


def run_contextref_functional_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-CONTEXTREF-HERMES")
    functional = evaluate()
    adaptation = refine_capability(
        "HERMES-CONTEXT",
        {
            "controlled_test": True,
            "outcome": {
                "functional_gain": functional.adapted_unsafe_admission_rate < functional.baseline_unsafe_admission_rate,
                "boundary_integrity": functional.boundary_integrity_rate == 1.0,
            },
        },
    )
    measurement = CandidateMeasurement(
        candidate.candidate_id,
        {"unsafe_malformed_reference_admission_rate": functional.baseline_unsafe_admission_rate},
        {"unsafe_malformed_reference_admission_rate": functional.adapted_unsafe_admission_rate},
        (), functional.repeatable, "EVOLUTION_GATE_REQUIRED",
    )
    evidence = measurement_to_implementation_evidence(
        candidate, measurement,
        metric_directions={"unsafe_malformed_reference_admission_rate": "minimize"},
        provenance_refs=functional.provenance_refs,
        boundary_integrity=functional.boundary_integrity_rate == 1.0,
    )
    handoff = advance_to_implementation(
        candidate, adaptation, evidence.baseline, evidence.adapted,
        metric_directions=evidence.metric_directions,
        repeatable=evidence.repeatable,
        regressions=evidence.regressions,
        provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
        functional_value_evidence=classify(
            "EXT-CONTEXTREF-HERMES",
            baseline=functional.baseline_unsafe_admission_rate,
            adapted=functional.adapted_unsafe_admission_rate,
            metric="unsafe_malformed_reference_admission_rate",
            direction="minimize",
            repeatable=functional.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled malformed context-reference admission prevention before ELO Context resolution",
            provenance_refs=functional.provenance_refs,
        ),
    )
    return handoff.implementation, evidence
