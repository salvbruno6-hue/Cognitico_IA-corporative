"""Provider-neutral governed migration planning and verification.

This module does not execute migrations. It defines the evidence-bearing
contract used by Forge to prepare safe transformations before an authorized
adapter applies them.
"""

from dataclasses import dataclass
import hashlib
from typing import Mapping


class MigrationError(ValueError):
    """Raised when a migration contract cannot be admitted safely."""


@dataclass(frozen=True)
class MigrationPlan:
    migration_id: str
    tenant_id: str
    source_ref: str
    target_ref: str
    before_checksum: str
    expected_after_checksum: str
    rollback_ref: str
    provenance: Mapping[str, str]
    idempotency_key: str
    destructive: bool = False

    def __post_init__(self) -> None:
        required = {
            "migration_id": self.migration_id,
            "tenant_id": self.tenant_id,
            "source_ref": self.source_ref,
            "target_ref": self.target_ref,
            "before_checksum": self.before_checksum,
            "expected_after_checksum": self.expected_after_checksum,
            "rollback_ref": self.rollback_ref,
            "idempotency_key": self.idempotency_key,
        }
        if any(not value.strip() for value in required.values()):
            raise MigrationError("migration identity, checksums, rollback and idempotency are required")
        if not self.provenance:
            raise MigrationError("migration provenance is required")
        forbidden = {"password", "token", "access_token", "refresh_token", "api_key", "service_role", "secret"}
        if any(key.lower() in forbidden for key in self.provenance):
            raise MigrationError("secret-bearing migration provenance is forbidden")
        if self.source_ref == self.target_ref:
            raise MigrationError("migration source and target must differ")


@dataclass(frozen=True)
class MigrationVerification:
    migration_id: str
    before_checksum: str
    observed_after_checksum: str
    expected_after_checksum: str
    rollback_available: bool
    status: str

    @property
    def passed(self) -> bool:
        return self.status == "PASS"


def checksum(payload: str) -> str:
    """Produce a deterministic SHA-256 checksum for migration evidence."""
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class NativeMigration:
    """Plan and verify transformations without owning infrastructure or data."""

    @staticmethod
    def plan(
        *,
        migration_id: str,
        tenant_id: str,
        source_ref: str,
        target_ref: str,
        before_payload: str,
        expected_after_payload: str,
        rollback_ref: str,
        provenance: Mapping[str, str],
        idempotency_key: str,
        destructive: bool = False,
    ) -> MigrationPlan:
        return MigrationPlan(
            migration_id=migration_id,
            tenant_id=tenant_id,
            source_ref=source_ref,
            target_ref=target_ref,
            before_checksum=checksum(before_payload),
            expected_after_checksum=checksum(expected_after_payload),
            rollback_ref=rollback_ref,
            provenance=dict(provenance),
            idempotency_key=idempotency_key,
            destructive=destructive,
        )

    @staticmethod
    def verify(
        plan: MigrationPlan,
        *,
        observed_before_payload: str,
        observed_after_payload: str,
        rollback_available: bool,
    ) -> MigrationVerification:
        before = checksum(observed_before_payload)
        after = checksum(observed_after_payload)
        status = "PASS" if (
            before == plan.before_checksum
            and after == plan.expected_after_checksum
            and rollback_available
        ) else "BLOCKED"
        return MigrationVerification(
            migration_id=plan.migration_id,
            before_checksum=before,
            observed_after_checksum=after,
            expected_after_checksum=plan.expected_after_checksum,
            rollback_available=rollback_available,
            status=status,
        )
