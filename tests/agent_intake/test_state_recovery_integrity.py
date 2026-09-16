from elo.agent_intake.state_recovery_integrity import (
    CAPABILITY_ID,
    evaluate_state_recovery,
    verify_recovery_isolation,
)


def test_state_recovery_integrity_preserves_state_and_continuity():
    result = evaluate_state_recovery(
        request_id="recovery-001",
        tenant_scope="multiteiner",
        state={"tenant_scope": "multiteiner", "decision_id": "d-001", "value": 42},
    )
    assert result.capability_id == CAPABILITY_ID
    assert result.status == "recovered"
    assert result.integrity_verified is True
    assert result.continuity_verified is True
    assert result.recovered_state == {
        "tenant_scope": "multiteiner",
        "decision_id": "d-001",
        "value": 42,
    }
    assert result.learning_candidate["promotion_state"] == "candidate_only"
    assert result.learning_candidate["canonical_mutation"] is False


def test_recovery_is_repeatable_and_does_not_mutate_input():
    state = {"tenant_scope": "multiteiner", "decision_id": "d-002", "value": 7}
    first = evaluate_state_recovery(
        request_id="recovery-repeat-001",
        tenant_scope="multiteiner",
        state=state,
    )
    second = evaluate_state_recovery(
        request_id="recovery-repeat-001",
        tenant_scope="multiteiner",
        state=state,
    )
    assert first == second
    assert state == {"tenant_scope": "multiteiner", "decision_id": "d-002", "value": 7}


def test_recovery_does_not_cross_tenant_boundaries():
    first, second = verify_recovery_isolation(
        request_id="recovery-isolation-001",
        tenant_a="tenant-a",
        tenant_b="tenant-b",
    )
    assert first.recovered_state["tenant_scope"] == "tenant-a"
    assert second.recovered_state["tenant_scope"] == "tenant-b"
    assert first.recovered_state != second.recovered_state
    assert first.learning_candidate["canonical_mutation"] is False
    assert second.learning_candidate["canonical_mutation"] is False


def test_failed_integrity_never_becomes_learning_candidate_for_promotion():
    result = evaluate_state_recovery(
        request_id="recovery-invalid-001",
        tenant_scope="multiteiner",
        state={"tenant_scope": "other-tenant", "value": 1},
    )
    assert result.status == "failed"
    assert result.integrity_verified is True
    assert result.continuity_verified is False
    assert result.learning_candidate["promotion_state"] == "candidate_only"
    assert result.learning_candidate["canonical_mutation"] is False
