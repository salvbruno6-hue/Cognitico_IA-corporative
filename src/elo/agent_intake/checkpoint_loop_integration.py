"""Integration probe for the first governed implementation-loop candidate.

This module composes existing checkpoint evidence, the measurement harness,
Symbiont adaptation, and the implementation loop. It remains descriptive and
does not authorize or mutate canonical ELO state.
"""
from __future__ import annotations

from .checkpoint_loop_harness import evaluate_checkpoint_loop_harness
from .hermes_current_extensions import build_candidate
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .implementation_loop import run_implementation_loop
from .symbiont_adaptation import refine_capability


def run_checkpoint_loop_probe(*, tenant_scope: str = "loop-tenant", repeats: int = 5):
    candidate = build_candidate("EXT-CHECKPOINT-HERMES")
    measurement = evaluate_checkpoint_loop_harness(
        tenant_scope=tenant_scope,
        repeats=repeats,
    )
    candidate_measurement = measurement.to_candidate_measurement()

    adaptation = refine_capability(
        "HERMES-CHECKPOINT",
        {
            "controlled_test": True,
            "outcome": {"integrity": True, "continuity": True},
        },
    )

    evidence = measurement_to_implementation_evidence(
        candidate,
        candidate_measurement,
        metric_directions={"recovery_success": "maximize"},
        provenance_refs=("controlled-eval:checkpoint-loop-harness",),
        boundary_integrity=True,
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
    return evidence, decision


__all__ = ["run_checkpoint_loop_probe"]
