"""Governed memory contracts and replaceable repository adapter for ELO."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Iterable, Protocol
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MemoryAccessError(PermissionError):
    """Raised when memory is outside the caller's tenant or policy boundary."""


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    tenant_id: str
    domain: str
    memory_type: str
    content: str
    session_id: str | None = None
    principal_id: str | None = None
    source_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=utc_now)
    expires_at: datetime | None = None
    provenance: dict[str, object] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        domain: str,
        memory_type: str,
        content: str,
        session_id: str | None = None,
        principal_id: str | None = None,
        source_refs: Iterable[str] = (),
        evidence_refs: Iterable[str] = (),
        expires_at: datetime | None = None,
        provenance: dict[str, object] | None = None,
    ) -> "MemoryRecord":
        if not tenant_id.strip():
            raise ValueError("tenant_id is required")
        if not domain.strip():
            raise ValueError("domain is required")
        if not memory_type.strip() or not content.strip():
            raise ValueError("memory_type and content are required")
        return cls(
            memory_id=str(uuid4()),
            tenant_id=tenant_id.strip(),
            domain=domain.strip(),
            memory_type=memory_type.strip(),
            content=content.strip(),
            session_id=session_id,
            principal_id=principal_id,
            source_refs=tuple(source_refs),
            evidence_refs=tuple(evidence_refs),
            expires_at=expires_at,
            provenance=dict(provenance or {}),
        )


class MemoryStore(Protocol):
    def save(self, record: MemoryRecord) -> MemoryRecord: ...
    def get(self, memory_id: str, *, tenant_id: str) -> MemoryRecord | None: ...
    def search(self, query: str, *, tenant_id: str, domain: str | None = None) -> list[MemoryRecord]: ...


class InMemoryMemoryStore:
    """Development adapter; the contract is persistence-ready without requiring a DB."""

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}
        self._lock = RLock()

    def save(self, record: MemoryRecord) -> MemoryRecord:
        with self._lock:
            self._records[record.memory_id] = record
        return record

    def get(self, memory_id: str, *, tenant_id: str) -> MemoryRecord | None:
        with self._lock:
            record = self._records.get(memory_id)
            if record is None:
                return None
            if record.tenant_id != tenant_id:
                raise MemoryAccessError("memory does not belong to tenant")
            return record

    def search(self, query: str, *, tenant_id: str, domain: str | None = None) -> list[MemoryRecord]:
        terms = {term.lower() for term in query.split() if term.strip()}
        with self._lock:
            records = [
                item for item in self._records.values()
                if item.tenant_id == tenant_id and (domain is None or item.domain == domain)
            ]
        if not terms:
            return records
        return [item for item in records if terms.intersection(set((item.memory_type + " " + item.content).lower().split()))]


__all__ = ["MemoryAccessError", "MemoryRecord", "MemoryStore", "InMemoryMemoryStore"]
