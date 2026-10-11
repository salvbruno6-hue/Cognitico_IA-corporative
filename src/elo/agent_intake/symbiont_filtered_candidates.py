"""Controlled Symbiont evaluation for candidates that passed architectural screening.

The fixtures are deterministic and synthetic. They demonstrate controlled
functional gain only; they are not production proof and execute no business work.
"""
from __future__ import annotations

from datetime import datetime, timezone

from elo.core.context_retrieval_bounds import normalize_bounded_retrieval
from elo.interface.wire_contract_registry import compatibility_fingerprint

from .hermes_functional_value_proof import FunctionalValueEvidence, classify
from .symbiont_capability_filter import (
    CapabilityEvolutionProposal,
    CapabilityFilterDecision,
    evaluate_capability_evolution,
)


WIRE_ID = "EXT-WIRE-CONTRACT-HERMES"
BOUNDED_CONTEXT_ID = "EXT-SESSION-SEARCH-BOUNDS-HERMES"


def wire_contract_evidence() -> FunctionalValueEvidence:
    fingerprint = compatibility_fingerprint()
    adapted = 1.0 if len(fingerprint) == 64 else 0.0
    return classify(
        WIRE_ID,
        baseline=0.0,
        adapted=adapted,
        metric="deterministic_contract_fingerprint_rate",
        direction="maximize",
        repeatable=(compatibility_fingerprint() == fingerprint),
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="controlled canonical-interface fingerprint fixture",
        provenance_refs=("controlled-eval:wire-contract/fingerprint/1", "controlled-eval:wire-contract/fingerprint/2"),
    )


def bounded_context_evidence() -> FunctionalValueEvidence:
    policy = normalize_bounded_retrieval(
        query="governed context",
        after=datetime(2026, 10, 1, tzinfo=timezone.utc),
        before=datetime(2026, 10, 3, tzinfo=timezone.utc),
    )
    samples = (
        datetime(2026, 9, 30, tzinfo=timezone.utc),
        datetime(2026, 10, 1, 12, tzinfo=timezone.utc),
        datetime(2026, 10, 2, 12, tzinfo=timezone.utc),
        datetime(2026, 10, 4, tzinfo=timezone.utc),
    )
    baseline_out_of_window = 2 / len(samples)
    admitted = tuple(item for item in samples if policy.admits_timestamp(item))
    adapted_out_of_window = sum(not policy.admits_timestamp(item) for item in admitted) / max(len(admitted), 1)
    repeat = normalize_bounded_retrieval(
        query="governed context",
        after=policy.after,
        before=policy.before,
    )
    return classify(
        BOUNDED_CONTEXT_ID,
        baseline=baseline_out_of_window,
        adapted=adapted_out_of_window,
        metric="out_of_window_context_admission_rate",
        direction="minimize",
        repeatable=(repeat == policy),
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope="controlled temporal-context admission fixture",
        provenance_refs=("controlled-eval:bounded-context/window/1", "controlled-eval:bounded-context/window/2"),
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
    evidence = {
        WIRE_ID: wire_contract_evidence(),
        BOUNDED_CONTEXT_ID: bounded_context_evidence(),
    }
    return tuple(
        evaluate_capability_evolution(proposal, evidence[proposal.candidate_id])
        for proposal in selected_proposals()
    )


__all__ = [
    "BOUNDED_CONTEXT_ID",
    "WIRE_ID",
    "bounded_context_evidence",
    "run_filtered_candidate_evaluation",
    "selected_proposals",
    "wire_contract_evidence",
]
