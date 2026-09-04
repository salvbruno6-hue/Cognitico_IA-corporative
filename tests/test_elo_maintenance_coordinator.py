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
        canonical_target_resolved=True,
        source_of_truth_resolved=True,
        reuse_analysis_complete=True,
        duplicate_or_parallel_found=False,
        contract_conflict=False,
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


def test_unknown_canonical_evidence_blocks_architectural_admission():
    event = base_event(
        canonical_target_resolved=False,
        source_of_truth_resolved=False,
        reuse_analysis_complete=False,
        duplicate_or_parallel_found=None,
        contract_conflict=None,
    )
    outcome, reasons = audit(event)
    assert outcome is Outcome.WAITING_FOR_EVIDENCE
    assert "canonical_target_unresolved" in reasons
    assert "duplicate_or_parallel_state_unknown" in reasons


def test_parallel_capability_blocks_architectural_admission():
    event = base_event(duplicate_or_parallel_found=True)
    outcome, reasons = audit(event)
    assert outcome is Outcome.BLOCKED
    assert "duplicate_or_parallel_capability_found" in reasons
