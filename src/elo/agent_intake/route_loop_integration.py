"""Governed implementation-loop probe for EXT-ROUTE-HERMES."""
from __future__ import annotations
from .hermes_current_extensions import build_candidate
from .hermes_routing_boundary import RoutingSignal, assess_routing
from .hermes_routing_evaluation import evaluate
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .implementation_loop import run_implementation_loop
from .symbiont_adaptation import refine_capability
def run_route_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-ROUTE-HERMES")
    evaluation = evaluate()
    baseline = {"successful_policy_routed_execution_rate": evaluation.baseline_rate}
    adapted = {"successful_policy_routed_execution_rate": evaluation.adapted_rate}
    regressions = ()
    signal = RoutingSignal("route-loop","multiteiner",("controlled-eval:route-loop",),
                           "provider-a",("provider-b",),"bounded-pool-v1",True,True)
    boundary = assess_routing(signal)
    adaptation = refine_capability(
        "HERMES-TOOLSETS",
        {"controlled_test": True, "outcome": {"policy": True, "boundary": True}},
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        __import__("elo.agent_intake.hermes_current_extensions", fromlist=["CandidateMeasurement"]).CandidateMeasurement(
            candidate.candidate_id, baseline, adapted, regressions, evaluation.repeatable, evaluation.result
        ),
        metric_directions={"successful_policy_routed_execution_rate": "maximize"},
        provenance_refs=boundary.evidence_refs,
        boundary_integrity=(boundary.canonical_authority is False and
                            boundary.execution_permitted is False and
                            boundary.governance_bypass_permitted is False),
    )
    decision = run_implementation_loop(
        candidate, adaptation, evidence.baseline, evidence.adapted,
        repeatable=evidence.repeatable, regressions=evidence.regressions,
        metric_directions=evidence.metric_directions,
    )
    return decision, evidence
