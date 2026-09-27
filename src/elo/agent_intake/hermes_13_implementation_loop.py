"""Governed implementation loop for the 13 original Hermes candidates.

This module is an orchestration layer only. It reuses each candidate's
existing functional-value probe and the canonical Symbiont/ELO governed
handoff. It does not create a second state machine, Evolution Gate,
approval authority, scheduler, runtime executor, or canonical mutation path.

The loop deliberately stops candidates at the existing governance boundary:
functional evidence -> Evolution Gate/ELO review -> explicit authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

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
from .learning_graph_functional_loop_integration import (
    run_learning_graph_functional_loop_probe,
)
from .learning_loop_integration import run_learning_loop_probe
from .profile_loop_integration import run_profile_loop_probe
from .route_loop_integration import run_route_loop_probe


@dataclass(frozen=True, slots=True)
class Hermes13LoopResult:
    candidate_id: str
    result: str
    next_state: str
    canonical_mutation: bool
    evidence_present: bool


@dataclass(frozen=True, slots=True)
class Hermes13ImplementationLoopReport:
    results: tuple[Hermes13LoopResult, ...]

    @property
    def all_candidates_processed(self) -> bool:
        return len(self.results) == 13 and {
            item.candidate_id for item in self.results
        } == set(HERMES_13_EXECUTION_ORDER)

    @property
    def authorization_pending(self) -> tuple[str, ...]:
        return tuple(
            item.candidate_id
            for item in self.results
            if item.next_state == "ELO_REVIEW"
        )


HERMES_13_EXECUTION_ORDER: tuple[str, ...] = (
    "EXT-CONTEXT-PLUGIN-HERMES",
    "EXT-WORKTREE-HERMES",
    "EXT-MULTIAGENT-HERMES",
    "EXT-CRON-HERMES",
    "EXT-MEMPROVIDER-HERMES",
    "EXT-ROUTE-HERMES",
    "EXT-PROFILE-HERMES",
    "EXT-BATCH-HERMES",
    "EXT-LEARN-HERMES",
    "EXT-LEARNING-GRAPH-HERMES",
    "EXT-CONTEXTREF-HERMES",
    "EXT-CHECKPOINT-HERMES",
    "EXT-HOOK-HERMES",
)

# The callable return shapes are already canonical candidate adapters.
# Checkpoint historically returns (evidence, implementation); the wrapper
# below normalizes that legacy ordering without changing the adapter itself.
Probe = Callable[[], tuple[object, object]]


def _normalize_probe_result(
    candidate_id: str,
    probe: Probe,
    *,
    implementation_first: bool = True,
) -> Hermes13LoopResult:
    first, second = probe()
    implementation = first if implementation_first else second
    evidence = second if implementation_first else first

    return Hermes13LoopResult(
        candidate_id=candidate_id,
        result=implementation.result,
        next_state=implementation.next_state,
        canonical_mutation=implementation.canonical_mutation,
        evidence_present=evidence is not None,
    )


def run_hermes_13_implementation_loop() -> Hermes13ImplementationLoopReport:
    """Run the 13 candidates through the existing governed handoff.

    No approval flags are supplied. Therefore this function can advance
    technically eligible candidates to the existing ELO review boundary, but
    cannot authorize implementation or mutate canonical state.
    """

    probes: tuple[tuple[str, Probe, bool], ...] = (
        ("EXT-CONTEXT-PLUGIN-HERMES", run_context_plugin_loop_probe, True),
        ("EXT-WORKTREE-HERMES", run_worktree_loop_probe, True),
        ("EXT-MULTIAGENT-HERMES", run_multiagent_loop_probe, True),
        ("EXT-CRON-HERMES", run_cron_loop_probe, True),
        ("EXT-MEMPROVIDER-HERMES", run_memory_provider_loop_probe, True),
        ("EXT-ROUTE-HERMES", run_route_loop_probe, True),
        ("EXT-PROFILE-HERMES", run_profile_loop_probe, True),
        ("EXT-BATCH-HERMES", run_batch_loop_probe, True),
        ("EXT-LEARN-HERMES", run_learning_loop_probe, True),
        (
            "EXT-LEARNING-GRAPH-HERMES",
            run_learning_graph_functional_loop_probe,
            True,
        ),
        (
            "EXT-CONTEXTREF-HERMES",
            run_contextref_functional_loop_probe,
            True,
        ),
        ("EXT-CHECKPOINT-HERMES", run_checkpoint_loop_probe, False),
        ("EXT-HOOK-HERMES", run_hook_loop_probe, True),
    )

    results = tuple(
        _normalize_probe_result(
            candidate_id,
            probe,
            implementation_first=implementation_first,
        )
        for candidate_id, probe, implementation_first in probes
    )

    report = Hermes13ImplementationLoopReport(results=results)

    if not report.all_candidates_processed:
        raise RuntimeError("Hermes 13 implementation loop did not process exactly the canonical 13 candidates")

    if any(item.canonical_mutation for item in report.results):
        raise RuntimeError("Hermes 13 implementation loop attempted canonical mutation")

    return report


__all__ = [
    "HERMES_13_EXECUTION_ORDER",
    "Hermes13ImplementationLoopReport",
    "Hermes13LoopResult",
    "run_hermes_13_implementation_loop",
]
