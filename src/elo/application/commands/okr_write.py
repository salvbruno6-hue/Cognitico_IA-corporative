"""Governed strategic OKR write service.

Layer: application
Owner: strategic-objective-domain (write coordination)
Authority: elo-authz (external)

This service never authorizes a caller. It accepts only a normalized grant already
issued by the canonical ``elo-authz`` boundary and delegates persistence to a
write port. The service does not own KPI, evidence, decision, execution or
learning authorities.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from typing import Protocol

from elo.contracts.okr import KeyResult, Objective, TargetApprovalState


class StrategicWriteAction(StrEnum):
    PROPOSE = "strategic_okr_propose"
    REVIEW = "strategic_okr_review"
    APPROVE = "strategic_okr_approve"
    CANONICAL_WRITE = "strategic_okr_write"


ACTION_CAPABILITY = {
    StrategicWriteAction.PROPOSE: "PROPOSE",
    StrategicWriteAction.REVIEW: "REVIEW",
    StrategicWriteAction.APPROVE: "APPROVE",
    StrategicWriteAction.CANONICAL_WRITE: "CANONICAL_WRITE",
}


def objective_resource_ref(objective_id: str) -> str:
    value = objective_id.strip()
    if not value:
        raise ValueError("objective_id is required")
    return f"strategic_okr:objective:{value}"


def key_result_resource_ref(key_result_id: str) -> str:
    value = key_result_id.strip()
    if not value:
        raise ValueError("key_result_id is required")
    return f"strategic_okr:key_result:{value}"


def binding_resource_ref(key_result_id: str, snapshot_id: str) -> str:
    kr = key_result_id.strip()
    snapshot = snapshot_id.strip()
    if not kr or not snapshot:
        raise ValueError("key_result_id and snapshot_id are required")
    return f"strategic_okr:binding:{kr}:{snapshot}"


@dataclass(frozen=True, slots=True)
class StrategicWriteGrant:
    """Normalized, tenant- and resource-bound receipt from ``elo-authz``."""

    authorized: bool
    authority: str
    action: StrategicWriteAction
    capability_code: str
    tenant_id: str
    resource_ref: str
    identity_id: str
    evidence_ref: str
    grant_ref: str
    expires_at: datetime

    def validates(
        self,
        *,
        tenant_id: str,
        action: StrategicWriteAction,
        resource_ref: str,
        now: datetime | None = None,
    ) -> bool:
        reference = now or datetime.now(timezone.utc)
        expiry = self.expires_at
        if expiry.tzinfo is None or expiry.utcoffset() is None:
            return False
        return (
            self.authorized
            and self.authority == "elo-authz"
            and self.action is action
            and self.capability_code == ACTION_CAPABILITY[action]
            and self.tenant_id == tenant_id
            and self.resource_ref == resource_ref
            and bool(self.identity_id.strip())
            and bool(self.evidence_ref.strip())
            and bool(self.grant_ref.strip())
            and expiry > reference
        )


@dataclass(frozen=True, slots=True)
class SnapshotBindingWrite:
    tenant_id: str
    key_result_id: str
    snapshot_id: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.tenant_id.strip():
            raise ValueError("tenant_id is required")
        if not self.key_result_id.strip():
            raise ValueError("key_result_id is required")
        if not self.snapshot_id.strip():
            raise ValueError("snapshot_id is required")
        refs = tuple(dict.fromkeys(ref.strip() for ref in self.evidence_refs if ref.strip()))
        object.__setattr__(self, "evidence_refs", refs)
        if not refs:
            raise ValueError("snapshot binding requires evidence_refs")


class OkrWriteRepository(Protocol):
    def upsert_objective(self, objective: Objective, *, authorization_ref: str) -> None: ...
    def upsert_key_result(self, key_result: KeyResult, *, authorization_ref: str) -> None: ...
    def bind_snapshot(self, binding: SnapshotBindingWrite, *, authorization_ref: str) -> None: ...


class GovernedOkrWriter:
    """Write coordination below the GovernedOrchestrator, never an authority."""

    def __init__(self, repository: OkrWriteRepository) -> None:
        self._repository = repository

    @staticmethod
    def _require(
        grant: StrategicWriteGrant,
        *,
        tenant_id: str,
        action: StrategicWriteAction,
        resource_ref: str,
    ) -> None:
        if not grant.validates(tenant_id=tenant_id, action=action, resource_ref=resource_ref):
            raise PermissionError("canonical tenant- and resource-bound elo-authz strategic write grant is required")

    def propose_objective(self, objective: Objective, grant: StrategicWriteGrant) -> None:
        self._require(
            grant,
            tenant_id=objective.tenant_id,
            action=StrategicWriteAction.PROPOSE,
            resource_ref=objective_resource_ref(objective.objective_id),
        )
        if not objective.evidence_refs:
            raise ValueError("objective proposal requires evidence_refs")
        self._repository.upsert_objective(objective, authorization_ref=grant.evidence_ref)

    def propose_key_result(self, key_result: KeyResult, grant: StrategicWriteGrant) -> None:
        self._require(
            grant,
            tenant_id=key_result.tenant_id,
            action=StrategicWriteAction.PROPOSE,
            resource_ref=key_result_resource_ref(key_result.key_result_id),
        )
        if key_result.target_approval_state is not TargetApprovalState.DRAFT:
            raise ValueError("approved KeyResult cannot be written through proposal action")
        self._repository.upsert_key_result(key_result, authorization_ref=grant.evidence_ref)

    def approve_key_result(self, key_result: KeyResult, grant: StrategicWriteGrant) -> None:
        self._require(
            grant,
            tenant_id=key_result.tenant_id,
            action=StrategicWriteAction.APPROVE,
            resource_ref=key_result_resource_ref(key_result.key_result_id),
        )
        if key_result.target_approval_state is not TargetApprovalState.APPROVED:
            raise ValueError("approval action requires an APPROVED target state")
        self._repository.upsert_key_result(key_result, authorization_ref=grant.evidence_ref)

    def bind_measurement_snapshot(self, binding: SnapshotBindingWrite, grant: StrategicWriteGrant) -> None:
        self._require(
            grant,
            tenant_id=binding.tenant_id,
            action=StrategicWriteAction.REVIEW,
            resource_ref=binding_resource_ref(binding.key_result_id, binding.snapshot_id),
        )
        self._repository.bind_snapshot(binding, authorization_ref=grant.evidence_ref)


__all__ = [
    "ACTION_CAPABILITY",
    "GovernedOkrWriter",
    "OkrWriteRepository",
    "SnapshotBindingWrite",
    "StrategicWriteAction",
    "StrategicWriteGrant",
    "binding_resource_ref",
    "key_result_resource_ref",
    "objective_resource_ref",
]
