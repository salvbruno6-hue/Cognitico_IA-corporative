"""Governed implementation-loop probe for EXT-MEMPROVIDER-HERMES.

The candidate enters the shared ELO governed mediator. This adapter does not
own an implementation state machine, memory authority, or approval authority.
"""

from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_memory_provider_adapter import adapt_memory_provider
from .hermes_memory_provider_boundary import MemoryProviderSignal
from .hermes_memory_provider_evaluation import evaluate
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def run_memory_provider_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-MEMPROVIDER-HERMES")
    evaluation = evaluate()

    signals = tuple(
        MemoryProviderSignal(
            f"provider-loop-{i}",
            "multiteiner",
            (f"controlled-eval:memory-provider-loop/{i}",),
            "retrieve",
            f"sha256:memory-provider-loop-{i}",
            True,
            True,
            False,
            False,
        )
        for i in range(1, 6)
    )
    contracts = tuple(adapt_memory_provider(signal) for signal in signals)
    refs = tuple(
        ref for contract in contracts if contract is not None
        for ref in contract.source_refs
    )
    boundary_integrity = all(
        contract is not None
        and contract.memory_authority is False
        and contract.mutation_permitted is False
        and contract.promotion_permitted is False
        for contract in contracts
    )

    adaptation = refine_capability(
        "HERMES-MEMORY",
        {
            "controlled_test": True,
            "outcome": {
                "candidate_bounded": True,
                "memory_authority": not boundary_integrity,
                "mutation_permitted": not boundary_integrity,
                "promotion_permitted": not boundary_integrity,
            },
        },
    )
    measurement = CandidateMeasurement(
        candidate.candidate_id,
        {"bounded_memory_provider_request_integrity_rate": evaluation.baseline_rate},
        {"bounded_memory_provider_request_integrity_rate": evaluation.adapted_rate},
        (),
        evaluation.repeatable,
        evaluation.result,
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={"bounded_memory_provider_request_integrity_rate": "maximize"},
        provenance_refs=refs,
        boundary_integrity=boundary_integrity,
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
