"""Governed implementation loop for the 13 original Hermes candidates.

This module is an orchestration layer only. It reuses each candidate's
existing functional-value probe and the canonical Symbiont/ELO governed
handoff. It does not create a second state machine, Evolution Gate,
approval authority, scheduler, runtime executor, or canonical mutation path.

Each candidate is validated against its own process contract after the existing
probe runs. The contract checks that the candidate's measured process, metric,
repeatability, provenance, and governance boundary are actually represented in
the evidence package before the result can advance.
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
) -> Hermes13LoopResult:
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

    return Hermes13LoopResult(
        candidate_id=candidate_id,
        result=implementation.result,
        next_state=applied.next_state,
        canonical_mutation=applied.canonical_mutation,
        evidence_present=True,
        process_contract_valid=True,
    )


def run_hermes_13_implementation_loop() -> Hermes13ImplementationLoopReport:
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
        _normalize_probe_result(cid, probe)
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
