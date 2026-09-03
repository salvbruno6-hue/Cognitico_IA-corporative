from automation.tasks.elo_maintenance_coordinator import Event, Outcome, audit, merge_gate


def base_event(**overrides):
    data = dict(
        number=1,
        concept_id="ELO.test.example",
        event_class="budget",
        acceptance_pass=True,
        specialist_pass=True,
        ci_pass=True,
        reviews_clear=True,
        scope_compliant=True,
        forbidden_action=False,
        elo_approve_merge=False,
        evidence_complete=True,
        canonical_identity_valid=True,
        architectural_impact=True,
        experience_value=False,
    )
    data.update(overrides)
    return Event(**data)


def test_routes_budget_to_finance_specialist_when_missing():
    outcome, reasons = audit(base_event(specialist_pass=None))
    assert outcome is Outcome.READY_FOR_SPECIALIST
    assert "specialist_consultation_required:domain-finance" in reasons


def test_merge_requires_explicit_elo_authorization():
    event = base_event(elo_approve_merge=False)
    outcome, _ = audit(event)
    assert outcome is Outcome.READY_FOR_ELO_DECISION
    assert not merge_gate(event)


def test_merge_is_allowed_only_after_all_gates():
    event = base_event(elo_approve_merge=True)
    assert merge_gate(event)


def test_valuable_non_architectural_experience_is_temporal():
    event = base_event(
        architectural_impact=False,
        experience_value=True,
        provenance_complete=True,
        contradiction_free=True,
        elo_approve_merge=False,
    )
    outcome, _ = audit(event)
    assert outcome is Outcome.RECORDED_AS_TEMPORAL_EXPERIENCE


def test_temporal_experience_cannot_bypass_identity_or_provenance():
    event = base_event(
        architectural_impact=False,
        experience_value=True,
        provenance_complete=False,
        contradiction_free=True,
    )
    outcome, reasons = audit(event)
    assert outcome is Outcome.WAITING_FOR_EVIDENCE
    assert "provenance_incomplete" in reasons


def test_new_capability_requires_reuse_analysis():
    event = base_event(reuse_analysis_complete=False)
    outcome, reasons = audit(event)
    assert outcome is Outcome.WAITING_FOR_EVIDENCE
    assert "reuse_analysis_required" in reasons


def test_duplicate_or_parallel_capability_is_blocked():
    event = base_event(duplicate_or_parallel_found=True)
    outcome, reasons = audit(event)
    assert outcome is Outcome.BLOCKED
    assert "duplicate_or_parallel_capability_detected" in reasons
    assert not merge_gate(event)


def test_unresolved_source_of_truth_is_blocked():
    event = base_event(source_of_truth_resolved=False)
    outcome, reasons = audit(event)
    assert outcome is Outcome.BLOCKED
    assert "source_of_truth_unresolved" in reasons


def test_canonical_contract_conflict_is_blocked():
    event = base_event(contract_conflict=True)
    outcome, reasons = audit(event)
    assert outcome is Outcome.BLOCKED
    assert "canonical_contract_conflict" in reasons
