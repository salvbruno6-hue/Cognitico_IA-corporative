"""Governed implementation-loop probe for EXT-MEMPROVIDER-HERMES.

The candidate enters the shared ELO governed mediator. This adapter does not
own an implementation state machine, memory authority, or approval authority.
"""

from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_memory_provider_boundary import (
    MemoryProviderSignal,
    assess_memory_provider,
)
from .hermes_memory_provider_evaluation import evaluate
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def run_memory_provider_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-MEMPROVIDER-HERMES")
    evaluation = evaluate()
    baseline = {"external_memory_candidate_rate": evaluation.baseline_rate}
    adapted = {"external_memory_candidate_rate": evaluation.adapted_rate}

    signal = MemoryProviderSignal(
        "provider-loop",
        "multiteiner",
        ("controlled-eval:memory-provider-loop",),
        "retrieve",
        "sha256:memory-provider-loop",
        True,
        True,
        False,
        False,
    )
    boundary = assess_memory_provider(signal)

    adaptation = refine_capability(
        "HERMES-MEMORY",
        {
            "controlled_test": True,
            "outcome": {
                "candidate_bounded": True,
                "canonical_authority": boundary.canonical_authority,
                "mutation_permitted": boundary.mutation_permitted,
                "promotion_permitted": boundary.promotion_permitted,
            },
        },
    )

    measurement = CandidateMeasurement(
        candidate.candidate_id,
        baseline,
        adapted,
        (),
        evaluation.repeatable,
        evaluation.result,
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={"external_memory_candidate_rate": "maximize"},
        provenance_refs=boundary.evidence_refs,
        boundary_integrity=(
            not boundary.canonical_authority
            and not boundary.mutation_permitted
            and not boundary.promotion_permitted
        ),
    )

    handoff = advance_to_implementation(
        candidate,
        adaptation,
        evidence.baseline,
        evidence.adapted,
        metric_directions=evidence.metric_directions,
        repeatable=evidence.repeatable,
        regressions=evidence.regressions,
        provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
    )
    return handoff.implementation, evidence


__all__ = ["run_memory_provider_loop_probe"]
