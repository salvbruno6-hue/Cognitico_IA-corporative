from elo.agent_intake.memory_context_retention import (
    CONTEXT_CAPABILITY_ID,
    MEMORY_CAPABILITY_ID,
    retention_evidence,
    validate_retention_capability_mapping,
)


def _records():
    return (
        {"id": "critical", "tenant_scope": "multiteiner", "text": "project decision critical requirement"},
        {"id": "background", "tenant_scope": "multiteiner", "text": "background operational note"},
        {"id": "other-tenant", "tenant_scope": "other", "text": "project decision critical requirement"},
    )


def test_retention_preserves_required_context_across_boundary():
    result = retention_evidence(
        request_id="retention-01",
        tenant_scope="multiteiner",
        records=_records(),
        required_ids=("critical",),
        query="critical requirement",
        retention_ids=("critical", "background"),
    )
    assert result.status == "completed"
    assert result.memory_capability_id == MEMORY_CAPABILITY_ID
    assert result.context_capability_id == CONTEXT_CAPABILITY_ID
    assert result.retained_ids == ("critical", "background")
    assert result.learning_candidate["promotion_state"] == "candidate_only"
    assert result.learning_candidate["canonical_mutation"] is False


def test_retention_is_tenant_scoped_and_deterministic():
    result = retention_evidence(
        request_id="retention-02",
        tenant_scope="multiteiner",
        records=_records(),
        required_ids=("critical",),
        query="critical requirement",
        retention_ids=("critical",),
    )
    assert result.status == "completed"
    assert result.evidence[1]["adapted_recall"] == ("critical",)


def test_retention_failure_is_not_learning():
    result = retention_evidence(
        request_id="retention-03",
        tenant_scope="multiteiner",
        records=_records(),
        required_ids=("critical",),
        query="critical requirement",
        retention_ids=("background",),
    )
    assert result.status == "failed"
    assert result.evidence[2]["continuity_preserved"] is False
    assert result.learning_candidate["promotion_state"] == "candidate_only"
    assert result.learning_candidate["canonical_mutation"] is False


def test_mapping_does_not_create_a_new_capability():
    validate_retention_capability_mapping()
