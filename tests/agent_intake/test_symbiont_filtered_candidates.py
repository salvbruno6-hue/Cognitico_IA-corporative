from datetime import datetime, timezone

import pytest

from elo.agent_intake.hermes_current_extensions import CANDIDATES, build_candidate
from elo.agent_intake.symbiont_adaptation import refine_capability
from elo.agent_intake.symbiont_capability_filter import FilterDisposition
from elo.agent_intake.skill_change_awareness import detect_skill_inventory_delta, inventory_digest
from elo.agent_intake.symbiont_filtered_candidates import (
    BOUNDED_CONTEXT_ID, LEGACY_OBSERVATION_IDS, SELECTED_INTEGRATION_IDS, SKILL_CHANGE_ID, WIRE_ID,
    assert_candidate_filter_coverage, bounded_context_evidence, run_filtered_candidate_evaluation,
    skill_change_evidence, wire_contract_evidence,
)
from elo.core.context_retrieval_bounds import RecallMode, normalize_bounded_retrieval
from elo.interface.wire_contract_registry import GOVERNED_SCHEMA_BASELINE, build_wire_contract_registry, compare_to_governed_baseline, compatibility_fingerprint


def test_every_registered_candidate_has_an_explicit_filter_disposition():
    assert_candidate_filter_coverage()
    registered = {candidate_id for candidate_id, *_ in CANDIDATES}
    assert registered == set(LEGACY_OBSERVATION_IDS | SELECTED_INTEGRATION_IDS)


def test_unaccounted_candidate_would_fail_closed(monkeypatch):
    import elo.agent_intake.symbiont_filtered_candidates as module
    monkeypatch.setattr(module, "CANDIDATES", module.CANDIDATES + (("EXT-UNREVIEWED", "new mechanism", "Parallel Owner", "unknown"),))
    with pytest.raises(RuntimeError, match="missing deep-filter disposition"):
        module.assert_candidate_filter_coverage()


def test_only_selected_candidates_pass_deep_filter():
    decisions = run_filtered_candidate_evaluation()
    assert {item.candidate_id for item in decisions} == {WIRE_ID, BOUNDED_CONTEXT_ID, SKILL_CHANGE_ID}
    assert all(item.disposition is FilterDisposition.ACCEPT for item in decisions)


def test_wire_contract_reuses_interface_owner_and_checks_governed_baseline():
    candidate = build_candidate(WIRE_ID)
    adaptation = refine_capability(WIRE_ID, {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": "hermes:wire-contract"})
    assert candidate.owner == "ELO Interface"
    assert adaptation.existing_capacity == "ELO Interface"
    assert candidate.canonical_mutation is False
    registry = build_wire_contract_registry()
    assert {item.name for item in registry} == {"CognitiveRequest", "CognitiveResponse", "ErrorContract"}
    assert {item.name: item.schema_digest for item in registry} == GOVERNED_SCHEMA_BASELINE
    compatibility = compare_to_governed_baseline()
    assert compatibility.compatible is True
    assert compatibility.changed_contracts == ()
    assert compatibility.missing_contracts == ()
    assert compatibility.unexpected_contracts == ()
    assert compatibility_fingerprint() == compatibility_fingerprint()
    assert wire_contract_evidence().functional_gain_proven is True


def test_bounded_context_reuses_context_owner_and_never_widens_time_scope():
    candidate = build_candidate(BOUNDED_CONTEXT_ID)
    adaptation = refine_capability(BOUNDED_CONTEXT_ID, {"controlled_test": True, "outcome": {"boundary": True}, "source_reference": "hermes:session-search"})
    assert candidate.owner == "ELO Context"
    assert adaptation.existing_capacity == "ELO Context"
    policy = normalize_bounded_retrieval(query="context", after=datetime(2026, 10, 1, tzinfo=timezone.utc), before=datetime(2026, 10, 3, tzinfo=timezone.utc))
    relaxed = policy.relaxed_retry()
    assert relaxed.recall_mode is RecallMode.OR_RELAXED_RETRY
    assert relaxed.after == policy.after
    assert relaxed.before == policy.before
    assert bounded_context_evidence().functional_gain_proven is True


def test_bounded_context_metric_uses_original_labeled_samples():
    evidence = bounded_context_evidence()
    assert evidence.baseline == 0.5
    assert evidence.adapted == 0.0
    assert evidence.metric == "temporal_context_admission_error_rate"


def test_skill_change_awareness_is_deterministic_and_observational():
    before = {"planning": "sha-a", "audit": "sha-b"}
    after = {"planning": "sha-a2", "audit": "sha-b", "forecast": "sha-c"}
    delta = detect_skill_inventory_delta(before, after)
    assert delta.added == ("forecast",)
    assert delta.changed == ("planning",)
    assert delta.removed == ()
    assert delta.has_change is True
    assert inventory_digest(before) == inventory_digest(dict(reversed(tuple(before.items()))))
    candidate = build_candidate(SKILL_CHANGE_ID)
    assert candidate.owner == "ELO Knowledge & Skills"
    assert candidate.canonical_mutation is False
    assert skill_change_evidence().functional_gain_proven is True
