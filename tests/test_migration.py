import pytest

from elo.forge.migration import MigrationError, NativeMigration, checksum


def test_migration_plan_is_deterministic_and_evidence_bearing():
    plan = NativeMigration.plan(
        migration_id="mig-001",
        tenant_id="tenant-a",
        source_ref="schema:v1",
        target_ref="schema:v2",
        before_payload="before-state",
        expected_after_payload="after-state",
        rollback_ref="schema:v1",
        provenance={"source": "controlled-fixture", "request_id": "req-1"},
        idempotency_key="mig-001:tenant-a",
    )
    assert plan.before_checksum == checksum("before-state")
    assert plan.expected_after_checksum == checksum("after-state")
    assert plan.rollback_ref == "schema:v1"


def test_migration_verification_passes_only_when_before_after_and_rollback_match():
    plan = NativeMigration.plan(
        migration_id="mig-002",
        tenant_id="tenant-a",
        source_ref="dataset:v1",
        target_ref="dataset:v2",
        before_payload="A",
        expected_after_payload="B",
        rollback_ref="dataset:v1",
        provenance={"source": "controlled-fixture"},
        idempotency_key="mig-002:tenant-a",
    )
    result = NativeMigration.verify(
        plan,
        observed_before_payload="A",
        observed_after_payload="B",
        rollback_available=True,
    )
    assert result.passed


def test_migration_verification_blocks_drift_or_missing_rollback():
    plan = NativeMigration.plan(
        migration_id="mig-003",
        tenant_id="tenant-a",
        source_ref="dataset:v1",
        target_ref="dataset:v2",
        before_payload="A",
        expected_after_payload="B",
        rollback_ref="dataset:v1",
        provenance={"source": "controlled-fixture"},
        idempotency_key="mig-003:tenant-a",
    )
    result = NativeMigration.verify(
        plan,
        observed_before_payload="A-corrupted",
        observed_after_payload="B",
        rollback_available=False,
    )
    assert result.status == "BLOCKED"


def test_migration_rejects_secret_bearing_provenance():
    with pytest.raises(MigrationError, match="secret-bearing"):
        NativeMigration.plan(
            migration_id="mig-004",
            tenant_id="tenant-a",
            source_ref="v1",
            target_ref="v2",
            before_payload="A",
            expected_after_payload="B",
            rollback_ref="v1",
            provenance={"api_key": "forbidden"},
            idempotency_key="mig-004:tenant-a",
        )


def test_migration_rejects_same_source_and_target():
    with pytest.raises(MigrationError, match="source and target"):
        NativeMigration.plan(
            migration_id="mig-005",
            tenant_id="tenant-a",
            source_ref="v1",
            target_ref="v1",
            before_payload="A",
            expected_after_payload="B",
            rollback_ref="v1",
            provenance={"source": "fixture"},
            idempotency_key="mig-005:tenant-a",
        )
