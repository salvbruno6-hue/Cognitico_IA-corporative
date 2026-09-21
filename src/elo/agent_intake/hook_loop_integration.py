"""First governed implementation-loop probe for EXT-HOOK-HERMES."""
from __future__ import annotations

from .hermes_current_extensions import build_candidate
from .hermes_hook_boundary import HookSignal, assess_hook
from .hook_loop_harness import evaluate_hook_loop_harness, to_candidate_measurement
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .hermes_governed_loop import advance_to_implementation
from .symbiont_adaptation import refine_capability


def run_hook_loop_probe(
    tenant_scope: str = "loop-tenant",
    repeats: int = 5,
) -> tuple[object, object]:
    candidate = build_candidate("EXT-HOOK-HERMES")
    measurement = evaluate_hook_loop_harness(tenant_scope, repeats)
    candidate_measurement = to_candidate_measurement(measurement)
    boundary = assess_hook(HookSignal(
        "hook-loop-signal",
        tenant_scope,
        "controlled.guardrail",
        ("controlled-eval:hook-loop-harness",),
        True,
        True,
    ))
    adaptation = refine_capability(
        "HERMES-AUTOMATION",
        {"controlled_test": True, "outcome": {"boundary": True, "guardrail": True}},
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        candidate_measurement,
        metric_directions=measurement.metric_directions,
        provenance_refs=boundary.evidence_refs,
        boundary_integrity=(
            not boundary.canonical_authority
            and not boundary.execution_authority
            and not boundary.merge_permitted
        ),
    )
    handoff = advance_to_implementation(
        candidate,
        adaptation,
        evidence.baseline,
        evidence.adapted,
        repeatable=evidence.repeatable,
        regressions=evidence.regressions,
        metric_directions=evidence.metric_directions,
        provenance_refs=evidence.provenance_refs,
        boundary_integrity=evidence.boundary_integrity,
    )
    return handoff.implementation, evidence
