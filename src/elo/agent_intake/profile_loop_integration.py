"""Governed implementation-loop probe for EXT-PROFILE-HERMES.

The candidate enters the shared ELO governed mediator. This adapter does not
own an implementation state machine or approval authority.
"""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_profile_adapter import adapt_profile
from .hermes_profile_boundary import ProfileSignal
from .hermes_profile_evaluation import evaluate
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def run_profile_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-PROFILE-HERMES")
    evaluation = evaluate()
    signals = tuple(
        ProfileSignal(
            f"profile-loop-{i}", "multiteiner",
            (f"controlled-eval:profile-loop/{i}",), f"profile-digest-{i}",
            True, True, False, False
        ) for i in range(1, 6)
    )
    contracts = tuple(adapt_profile(signal) for signal in signals)
    refs = tuple(ref for contract in contracts if contract is not None for ref in contract.source_refs)
    boundary_integrity = all(
        contract is not None
        and not contract.shared_canonical_memory
        and not contract.authority_transfer
        and not contract.execution_permitted
        and not contract.promotion_permitted
        for contract in contracts
    )
    adaptation = refine_capability(
        "HERMES-CONTEXT",
        {"controlled_test": True, "outcome": {
            "profile_bounded": boundary_integrity,
            "canonical_memory_preserved": boundary_integrity,
            "authority_preserved": boundary_integrity,
        }},
    )
    measurement = CandidateMeasurement(
        candidate.candidate_id,
        {"bounded_profile_isolation_integrity_rate": evaluation.baseline_rate},
        {"bounded_profile_isolation_integrity_rate": evaluation.adapted_rate},
        (), evaluation.repeatable, evaluation.result,
    )
    evidence = measurement_to_implementation_evidence(
        candidate, measurement,
        metric_directions={"bounded_profile_isolation_integrity_rate": "maximize"},
        provenance_refs=refs, boundary_integrity=boundary_integrity,
    )
    handoff = advance_to_implementation(
        candidate, adaptation, evidence.baseline, evidence.adapted,
        metric_directions=evidence.metric_directions, repeatable=evidence.repeatable,
        regressions=evidence.regressions, provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
    )
    return handoff.implementation, evidence
