"""Controlled Symbiont evaluation for selected Hermes evolution candidates.

Every registered Hermes candidate is accounted for. Historical candidate-only
observations remain preserved observations; candidates selected for integration
must pass the deep owner/objective/net-gain filter. Any newly registered candidate
without an explicit filtering disposition fails closed.

The fixtures are deterministic and synthetic. They demonstrate controlled
functional gain only; they are not production proof and execute no business work.
"""
from __future__ import annotations

from datetime import datetime, timezone

from elo.core.context_retrieval_bounds import normalize_bounded_retrieval
from elo.interface.wire_contract_registry import (
    compare_to_governed_baseline,
    compatibility_fingerprint,
)

from .hermes_current_extensions import CANDIDATES
from .hermes_functional_value_proof import FunctionalValueEvidence, classify
from .symbiont_capability_filter import (
    CapabilityEvolutionProposal,
    CapabilityFilterDecision,
    evaluate_capability_evolution,
)


WIRE_ID = "EXT-WIRE-CONTRACT-HERMES"
BOUNDED_CONTEXT_ID = "EXT-SESSION-SEARCH-BOUNDS-HERMES"
SELECTED_INTEGRATION_IDS = frozenset({WIRE_ID, BOUNDED_CONTEXT_ID})

# Candidate-only observations already present before this integration. Keeping
# them listed here is not approval or promotion; it prevents a future candidate
# from silently bypassing the deep filter by merely being appended to CANDIDATES.
LEGACY_OBSERVATION_IDS = frozenset({
    "EXT-CONTEXTREF-HERMES",
    "EXT-CHECKPOINT-HERMES",
    "EXT-HOOK-HERMES",
    "EXT-ROUTE-HERMES",
    "EXT-PROFILE-HERMES",
    "EXT-BATCH-HERMES",
    "EXT-MEMPROVIDER-HERMES",
    "EXT-LEARN-HERMES",
    "EXT-LEARNING-GRAPH-HERMES",
    "EXT-CONTEXT-PLUGIN-HERMES",
    "EXT-WORKTREE-HERMES",
    "EXT-MULTIAGENT-HERMES",
    "EXT-CRON-HERMES",
    "EXT-MCP-HERMES",
    "EXT-TOOL-SEARCH-HERMES",
    "EXT-CODE-EXEC-HERMES",
    "EXT-API-HERMES",
    "EXT-ACP-HERMES",
    "EXT-PLUGIN-CATALOG-HERMES",
    "EXT-PROMPT-CACHE-HERMES",
})


def assert_candidate_filter_coverage() -> None:
    """Fail if any registry candidate has no explicit filter disposition."""
    registered = {candidate_id for candidate_id, *_ in CANDIDATES}
    covered = set(LEGACY_OBSERVATION_IDS | SELECTED_INTEGRATION_IDS)
    missing = tuple(sorted(registered - covered))
    stale = tuple(sorted(covered - registered))
    if missing:
        raise RuntimeError(
            "Hermes candidates missing deep-filter disposition: " + ", ".join(missing)
        )
    if stale:
        raise RuntimeError(
            "deep-filter disposition references unknown candidates: " + ", ".join(stale)
        )


def wire_contract_evidence() -> FunctionalValueEvidence:
    baseline = compare_to_governed_baseline()
    first = compatibility_fingerprint()
    second = compatibility_fingerprint()
    adapted = 1.0 if baseline.compatible and first == second else 0.0
    return classify(
        WIRE_ID,
        baseline=0.0,
        adapted=adapted,
        metric="governed_contract_compatibility_detection_rate",
        direction="maximize",
        repeatable=(baseline.compatible and first == second),
        regressions=() if baseline.compatible else ("canonical_contract_drift",),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="governed canonical-interface baseline comparison",
        provenance_refs=(
            "elo:interface/governed-schema-baseline-v1",
            "controlled-eval:wire-contract/current-registry",
        ),
    )


def bounded_context_evidence() -> FunctionalValueEvidence:
    policy = normalize_bounded_retrieval(
        query="governed context",
        after=datetime(2026, 10, 1, tzinfo=timezone.utc),
        before=datetime(2026, 10, 3, tzinfo=timezone.utc),
    )
    labeled_samples = (
        (datetime(2026, 9, 30, tzinfo=timezone.utc), False),
        (datetime(2026, 10, 1, 12, tzinfo=timezone.utc), True),
        (datetime(2026, 10, 2, 12, tzinfo=timezone.utc), True),
        (datetime(2026, 10, 4, tzinfo=timezone.utc), False),
    )
    # Baseline represents unbounded admission: every timestamp is admitted.
    baseline_errors = sum(expected is False for _, expected in labeled_samples)
    baseline_error_rate = baseline_errors / len(labeled_samples)
    adapted_errors = sum(
        policy.admits_timestamp(timestamp) is not expected
        for timestamp, expected in labeled_samples
    )
    adapted_error_rate = adapted_errors / len(labeled_samples)
    repeat = normalize_bounded_retrieval(
        query="governed context",
        after=policy.after,
        before=policy.before,
    )
    return classify(
        BOUNDED_CONTEXT_ID,
        baseline=baseline_error_rate,
        adapted=adapted_error_rate,
        metric="temporal_context_admission_error_rate",
        direction="minimize",
        repeatable=(repeat == policy),
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="controlled labeled temporal-context admission fixture",
        provenance_refs=(
            "controlled-eval:bounded-context/labeled-window/1",
            "controlled-eval:bounded-context/labeled-window/2",
        ),
    )


def selected_proposals() -> tuple[CapabilityEvolutionProposal, ...]:
    return (
        CapabilityEvolutionProposal(
            candidate_id=WIRE_ID,
            existing_owner="ELO Interface",
            proposed_owner="ELO Interface",
            mechanism_objective="make interface compatibility change observable and reviewable",
            owner_objective="govern stable cognitive request/response interface contracts",
            objective_alignment_confirmed=True,
        ),
        CapabilityEvolutionProposal(
            candidate_id=BOUNDED_CONTEXT_ID,
            existing_owner="ELO Context",
            proposed_owner="ELO Context",
            mechanism_objective="increase retrieval precision using bounded temporal scope and explicit retry",
            owner_objective="assemble relevant bounded context without creating memory authority",
            objective_alignment_confirmed=True,
        ),
    )


def run_filtered_candidate_evaluation() -> tuple[CapabilityFilterDecision, ...]:
    assert_candidate_filter_coverage()
    evidence = {
        WIRE_ID: wire_contract_evidence(),
        BOUNDED_CONTEXT_ID: bounded_context_evidence(),
    }
    proposals = selected_proposals()
    proposed_ids = {item.candidate_id for item in proposals}
    if proposed_ids != SELECTED_INTEGRATION_IDS:
        raise RuntimeError("selected integration candidates and deep-filter proposals diverged")
    return tuple(
        evaluate_capability_evolution(proposal, evidence[proposal.candidate_id])
        for proposal in proposals
    )


__all__ = [
    "BOUNDED_CONTEXT_ID",
    "LEGACY_OBSERVATION_IDS",
    "SELECTED_INTEGRATION_IDS",
    "WIRE_ID",
    "assert_candidate_filter_coverage",
    "bounded_context_evidence",
    "run_filtered_candidate_evaluation",
    "selected_proposals",
    "wire_contract_evidence",
]
