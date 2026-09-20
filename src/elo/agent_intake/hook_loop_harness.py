"""Deterministic controlled measurement harness for EXT-HOOK-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_current_extensions import CandidateMeasurement
from .hermes_hook_boundary import HookSignal, assess_hook
@dataclass(frozen=True, slots=True)
class HookLoopMeasurement:
    candidate_id: str
    baseline: dict[str, float]
    adapted: dict[str, float]
    regressions: tuple[str, ...]
    repeatable: bool
    metric_directions: dict[str, str]
def _baseline_probe(tenant_scope: str) -> float:
    _ = tenant_scope
    return 0.0
def _adapted_probe(tenant_scope: str) -> float:
    signal = HookSignal("hook-loop-signal", tenant_scope, "controlled.guardrail",
                        ("controlled-eval:hook-loop-harness",), True, True)
    return 1.0 if assess_hook(signal).disposition.value == "CANDIDATE" else 0.0
def evaluate_hook_loop_harness(tenant_scope: str = "loop-tenant", repeats: int = 3) -> HookLoopMeasurement:
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    baseline = [_baseline_probe(tenant_scope) for _ in range(repeats)]
    adapted = [_adapted_probe(tenant_scope) for _ in range(repeats)]
    return HookLoopMeasurement(
        "EXT-HOOK-HERMES",
        {"guardrail_interception_coverage": baseline[0]},
        {"guardrail_interception_coverage": adapted[0]},
        (),
        len(set(baseline)) == 1 and len(set(adapted)) == 1,
        {"guardrail_interception_coverage": "maximize"},
    )
def to_candidate_measurement(measurement: HookLoopMeasurement) -> CandidateMeasurement:
    if measurement.regressions:
        result = "REJECT"
    elif measurement.repeatable and measurement.adapted["guardrail_interception_coverage"] > measurement.baseline["guardrail_interception_coverage"]:
        result = "EVOLUTION_GATE_REQUIRED"
    else:
        result = "RETEST"
    return CandidateMeasurement(measurement.candidate_id, measurement.baseline, measurement.adapted,
                                measurement.regressions, measurement.repeatable, result)
