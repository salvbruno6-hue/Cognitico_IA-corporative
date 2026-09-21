"""Controlled implementation-loop probe for EXT-PROFILE-HERMES."""
from __future__ import annotations

from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_profile_boundary import ProfileDisposition, ProfileSignal, assess_profile
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .implementation_loop import run_implementation_loop
from .symbiont_adaptation import refine_capability


def run_profile_loop_probe(tenant_scope: str = "loop-tenant", repeats: int = 5):
    if repeats < 1:
        raise ValueError("repeats must be >= 1")

    candidate = build_candidate("EXT-PROFILE-HERMES")
    baseline = {"profile_isolation_compliance": 0.0}
    adapted_values = []

    for _ in range(repeats):
        signal = ProfileSignal(
            "profile-loop",
            tenant_scope,
            ("controlled-eval:profile-loop",),
            "profile-digest-v1",
            True,
            True,
            False,
            False,
        )
        assessment = assess_profile(signal)
        adapted_values.append(
            1.0 if assessment.disposition is ProfileDisposition.CANDIDATE else 0.0
        )

    adapted = {"profile_isolation_compliance": adapted_values[0]}
    measurement = CandidateMeasurement(
        candidate_id=candidate.candidate_id,
        baseline=baseline,
        adapted=adapted,
        regressions=(),
        repeatable=len(set(adapted_values)) == 1,
        result="EVOLUTION_GATE_REQUIRED",
    )
    adaptation = refine_capability(
        "HERMES-DELEGATION",
        {"controlled_test": True, "outcome": {"boundary": True}},
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={"profile_isolation_compliance": "maximize"},
        provenance_refs=("controlled-eval:profile-loop",),
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
    return decision, evidence


__all__ = ["run_profile_loop_probe"]
