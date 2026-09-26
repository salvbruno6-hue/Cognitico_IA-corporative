from elo.agent_intake.checkpoint_compaction_guard import (
    CAPABILITY_ID,
    CheckpointReceipt,
    CompressionBoundaryRequest,
    evaluate_compression_boundary,
)


def receipt(*, scope: str = "tenant-a", state: str = "CONFIRMED", durable: bool = True):
    return CheckpointReceipt(
        checkpoint_id="cp-001",
        provider_id="provider-test",
        tenant_scope=scope,
        state=state,
        durable=durable,
        evidence_id="evidence-001",
    )


def test_optional_checkpoint_does_not_block_boundary():
    result = evaluate_compression_boundary(
        CompressionBoundaryRequest("req-001", "tenant-a", checkpoint_required=False),
        checkpoint=None,
    )
    assert result.decision == "ALLOW"
    assert result.capability_id == CAPABILITY_ID


def test_required_checkpoint_fails_closed_when_absent():
    result = evaluate_compression_boundary(
        CompressionBoundaryRequest("req-002", "tenant-a", checkpoint_required=True),
        checkpoint=None,
    )
    assert result.decision == "BLOCK"
    assert "absent" in result.reason


def test_required_checkpoint_allows_only_durable_confirmation():
    result = evaluate_compression_boundary(
        CompressionBoundaryRequest("req-003", "tenant-a", checkpoint_required=True),
        checkpoint=receipt(),
    )
    assert result.decision == "ALLOW"
    assert result.checkpoint_id == "cp-001"
    assert result.evidence_id == "evidence-001"


def test_unconfirmed_checkpoint_blocks_boundary():
    result = evaluate_compression_boundary(
        CompressionBoundaryRequest("req-004", "tenant-a", checkpoint_required=True),
        checkpoint=receipt(state="UNCONFIRMED"),
    )
    assert result.decision == "BLOCK"


def test_non_durable_checkpoint_blocks_boundary():
    result = evaluate_compression_boundary(
        CompressionBoundaryRequest("req-005", "tenant-a", checkpoint_required=True),
        checkpoint=receipt(durable=False),
    )
    assert result.decision == "BLOCK"


def test_scope_mismatch_blocks_cross_tenant_recovery():
    result = evaluate_compression_boundary(
        CompressionBoundaryRequest("req-006", "tenant-a", checkpoint_required=True),
        checkpoint=receipt(scope="tenant-b"),
    )
    assert result.decision == "BLOCK"
    assert "scope" in result.reason


def test_guard_never_transfers_authority():
    result = evaluate_compression_boundary(
        CompressionBoundaryRequest("req-007", "tenant-a", checkpoint_required=True),
        checkpoint=receipt(),
    )
    assert result.authority_transfer is False
