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
from .hermes_cron_adapter import adapt_schedule
from .hermes_cron_boundary import ScheduleSignal
from .hermes_cron_evaluation import evaluate as evaluate_cron
from .hermes_cron_functional_evaluation import evaluate_cron_functional_gain
from .hermes_mcp_evaluation import evaluate as evaluate_mcp
from .hermes_current_extensions import CandidateMeasurement, build_candidate
from .hermes_governed_loop import advance_to_implementation
from .hermes_functional_value_proof import FunctionalValueEvidence, classify
from .hermes_hook_evaluation import evaluate as evaluate_hook
from .hermes_multiagent_boundary import DelegationSignal, assess_delegation
from .hermes_multiagent_evaluation import evaluate as evaluate_multiagent
from .hermes_multiagent_functional_evaluation import evaluate_multiagent_functional_gain
from .hermes_multiagent_adapter import adapt_delegation
from .hermes_live_steering_refinement import evaluate_live_steering_gain
from .hermes_cron_continuity_refinement import evaluate_cron_continuity_gain
from .hermes_memory_provider_functional_evaluation import evaluate_memory_provider_functional_gain
from .hermes_worktree_adapter import adapt_worktree
from .hermes_worktree_boundary import WorktreeSignal
from .hermes_worktree_evaluation import evaluate as evaluate_worktree
from .hermes_worktree_functional_evaluation import evaluate_worktree_functional_gain
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
    functional_value_evidence: FunctionalValueEvidence | None = None,
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
        functional_value_evidence=functional_value_evidence,
    )
    return handoff.implementation, evidence


def run_multiagent_loop_probe() -> tuple[object, object]:
    evaluation = evaluate_multiagent()
    functional = evaluate_multiagent_functional_gain()
    signals = tuple(
        DelegationSignal(
            f"secondary-loop-{i}",
            "multiteiner",
            "elo",
            f"worker-{i}",
            f"goal-{i}",
            (f"controlled-eval:multiagent/{i}",),
            resource_scope=("read-only", "scoped-context"),
            provenance_verified=True,
            isolated_context=True,
            delegation_depth=1,
            max_child_concurrency=2,
            heartbeat_ref=f"controlled-eval:heartbeat:secondary-loop/{i}",
        )
        for i in range(1, 6)
    )
    work_items = tuple(adapt_delegation(signal) for signal in signals)
    refs = tuple(
        ref for item in work_items if item is not None for ref in item.source_refs
    )
    boundary_integrity = all(
        item is not None
        and not item.child_authority
        and not item.promotion_permitted
        for item in work_items
    )
    return _handoff(
        "EXT-MULTIAGENT-HERMES",
        "context_isolation_rate",
        functional.baseline_context_isolation_rate,
        functional.adapted_context_isolation_rate,
        functional.repeatable,
        functional.provenance_refs,
        functional.boundary_integrity,
        "HERMES-DELEGATION",
        functional_value_evidence=classify(
            "EXT-MULTIAGENT-HERMES",
            baseline=functional.baseline_context_isolation_rate,
            adapted=functional.adapted_context_isolation_rate,
            metric="context_isolation_rate",
            direction="maximize",
            repeatable=functional.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled concurrent delegated-task context isolation",
            provenance_refs=functional.provenance_refs,
        ),
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
        functional_value_evidence=classify(
            "EXT-CONTEXT-PLUGIN-HERMES",
            baseline=evaluation.baseline_success_rate,
            adapted=evaluation.adapted_success_rate,
            metric="context_task_success_rate",
            direction="maximize",
            repeatable=evaluation.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled context-resolution task",
            provenance_refs=refs,
        ),
    )


def run_hook_loop_probe() -> tuple[object, object]:
    """Route EXT-HOOK-HERMES through the existing automation capability surface."""
    evaluation = evaluate_hook()
    evidence = classify(
        "EXT-HOOK-HERMES",
        baseline=evaluation.baseline_detection_rate,
        adapted=evaluation.adapted_detection_rate,
        metric="lifecycle_guardrail_detection_rate",
        direction="maximize",
        repeatable=evaluation.repeatable,
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="controlled lifecycle guardrail detection task",
        provenance_refs=evaluation.provenance_refs,
    )
    return _handoff(
        "EXT-HOOK-HERMES",
        "lifecycle_guardrail_detection_rate",
        evaluation.baseline_detection_rate,
        evaluation.adapted_detection_rate,
        evaluation.repeatable,
        evaluation.provenance_refs,
        evaluation.boundary_integrity,
        "HERMES-AUTOMATION",
        functional_value_evidence=evidence,
    )


def run_cron_loop_probe() -> tuple[object, object]:
    """Route EXT-CRON-HERMES through HERMES-AUTOMATION with functional evidence."""
    evaluation = evaluate_cron()
    functional = evaluate_cron_functional_gain()
    return _handoff(
        "EXT-CRON-HERMES",
        "idempotency_collision_free_rate",
        functional.baseline_idempotency_collision_free_rate,
        functional.adapted_idempotency_collision_free_rate,
        functional.repeatable,
        functional.provenance_refs,
        functional.boundary_integrity,
        "HERMES-AUTOMATION",
        functional_value_evidence=classify(
            "EXT-CRON-HERMES",
            baseline=functional.baseline_idempotency_collision_free_rate,
            adapted=functional.adapted_idempotency_collision_free_rate,
            metric="idempotency_collision_free_rate",
            direction="maximize",
            repeatable=functional.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled distinct-task schedule idempotency collision prevention",
            provenance_refs=functional.provenance_refs,
        ),
    )


def run_live_steering_refinement_probe() -> tuple[object, object]:
    """Route live steering evidence through the existing multiagent owner."""
    baseline, adapted, repeatable, boundary, refs = evaluate_live_steering_gain()
    return _handoff(
        "EXT-MULTIAGENT-HERMES",
        "live_steering_boundary_integrity_rate",
        baseline,
        adapted,
        repeatable,
        refs,
        boundary,
        "HERMES-DELEGATION",
        functional_value_evidence=classify(
            "EXT-MULTIAGENT-HERMES",
            baseline=baseline,
            adapted=adapted,
            metric="live_steering_boundary_integrity_rate",
            direction="maximize",
            repeatable=repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled live-steering contract boundary",
            provenance_refs=refs,
        ),
    )


def run_cron_continuity_refinement_probe() -> tuple[object, object]:
    """Route bounded cron continuity evidence through HERMES-AUTOMATION."""
    baseline, adapted, repeatable, boundary, refs = evaluate_cron_continuity_gain()
    return _handoff(
        "EXT-CRON-HERMES",
        "cron_continuity_boundary_integrity_rate",
        baseline,
        adapted,
        repeatable,
        refs,
        boundary,
        "HERMES-AUTOMATION",
        functional_value_evidence=classify(
            "EXT-CRON-HERMES",
            baseline=baseline,
            adapted=adapted,
            metric="cron_continuity_boundary_integrity_rate",
            direction="maximize",
            repeatable=repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled bounded prior-run continuity contract",
            provenance_refs=refs,
        ),
    )



def run_memory_provider_loop_probe() -> tuple[object, object]:
    """Route EXT-MEMPROVIDER-HERMES through the existing HERMES-MEMORY surface."""
    functional = evaluate_memory_provider_functional_gain()
    return _handoff(
        "EXT-MEMPROVIDER-HERMES",
        "provider_identity_preservation_rate",
        functional.baseline_identity_preservation_rate,
        functional.adapted_identity_preservation_rate,
        functional.repeatable,
        functional.provenance_refs,
        functional.boundary_integrity,
        "HERMES-MEMORY",
        functional_value_evidence=classify(
            "EXT-MEMPROVIDER-HERMES",
            baseline=functional.baseline_identity_preservation_rate,
            adapted=functional.adapted_identity_preservation_rate,
            metric="provider_identity_preservation_rate",
            direction="maximize",
            repeatable=functional.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled retrieval request provider/evidence identity preservation",
            provenance_refs=functional.provenance_refs,
        ),
    )


def run_worktree_loop_probe() -> tuple[object, object]:
    """Route EXT-WORKTREE-HERMES through the existing governed implementation loop."""
    evaluation = evaluate_worktree()
    functional = evaluate_worktree_functional_gain()
    signals = tuple(
        WorktreeSignal(
            f"worktree-loop-{i}",
            "multiteiner",
            f"wt/loop/{i}",
            (f"controlled-eval:worktree/{i}",),
            "main",
            True,
            provenance_verified=True,
        )
        for i in range(1, 6)
    )
    workspaces = tuple(adapt_worktree(signal) for signal in signals)
    refs = tuple(
        ref for workspace in workspaces if workspace is not None
        for ref in workspace.source_refs
    )
    boundary_integrity = all(
        workspace is not None
        and not workspace.canonical_authority
        and not workspace.merge_authority
        for workspace in workspaces
    )
    return _handoff(
        "EXT-WORKTREE-HERMES",
        "collision_free_task_rate",
        functional.baseline_collision_free_rate,
        functional.adapted_collision_free_rate,
        functional.repeatable,
        functional.provenance_refs,
        functional.boundary_integrity,
        "EXT-WORKTREE-HERMES",
        functional_value_evidence=classify(
            "EXT-WORKTREE-HERMES",
            baseline=functional.baseline_collision_free_rate,
            adapted=functional.adapted_collision_free_rate,
            metric="collision_free_task_rate",
            direction="maximize",
            repeatable=functional.repeatable,
            regressions=(),
            attribution="CANDIDATE_ATTRIBUTED",
            proof_scope="controlled concurrent-task workspace collision prevention",
            provenance_refs=functional.provenance_refs,
        ),
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
    "run_hook_loop_probe",
    "run_worktree_loop_probe",
    "run_mcp_loop_probe",
    "run_independent_review_loop_probe",
    "run_live_steering_refinement_probe",
    "run_cron_continuity_refinement_probe",
]
