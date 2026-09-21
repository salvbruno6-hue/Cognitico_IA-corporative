"""Governed implementation-loop probe for EXT-ROUTE-HERMES.

The candidate enters the shared ELO governed mediator. This adapter does not
own an implementation state machine or approval authority.
"""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_routing_boundary import RoutingSignal, assess_routing
from .hermes_routing_evaluation import evaluate
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def run_route_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-ROUTE-HERMES")
    evaluation = evaluate()
    baseline = {"successful_policy_routed_execution_rate": evaluation.baseline_rate}
    adapted = {"successful_policy_routed_execution_rate": evaluation.adapted_rate}

    signal = RoutingSignal(
        "route-loop",
        "multiteiner",
        ("controlled-eval:route-loop",),
        "provider-a",
        ("provider-b",),
        "bounded-pool-v1",
        True,
        True,
    )
    boundary = assess_routing(signal)

    adaptation = refine_capability(
        "HERMES-TOOLSETS",
        {"controlled_test": True, "outcome": {"policy": True, "boundary": True}},
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
        metric_directions={
            "successful_policy_routed_execution_rate": "maximize"
        },
        provenance_refs=boundary.evidence_refs,
        boundary_integrity=(
            boundary.canonical_authority is False
            and boundary.execution_permitted is False
            and boundary.governance_bypass_permitted is False
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
