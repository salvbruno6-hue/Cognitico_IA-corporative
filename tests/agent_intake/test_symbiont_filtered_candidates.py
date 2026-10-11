from datetime import datetime, timezone

from elo.agent_intake.hermes_current_extensions import build_candidate
from elo.agent_intake.symbiont_adaptation import refine_capability
from elo.agent_intake.symbiont_capability_filter import FilterDisposition
from elo.agent_intake.symbiont_filtered_candidates import (
    BOUNDED_CONTEXT_ID,
    WIRE_ID,
    bounded_context_evidence,
    run_filtered_candidate_evaluation,
    wire_contract_evidence,
)
from elo.core.context_retrieval_bounds import RecallMode, normalize_bounded_retrieval
from elo.interface.wire_contract_registry import (
    build_wire_contract_registry,
    compatibility_fingerprint,
)


def test_only_selected_candidates_pass_deep_filter():
    decisions = run_filtered_candidate_evaluation()
    assert {item.candidate_id for item in decisions} == {WIRE_ID, BOUNDED_CONTEXT_ID}
    assert all(item.disposition is FilterDisposition.ACCEPT for item in decisions)


def test_wire_contract_reuses_interface_owner_and_is_observational():
    candidate = build_candidate(WIRE_ID)
    adaptation = refine_capability(
        WIRE_ID,
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": "hermes:wire-contract"},
    )
    assert candidate.owner == "ELO Interface"
    assert adaptation.existing_capacity == "ELO Interface"
    assert candidate.canonical_mutation is False
    registry = build_wire_contract_registry()
    assert {item.name for item in registry} == {"CognitiveRequest", "CognitiveResponse", "ErrorContract"}
    assert compatibility_fingerprint() == compatibility_fingerprint()
    assert wire_contract_evidence().functional_gain_proven is True


def test_bounded_context_reuses_context_owner_and_never_widens_time_scope():
    candidate = build_candidate(BOUNDED_CONTEXT_ID)
    adaptation = refine_capability(
        BOUNDED_CONTEXT_ID,
        {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": "hermes:session-search"},
    )
    assert candidate.owner == "ELO Context"
    assert adaptation.existing_capacity == "ELO Context"
    policy = normalize_bounded_retrieval(
        query="context",
        after=datetime(2026, 10, 1, tzinfo=timezone.utc),
        before=datetime(2026, 10, 3, tzinfo=timezone.utc),
    )
    relaxed = policy.relaxed_retry()
    assert relaxed.recall_mode is RecallMode.OR_RELAXED_RETRY
    assert relaxed.after == policy.after
    assert relaxed.before == policy.before
    assert bounded_context_evidence().functional_gain_proven is True
