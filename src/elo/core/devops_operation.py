"""Provider-neutral operational lifecycle for governed ELO changes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class DevOpsOperationError(ValueError):
    """Raised when an operational cycle is unsafe or incomplete."""


@dataclass(frozen=True)
class OperationCycle:
    cycle_id: str
    tenant_id: str
    target: str
    change_ref: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    rollback_ref: str
    state: str = "CANDIDATE"


class NativeDevOpsOperation:
    """Model deployment/recovery readiness without owning deployment infrastructure."""

    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    def prepare(self, *, cycle_id: str, tenant_id: str, target: str, change_ref: str,
                evidence_ids: tuple[str, ...] | list[str], provenance: Mapping[str, str],
                rollback_ref: str) -> OperationCycle:
        if any(not str(v).strip() for v in (cycle_id, tenant_id, target, change_ref, rollback_ref)):
            raise DevOpsOperationError("cycle identity, target, change and rollback are required")
        if not evidence_ids:
            raise DevOpsOperationError("operational evidence is required")
        if not provenance.get("source_ref") or not provenance.get("source_commit"):
            raise DevOpsOperationError("provenance requires source_ref and source_commit")
        if any(key.lower() in self._SECRET_KEYS for key in provenance):
            raise DevOpsOperationError("secret-bearing provenance is forbidden")
        return OperationCycle(cycle_id.strip(), tenant_id.strip(), target.strip(), change_ref.strip(),
                              tuple(evidence_ids), dict(provenance), rollback_ref.strip())

    @staticmethod
    def advance(*, cycle: OperationCycle, health_passed: bool, rollback_tested: bool) -> OperationCycle:
        if not health_passed:
            return OperationCycle(**{**cycle.__dict__, "state": "RECOVERY_REQUIRED"})
        if not rollback_tested:
            return OperationCycle(**{**cycle.__dict__, "state": "ROLLBACK_UNVERIFIED"})
        return OperationCycle(**{**cycle.__dict__, "state": "READY_FOR_GOVERNANCE"})
