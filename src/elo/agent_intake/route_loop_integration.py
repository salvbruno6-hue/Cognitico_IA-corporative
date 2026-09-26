"""Governed implementation-loop probe for EXT-ROUTE-HERMES.

The candidate enters the shared ELO governed mediator. This adapter does not
own an implementation state machine or approval authority.
"""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_routing_adapter import adapt_routing
from .hermes_routing_boundary import RoutingSignal
from .hermes_routing_evaluation import evaluate
from .hermes_route_functional_evaluation import evaluate_route_functional_gain
from .hermes_functional_value_proof import classify
from .hermes_governed_loop import advance_to_implementation
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def run_route_loop_probe() -> tuple[object, object]:
    candidate = build_candidate("EXT-ROUTE-HERMES")
    evaluation = evaluate()
    functional = evaluate_route_functional_gain()
    signals = tuple(
        RoutingSignal(
            f"route-loop-{i}",
            "multiteiner",
            (f"controlled-eval:route-loop/{i}",),
            "provider-a",
            ("provider-b",),
            "bounded-pool-v1",
            True,
            True,
            False,
            False,
        )
        for i in range(1, 6)
    )
    contracts = tuple(adapt_routing(signal) for signal in signals)
    refs = tuple(
        ref for contract in contracts if contract is not None
        for ref in contract.source_refs
    )
    boundary_integrity = all(
        contract is not None
        and not contract.canonical_authority
        and not contract.execution_permitted
        and not contract.governance_bypass_permitted
        for contract in contracts
    )

    adaptation = refine_capability(
        "HERMES-TOOLSETS",
        {
            "controlled_test": True,
            "outcome": {
                "policy_contract_bounded": boundary_integrity,
                "execution_blocked": boundary_integrity,
                "authority_preserved": boundary_integrity,
            },
        },
    )
    measurement = CandidateMeasurement(
        candidate.candidate_id,
        {"unsafe_route_admission_block_rate": functional.baseline_unsafe_route_admission_block_rate},
        {"unsafe_route_admission_block_rate": functional.adapted_unsafe_route_admission_block_rate},
        (),
        evaluation.repeatable,
        evaluation.result,
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={"unsafe_route_admission_block_rate": "maximize"},
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
