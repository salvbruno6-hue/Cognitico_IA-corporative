"""Bounded organizational-intelligence member for ELO.

This module deliberately owns structural assertions only. Global reasoning,
memory, provider orchestration and decision authority remain in the ELO core.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable


class ResultStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    CONFLICTING = "CONFLICTING"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class StructuralAssertion:
    assertion_id: str
    tenant_id: str
    source_domain: str
    target_domain: str
    relation: str
    source_id: str
    target_id: str
    provenance: str
    owner: str
    status: str = "ACTIVE"
    valid_from: datetime | None = None
    valid_to: datetime | None = None

    def is_valid_at(self, at: datetime | None) -> bool:
        if at is None:
            return True
        if self.valid_from is not None and at < self.valid_from:
            return False
        if self.valid_to is not None and at >= self.valid_to:
            return False
        return True


@dataclass(frozen=True, slots=True)
class MemberResult:
    status: ResultStatus
    member_id: str
    member_version: str
    tenant_id: str
    scope: str
    evidence_refs: tuple[str, ...]
    assertions: tuple[StructuralAssertion, ...]
    confidence: float | None = None
    reason: str | None = None


class ELOOrgMember:
    """First bounded ELO member for organizational structure."""

    member_id = "ELO-ORG"
    version = "1.0.0"
    capabilities = frozenset(
        {
            "organizational_structure",
            "taxonomy",
            "process_module_relationships",
            "specialist_responsibility",
            "dependency_mapping",
            "management_views",
        }
    )

    def __init__(self, assertions: Iterable[StructuralAssertion] = ()) -> None:
        self._assertions = tuple(assertions)

    def _result(
        self,
        status: ResultStatus,
        tenant_id: str,
        scope: str,
        assertions: tuple[StructuralAssertion, ...] = (),
        evidence_refs: tuple[str, ...] = (),
        reason: str | None = None,
        confidence: float | None = None,
    ) -> MemberResult:
        return MemberResult(
            status=status,
            member_id=self.member_id,
            member_version=self.version,
            tenant_id=tenant_id,
            scope=scope,
            evidence_refs=evidence_refs,
            assertions=assertions,
            confidence=confidence,
            reason=reason,
        )

    def query(
        self,
        *,
        tenant_id: str,
        source_domain: str,
        target_domain: str,
        relation: str,
        at: datetime | None = None,
    ) -> MemberResult:
        """Return only authorized, provenanced assertions for a scoped query."""
        if not tenant_id or not source_domain or not target_domain or not relation:
            return self._result(
                ResultStatus.BLOCKED,
                tenant_id,
                f"{source_domain}->{target_domain}",
                reason="scope and relation are mandatory",
            )

        scope = f"{source_domain}->{target_domain}"
        matches = tuple(
            a
            for a in self._assertions
            if a.tenant_id == tenant_id
            and a.source_domain == source_domain
            and a.target_domain == target_domain
            and a.relation == relation
            and a.is_valid_at(at)
        )

        if not matches:
            return self._result(
                ResultStatus.INCONCLUSIVE,
                tenant_id,
                scope,
                reason="no valid structural assertion found",
            )

        if any(not a.provenance for a in matches):
            return self._result(
                ResultStatus.BLOCKED,
                tenant_id,
                scope,
                reason="structural assertion without provenance",
            )

        unique_targets = {(a.source_id, a.target_id) for a in matches}
        if len(unique_targets) > 1:
            return self._result(
                ResultStatus.CONFLICTING,
                tenant_id,
                scope,
                assertions=matches,
                evidence_refs=tuple(a.provenance for a in matches),
                reason="material structural assertions conflict",
            )

        return self._result(
            ResultStatus.SUPPORTED,
            tenant_id,
            scope,
            assertions=matches,
            evidence_refs=tuple(a.provenance for a in matches),
            confidence=1.0,
        )

    def health(self) -> dict[str, str]:
        return {"member_id": self.member_id, "version": self.version, "status": "ACTIVE"}
