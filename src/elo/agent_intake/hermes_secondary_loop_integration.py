"""Shared governed-loop adapters for already-evaluated Hermes candidates.

Only candidates with an existing canonical Symbiont adaptation surface are
routed here. This module does not create a new state machine, authority,
Evolution Gate, execution path, or canonical mutation path.
"""
from __future__ import annotations

from .hermes_context_plugin_boundary import (
    ContextEnginePluginSignal,
    assess_context_engine_plugin,
)
from .hermes_context_plugin_evaluation import evaluate_context_plugin_candidate
from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_governed_loop import advance_to_implementation
from .hermes_multiagent_boundary import DelegationSignal, assess_delegation
from .hermes_multiagent_evaluation import evaluate as evaluate_multiagent
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def _handoff(
    candidate_id: str,
    metric: str,
    baseline: float,
    adapted: float,
    repeatable: bool,
    provenance_refs: tuple[str, ...],
    boundary_integrity: bool,
    capability_id: str,
):
    candidate = build_candidate(candidate_id)
    result = (
        "EVOLUTION_GATE_REQUIRED"
        if adapted > baseline and repeatable
        else "RETEST"
    )
    measurement = CandidateMeasurement(
        candidate.candidate_id,
        {metric: baseline},
        {metric: adapted},
        (),
        repeatable,
        result,
    )
    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={metric: "maximize"},
        provenance_refs=provenance_refs,
        boundary_integrity=boundary_integrity,
    )
    adaptation = refine_capability(
        capability_id,
        {
            "controlled_test": True,
            "outcome": {
                "boundary": boundary_integrity,
                "evaluation": True,
            },
        },
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


def run_multiagent_loop_probe() -> tuple[object, object]:
    evaluation = evaluate_multiagent()
    signals = tuple(
        DelegationSignal(
            f"secondary-loop-{i}",
            "multiteiner",
            "elo",
            f"worker-{i}",
            f"goal-{i}",
            (f"controlled-eval:multiagent/{i}",),
            provenance_verified=True,
            isolated_context=True,
        )
        for i in range(1, 6)
    )
    assessments = tuple(assess_delegation(signal) for signal in signals)
    refs = tuple(ref for assessment in assessments for ref in assessment.evidence_refs)
    boundary_integrity = all(
        not assessment.canonical_authority
        and not assessment.execution_permitted
        and not assessment.promotion_permitted
        for assessment in assessments
    )
    return _handoff(
        "EXT-MULTIAGENT-HERMES",
        "valid_delegation_recognition_rate",
        evaluation.baseline_rate,
        evaluation.adapted_rate,
        evaluation.repeatable,
        refs,
        boundary_integrity,
        "HERMES-DELEGATION",
    )


def run_context_plugin_loop_probe() -> tuple[object, object]:
    evaluation = evaluate_context_plugin_candidate()
    signals = tuple(
        ContextEnginePluginSignal(
            f"secondary-loop-{i}",
            "multiteiner",
            "lcm",
            "lcm",
            ("controlled-eval:context-plugin",),
            explicit_activation=True,
            provenance_verified=True,
        )
        for i in range(5)
    )
    assessments = tuple(assess_context_engine_plugin(signal) for signal in signals)
    refs = tuple(ref for assessment in assessments for ref in assessment.evidence_refs)
    boundary_integrity = all(
        not assessment.canonical_authority
        and not assessment.activation_permitted
        for assessment in assessments
    )
    return _handoff(
        "EXT-CONTEXT-PLUGIN-HERMES",
        "context_task_success_rate",
        evaluation.baseline_success_rate,
        evaluation.adapted_success_rate,
        evaluation.repeatable,
        refs,
        boundary_integrity,
        "HERMES-CONTEXT",
    )


__all__ = [
    "run_multiagent_loop_probe",
    "run_context_plugin_loop_probe",
]
