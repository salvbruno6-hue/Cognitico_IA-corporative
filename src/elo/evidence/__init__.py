"""Evidence contracts and tenant-scoped repository for ELO-002."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Any, Iterable
from uuid import uuid4


class EvidenceAccessError(PermissionError):
    """Raised when evidence is accessed outside its tenant boundary."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    tenant_id: str
    domain: str
    source_type: str
    source_id: str
    claim: str
    content_ref: str
    observed_at: datetime
    quality: str = "UNVERIFIED"
    relevance: float = 0.0
    provenance: dict[str, object] = field(default_factory=dict)
    source_system: str = ""
    source_schema: str = ""
    source_table: str = ""
    source_record_id: str = ""
    source_domain: str = ""
    source_fields: tuple[str, ...] = ()
    value: Any = None
    confidence: str = "unverified"
    absence_type: str | None = None
    query_scope: dict[str, object] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        domain: str,
        source_type: str,
        source_id: str,
        claim: str,
        content_ref: str,
        observed_at: datetime | None = None,
        quality: str = "UNVERIFIED",
        relevance: float = 0.0,
        provenance: dict[str, object] | None = None,
        source_system: str = "",
        source_schema: str = "",
        source_table: str = "",
        source_record_id: str = "",
        source_domain: str = "",
        source_fields: Iterable[str] = (),
        value: Any = None,
        confidence: str = "unverified",
        absence_type: str | None = None,
        query_scope: dict[str, object] | None = None,
    ) -> "Evidence":
        if not tenant_id.strip():
            raise ValueError("tenant_id is required")
        if not domain.strip():
            raise ValueError("domain is required")
        if not claim.strip():
            raise ValueError("claim is required")
        return cls(
            evidence_id=str(uuid4()),
            tenant_id=tenant_id.strip(),
            domain=domain.strip(),
            source_type=source_type.strip(),
            source_id=source_id.strip(),
            claim=claim.strip(),
            content_ref=content_ref.strip(),
            observed_at=observed_at or utc_now(),
            quality=quality,
            relevance=max(0.0, min(1.0, float(relevance))),
            provenance=dict(provenance or {}),
            source_system=source_system.strip(),
            source_schema=source_schema.strip(),
            source_table=source_table.strip(),
            source_record_id=source_record_id.strip(),
            source_domain=source_domain.strip(),
            source_fields=tuple(str(item) for item in source_fields),
            value=value,
            confidence=confidence.strip() or "unverified",
            absence_type=absence_type,
            query_scope=dict(query_scope or {}),
        )

    @classmethod
    def from_forge(
        cls,
        *,
        tenant_id: str,
        source_table: str,
        source_domain: str,
        claim: str,
        source_record_id: str = "",
        source_fields: Iterable[str] = (),
        value: Any = None,
        confidence: str = "observed",
        absence_type: str | None = None,
        query_scope: dict[str, object] | None = None,
    ) -> "Evidence":
        return cls.create(
            tenant_id=tenant_id,
            domain=source_domain,
            source_type="ELO Forge",
            source_id=source_record_id or source_table,
            claim=claim,
            content_ref=f"forge://public/{source_table}/{source_record_id}".rstrip("/"),
            quality="OBSERVED" if confidence == "observed" else "UNVERIFIED",
            relevance=1.0,
            provenance={
                "source": "Supabase Elo-forge",
                "read_only": True,
                "guessed": False,
            },
            source_system="ELO Forge",
            source_schema="public",
            source_table=source_table,
            source_record_id=source_record_id,
            source_domain=source_domain,
            source_fields=source_fields,
            value=value,
            confidence=confidence,
            absence_type=absence_type,
            query_scope=query_scope,
        )


class EvidenceRepository:
    """In-memory evidence adapter with explicit tenant enforcement."""

    def __init__(self) -> None:
        self._items: dict[str, Evidence] = {}
        self._lock = RLock()

    def save(self, evidence: Evidence) -> Evidence:
        with self._lock:
            self._items[evidence.evidence_id] = evidence
        return evidence

    def get(self, evidence_id: str, *, tenant_id: str) -> Evidence | None:
        with self._lock:
            evidence = self._items.get(evidence_id)
            if evidence is None:
                return None
            if evidence.tenant_id != tenant_id:
                raise EvidenceAccessError("evidence does not belong to tenant")
            return evidence

    def list_for_refs(self, evidence_refs: Iterable[str], *, tenant_id: str) -> list[Evidence]:
        return [evidence for ref in evidence_refs if (evidence := self.get(ref, tenant_id=tenant_id)) is not None]


__all__ = ["Evidence", "EvidenceAccessError", "EvidenceRepository"]
