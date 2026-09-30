"""Governed implementation loop for the 13 original Hermes candidates.

This module is an orchestration layer only. It reuses each candidate's
existing functional-value probe and the canonical Symbiont/ELO governed
handoff. It does not create a second state machine, Evolution Gate,
approval authority, scheduler, runtime executor, or canonical mutation path.

Learning feedback is optional and explicit: controlled probes do not create
persistent learning unless a real SkillExecutionContext is supplied.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from elo.core.learning_governance import GovernedLearningService
from elo.cognitive.symbiont_skill_feedback_loop import (
    SkillExecutionContext,
    SkillLearningFeedback,
    observe_skill_outcome,
)

from .batch_loop_integration import run_batch_loop_probe
from .checkpoint_loop_integration import run_checkpoint_loop_probe
from .contextref_functional_loop_integration import run_contextref_functional_loop_probe
from .hermes_secondary_loop_integration import (
    run_context_plugin_loop_probe,
    run_cron_loop_probe,
    run_hook_loop_probe,
    run_memory_provider_loop_probe,
    run_multiagent_loop_probe,
    run_worktree_loop_probe,
)
from .learning_graph_functional_loop_integration import run_learning_graph_functional_loop_probe
from .learning_loop_integration import run_learning_loop_probe
from .profile_loop_integration import run_profile_loop_probe
from .route_loop_integration import run_route_loop_probe
from .hermes_13_process_contract import get_process_contract
from .hermes_symbiont_loop import apply_candidate_through_symbiont


@dataclass(frozen=True, slots=True)
class Hermes13LoopResult:
    candidate_id: str
    result: str
    next_state: str
    canonical_mutation: bool
    evidence_present: bool
    process_contract_valid: bool
    learning_feedback: SkillLearningFeedback | None = None
    evidence: object | None = None


@dataclass(frozen=True, slots=True)
class Hermes13ImplementationLoopReport:
    results: tuple[Hermes13LoopResult, ...]

    @property
    def all_candidates_processed(self) -> bool:
        return (
            len(self.results) == 13
            and {item.candidate_id for item in self.results}
            == set(HERMES_13_EXECUTION_ORDER)
        )

    @property
    def authorization_pending(self) -> tuple[str, ...]:
        return tuple(
            item.candidate_id
            for item in self.results
            if item.next_state == "ELO_REVIEW"
        )

    @property
    def learning_feedback_count(self) -> int:
        return sum(item.learning_feedback is not None for item in self.results)


HERMES_13_EXECUTION_ORDER = (
    "EXT-CONTEXT-PLUGIN-HERMES", "EXT-WORKTREE-HERMES", "EXT-MULTIAGENT-HERMES",
    "EXT-CRON-HERMES", "EXT-MEMPROVIDER-HERMES", "EXT-ROUTE-HERMES",
    "EXT-PROFILE-HERMES", "EXT-BATCH-HERMES", "EXT-LEARN-HERMES",
    "EXT-LEARNING-GRAPH-HERMES", "EXT-CONTEXTREF-HERMES",
    "EXT-CHECKPOINT-HERMES", "EXT-HOOK-HERMES",
)

Probe = Callable[[], tuple[object, object]]


def _normalize_probe_result(
    candidate_id: str,
    probe: Probe,
    *,
    learning_service: GovernedLearningService | None = None,
    learning_context: SkillExecutionContext | None = None,
) -> Hermes13LoopResult:
    if (learning_service is None) != (learning_context is None):
        raise ValueError(
            "learning_service and learning_context must be supplied together"
        )
    if learning_context is not None and learning_context.skill_id != candidate_id:
        raise ValueError(
            f"{candidate_id}: learning context skill_id does not match candidate"
        )

    contract = get_process_contract(candidate_id)
    applied = apply_candidate_through_symbiont(
        candidate_id,
        probe,
        implementation_first=contract.implementation_first,
    )
    implementation = applied.implementation
    evidence = applied.evidence
    if evidence is None:
        raise RuntimeError(
            f"{candidate_id}: candidate process completed without implementation evidence"
        )

    contract.validate_evidence(evidence)

    feedback = None
    if learning_service is not None and learning_context is not None:
        feedback = observe_skill_outcome(
            learning_service,
            learning_context,
            evidence_complete=bool(learning_context.evidence_ids),
        )

    return Hermes13LoopResult(
        candidate_id=candidate_id,
        result=implementation.result,
        next_state=applied.next_state,
        canonical_mutation=applied.canonical_mutation,
        evidence_present=True,
        process_contract_valid=True,
        learning_feedback=feedback,
        evidence=evidence,
    )


def run_hermes_13_implementation_loop(
    *,
    learning_service: GovernedLearningService | None = None,
    learning_contexts: Mapping[str, SkillExecutionContext] | None = None,
) -> Hermes13ImplementationLoopReport:
    """Run the 13 candidates and optionally capture explicit execution learning.

    If learning_contexts are omitted, the loop remains a controlled probe and
    produces no persistent learning. When supplied, each context must identify
    the matching candidate; observed outcomes then enter the existing governed
    trigger lifecycle.
    """
    contexts = learning_contexts or {}
    if (learning_service is None) != (not contexts):
        raise ValueError(
            "learning_service and learning_contexts must be supplied together"
        )
    unknown = tuple(
        candidate_id for candidate_id in contexts
        if candidate_id not in HERMES_13_EXECUTION_ORDER
    )
    if unknown:
        raise ValueError(
            "learning_contexts contains non-canonical Hermes candidates: "
            + ", ".join(unknown)
        )

    probes = (
        ("EXT-CONTEXT-PLUGIN-HERMES", run_context_plugin_loop_probe),
        ("EXT-WORKTREE-HERMES", run_worktree_loop_probe),
        ("EXT-MULTIAGENT-HERMES", run_multiagent_loop_probe),
        ("EXT-CRON-HERMES", run_cron_loop_probe),
        ("EXT-MEMPROVIDER-HERMES", run_memory_provider_loop_probe),
        ("EXT-ROUTE-HERMES", run_route_loop_probe),
        ("EXT-PROFILE-HERMES", run_profile_loop_probe),
        ("EXT-BATCH-HERMES", run_batch_loop_probe),
        ("EXT-LEARN-HERMES", run_learning_loop_probe),
        ("EXT-LEARNING-GRAPH-HERMES", run_learning_graph_functional_loop_probe),
        ("EXT-CONTEXTREF-HERMES", run_contextref_functional_loop_probe),
        ("EXT-CHECKPOINT-HERMES", run_checkpoint_loop_probe),
        ("EXT-HOOK-HERMES", run_hook_loop_probe),
    )
    report = Hermes13ImplementationLoopReport(tuple(
        _normalize_probe_result(
            cid,
            probe,
            learning_service=learning_service,
            learning_context=contexts.get(cid),
        )
        for cid, probe in probes
    ))
    if not report.all_candidates_processed:
        raise RuntimeError(
            "Hermes 13 implementation loop did not process exactly the canonical 13 candidates"
        )
    if not all(item.process_contract_valid for item in report.results):
        raise RuntimeError("Hermes 13 implementation loop contains invalid process evidence")
    if any(item.canonical_mutation for item in report.results):
        raise RuntimeError(
            "Hermes 13 implementation loop attempted canonical mutation"
        )
    return report


__all__ = [
    "HERMES_13_EXECUTION_ORDER",
    "Hermes13ImplementationLoopReport",
    "Hermes13LoopResult",
    "run_hermes_13_implementation_loop",
]
