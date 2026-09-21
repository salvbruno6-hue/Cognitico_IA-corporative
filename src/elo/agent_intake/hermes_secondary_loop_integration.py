"""Shared governed-loop adapters for already-evaluated Hermes secondary candidates.

These adapters consolidate existing candidate evaluations into the canonical
Hermes governed mediator. They do not create a new state machine, authority,
Evolution Gate, execution path, or canonical mutation path.
"""
from __future__ import annotations

from .hermes_context_plugin_boundary import (
    ContextEnginePluginSignal,
    PluginDisposition,
    assess_context_engine_plugin,
)
from .hermes_context_plugin_evaluation import evaluate_context_plugin_candidate
from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_governed_loop import advance_to_implementation
from .hermes_learning_graph_evaluation import evaluate as evaluate_learning_graph
from .hermes_multiagent_boundary import DelegationSignal, assess_delegation
from .hermes_multiagent_evaluation import evaluate as evaluate_multiagent
from .hermes_worktree_boundary import WorktreeSignal, assess_worktree
from .hermes_worktree_evaluation import evaluate as evaluate_worktree
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .symbiont_adaptation import refine_capability


def _handoff(candidate_id: str, metric: str, baseline: float, adapted: float,
             repeatable: bool, provenance_refs: tuple[str, ...],
             boundary_integrity: bool, capability_id: str):
    candidate = build_candidate(candidate_id)
    measurement = CandidateMeasurement(
        candidate.candidate_id,
        {metric: baseline},
        {metric: adapted},
        (),
        repeatable,
        "EVOLUTION_GATE_REQUIRED" if adapted > baseline and repeatable else "RETEST",
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
        {"controlled_test": True, "outcome": {"boundary": boundary_integrity, "evaluation": True}},
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
            f"secondary-loop-{i}", "multiteiner", "elo", f"worker-{i}",
            f"goal-{i}", (f"controlled-eval:multiagent/{i}",),
            provenance_verified=True, isolated_context=True,
        )
        for i in range(1, 6)
    )
    boundary = tuple(assess_delegation(s) for s in signals)
    refs = tuple(ref for assessment in boundary for ref in assessment.evidence_refs)
    return _handoff(
        "EXT-MULTIAGENT-HERMES",
        "valid_delegation_recognition_rate",
        evaluation.baseline_rate,
        evaluation.adapted_rate,
        evaluation.repeatable,
        refs,
        all(not a.canonical_authority and not a.execution_permitted and not a.promotion_permitted for a in boundary),
        "HERMES-DELEGATION",
    )


def run_worktree_loop_probe() -> tuple[object, object]:
    evaluation = evaluate_worktree()
    signals = tuple(
        WorktreeSignal(
            f"secondary-loop-{i}", "multiteiner", f"wt/secondary/{i}",
            (f"controlled-eval:worktree/{i}",), "main", True,
            provenance_verified=True,
        )
        for i in range(1, 6)
    )
    boundary = tuple(assess_worktree(s) for s in signals)
    refs = tuple(ref for assessment in boundary for ref in assessment.evidence_refs)
    return _handoff(
        "EXT-WORKTREE-HERMES",
        "valid_isolation_recognition_rate",
        evaluation.baseline_rate,
        evaluation.adapted_rate,
        evaluation.repeatable,
        refs,
        all(not a.canonical_authority and not a.merge_permitted for a in boundary),
        "HERMES-MCP",
    )


def run_context_plugin_loop_probe() -> tuple[object, object]:
    evaluation = evaluate_context_plugin_candidate()
    signals = tuple(
        ContextEnginePluginSignal(
            f"secondary-loop-{i}", "multiteiner", "lcm", "lcm",
            ("controlled-eval:context-plugin",), True, provenance_verified=True,
        )
        for i in range(5)
    )
    boundary = tuple(assess_context_engine_plugin(s) for s in signals)
    refs = tuple(ref for assessment in boundary for ref in assessment.evidence_refs)
    return _handoff(
        "EXT-CONTEXT-PLUGIN-HERMES",
        "context_task_success_rate",
        evaluation.baseline_success_rate,
        evaluation.adapted_success_rate,
        evaluation.repeatable,
        refs,
        all(not a.canonical_authority and not a.activation_permitted for a in boundary),
        "HERMES-CONTEXT",
    )


def run_learning_graph_loop_probe() -> tuple[object, object]:
    evaluation = evaluate_learning_graph()
    return _handoff(
        "EXT-LEARNING-GRAPH-HERMES",
        "valid_learning_graph_relation_rate",
        evaluation.baseline_rate,
        evaluation.adapted_rate,
        evaluation.repeatable,
        tuple(f"controlled-eval:learning-graph/{i}" for i in range(1, 6)),
        evaluation.boundary_integrity_rate == 1.0,
        "HERMES-MEMORY",
    )


__all__ = [
    "run_multiagent_loop_probe",
    "run_worktree_loop_probe",
    "run_context_plugin_loop_probe",
    "run_learning_graph_loop_probe",
]
