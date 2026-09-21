"""Governed implementation-loop probe for EXT-PROFILE-HERMES.

The candidate enters the shared ELO governed mediator. This adapter does not
own an implementation state machine or approval authority.
"""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_profile_boundary import ProfileSignal, assess_profile
from .hermes_profile_evaluation import evaluate
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def run_profile_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-PROFILE-HERMES")
    evaluation = evaluate()
    baseline = {"isolated_profile_candidate_rate": evaluation.baseline_rate}
    adapted = {"isolated_profile_candidate_rate": evaluation.adapted_rate}

    signal = ProfileSignal(
        "profile-loop",
        "multiteiner",
        ("controlled-eval:profile-loop",),
        "profile-digest-v1",
        True,
        True,
        False,
        False,
    )
    boundary = assess_profile(signal)

    adaptation = refine_capability(
        "HERMES-CONTEXT",
        {"controlled_test": True, "outcome": {"isolated_state": True, "boundary": True}},
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
        metric_directions={"isolated_profile_candidate_rate": "maximize"},
        provenance_refs=boundary.evidence_refs,
        boundary_integrity=(
            not boundary.canonical_authority
            and not boundary.execution_permitted
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
