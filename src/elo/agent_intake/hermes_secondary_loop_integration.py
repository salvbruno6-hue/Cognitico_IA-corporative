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
from .hermes_cron_boundary import ScheduleSignal, assess_schedule
from .hermes_cron_evaluation import evaluate as evaluate_cron
from .hermes_mcp_evaluation import evaluate as evaluate_mcp
from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_governed_loop import advance_to_implementation
from .hermes_multiagent_boundary import DelegationSignal, assess_delegation
from .hermes_multiagent_evaluation import evaluate as evaluate_multiagent
from .implementation_evidence_adapter import measurement_to_implementation_evidence
from .independent_review import IndependentReviewEvidence, validate_independent_review
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


def run_cron_loop_probe() -> tuple[object, object]:
    """Route EXT-CRON-HERMES through the existing HERMES-AUTOMATION surface."""
    evaluation = evaluate_cron()
    signals = tuple(
        ScheduleSignal(
            f"cron-loop-{i}",
            "multiteiner",
            f"task-{i}",
            (f"controlled-eval:cron/{i}",),
            "0 8 * * *",
            "elo",
            provenance_verified=True,
            explicit_authorization=True,
            idempotent=True,
            governance_bypass=False,
        )
        for i in range(1, 6)
    )
    assessments = tuple(assess_schedule(signal) for signal in signals)
    refs = tuple(ref for assessment in assessments for ref in assessment.evidence_refs)
    boundary_integrity = all(
        not assessment.canonical_authority
        and not assessment.execution_permitted
        for assessment in assessments
    )
    return _handoff(
        "EXT-CRON-HERMES",
        "authorized_idempotent_schedule_recognition_rate",
        evaluation.baseline_rate,
        evaluation.adapted_rate,
        evaluation.repeatable,
        refs,
        boundary_integrity,
        "HERMES-AUTOMATION",
    )



def run_mcp_loop_probe() -> tuple[object, object]:
    """Route EXT-MCP-HERMES through the existing HERMES-MCP gateway surface."""
    evaluation = evaluate_mcp()
    refs = tuple(f"controlled-eval:mcp/{i}" for i in range(1, 6))
    return _handoff(
        "EXT-MCP-HERMES",
        "governed_mcp_benchmark_pass_rate",
        evaluation.baseline_rate,
        evaluation.adapted_rate,
        evaluation.repeatable,
        refs,
        evaluation.boundary_integrity_rate == 1.0,
        "HERMES-MCP",
    )


def run_independent_review_loop_probe() -> tuple[object, object]:
    """Evaluate independent review as a refinement of HERMES-DELEGATION."""
    reviews = tuple(
        IndependentReviewEvidence(
            subject_id=f"candidate:HERMES-DELEGATION:{i}",
            subject_owner_id="elo-forge",
            reviewer_id=f"elo-reviewer-{i}",
            review_scope="governance-contract",
            context_snapshot_id=f"ctx-independent-review-{i}",
            inherited_skill_ids=("skill:review",),
            authorized_tool_ids=("tool:read",),
            verdict="PASS",
            evidence_ids=(f"controlled-eval:independent-review/{i}",),
            provenance={"source": "hermes", "mode": "read_only"},
        )
        for i in range(1, 6)
    )
    valid_rate = sum(
        validate_independent_review(review)
        for review in reviews
    ) / len(reviews)
    refs = tuple(
        evidence_id
        for review in reviews
        for evidence_id in review.evidence_ids
    )
    return _handoff(
        "EXT-MULTIAGENT-HERMES",
        "independent_review_validation_rate",
        valid_rate,
        valid_rate,
        True,
        refs,
        boundary_integrity=True,
        capability_id="HERMES-DELEGATION",
    )


__all__ = [
    "run_multiagent_loop_probe",
    "run_context_plugin_loop_probe",
    "run_cron_loop_probe",
    "run_mcp_loop_probe",
    "run_independent_review_loop_probe",
]
