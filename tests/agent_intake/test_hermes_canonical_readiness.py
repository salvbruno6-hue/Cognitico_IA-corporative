from src.elo.agent_intake.hermes_canonical_readiness import (
    HERMES_EVALUATED_CAPABILITIES, HermesReadinessEvidence, Readiness,
    canonical_mutation_permitted, evaluate_readiness,
)

def _evidence(**overrides):
    data = dict(candidate_id="EXT-CONTEXTREF-HERMES", owner="ELO Context",
        baseline_id="baseline-1", experiment_id="exp-1", metric="latency_ms",
        baseline_value=100.0, candidate_value=90.0, metric_direction="lower",
        repeatability_runs=2, repeatability_passed=True, security_verified=True,
        isolation_verified=True, authority_conflict=False, evolution_gate="PASS",
        approval_ref="approval-1", promotion_package_ref="package-1")
    data.update(overrides)
    return HermesReadinessEvidence(**data)

def test_evaluated_scope_contains_all_current_hermes_mechanisms():
    assert len(HERMES_EVALUATED_CAPABILITIES) == 14
    assert "EXT-CHECKPOINT-HERMES" in HERMES_EVALUATED_CAPABILITIES
    assert "EXT-CURATOR-HERMES" in HERMES_EVALUATED_CAPABILITIES

def test_complete_repeatable_evidence_is_green():
    assert evaluate_readiness(_evidence()) is Readiness.GREEN_READY_FOR_EVOLUTION_GATE

def test_single_run_is_not_green():
    assert evaluate_readiness(_evidence(repeatability_runs=1)) is Readiness.YELLOW_EVIDENCE_PENDING

def test_missing_measurable_gain_is_not_green():
    assert evaluate_readiness(_evidence(candidate_value=100.0)) is Readiness.YELLOW_EVIDENCE_PENDING

def test_security_or_isolation_gap_is_not_green():
    assert evaluate_readiness(_evidence(security_verified=False)) is Readiness.YELLOW_EVIDENCE_PENDING
    assert evaluate_readiness(_evidence(isolation_verified=False)) is Readiness.YELLOW_EVIDENCE_PENDING

def test_authority_conflict_is_red():
    assert evaluate_readiness(_evidence(authority_conflict=True)) is Readiness.RED_REJECTED

def test_unknown_candidate_is_red():
    assert evaluate_readiness(_evidence(candidate_id="EXT-UNKNOWN-HERMES")) is Readiness.RED_REJECTED

def test_evolution_gate_and_approval_are_required_for_green():
    assert evaluate_readiness(_evidence(evolution_gate="PENDING")) is Readiness.YELLOW_EVIDENCE_PENDING
    assert evaluate_readiness(_evidence(approval_ref=None)) is Readiness.YELLOW_EVIDENCE_PENDING
    assert evaluate_readiness(_evidence(promotion_package_ref=None)) is Readiness.YELLOW_EVIDENCE_PENDING

def test_readiness_never_grants_canonical_mutation():
    assert canonical_mutation_permitted(_evidence()) is False