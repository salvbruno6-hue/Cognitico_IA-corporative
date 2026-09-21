"""Controlled implementation-loop probe for EXT-ROUTE-HERMES."""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_routing_boundary import RoutingDisposition, RoutingSignal, assess_routing
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .implementation_loop import run_implementation_loop
from .symbiont_adaptation import refine_capability


def run_route_loop_probe(tenant_scope: str = "loop-tenant", repeats: int = 5):
    if repeats < 1:
        raise ValueError("repeats must be >= 1")

    candidate = build_candidate("EXT-ROUTE-HERMES")
    baseline = {"successful_policy_routed_execution_rate": 0.0}
    adapted_values = []

    for _ in range(repeats):
        signal = RoutingSignal(
            "route-loop",
            tenant_scope,
            ("controlled-eval:route-loop",),
            "provider-a",
            ("provider-b",),
            "bounded-pool-v1",
            provenance_verified=True,
            explicit_policy=True,
        )
        assessment = assess_routing(signal)
        adapted_values.append(
            1.0 if assessment.disposition is RoutingDisposition.CANDIDATE else 0.0
        )

    adapted = {"successful_policy_routed_execution_rate": adapted_values[0]}
    measurement = CandidateMeasurement(
        candidate_id=candidate.candidate_id,
        baseline=baseline,
        adapted=adapted,
        regressions=(),
        repeatable=len(set(adapted_values)) == 1,
        result="EVOLUTION_GATE_REQUIRED",
    )
    adaptation = refine_capability(
        "HERMES-TOOLSETS",
        {"controlled_test": True, "outcome": {"boundary": True}},
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={"successful_policy_routed_execution_rate": "maximize"},
        provenance_refs=("controlled-eval:route-loop",),
        boundary_integrity=(
            not assess_routing(signal).canonical_authority
            and not assess_routing(signal).execution_permitted
            and not assess_routing(signal).governance_bypass_permitted
        ),
    )
    decision = run_implementation_loop(
        candidate,
        adaptation,
        evidence.baseline,
        evidence.adapted,
        repeatable=evidence.repeatable,
        regressions=evidence.regressions,
        metric_directions=evidence.metric_directions,
    )
    return decision, evidence


__all__ = ["run_route_loop_probe"]
