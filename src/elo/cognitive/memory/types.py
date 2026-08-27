from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class MemoryKind(StrEnum):
    WORKING = "working"
    SESSION = "session"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    EXPERIENCE = "experience"
    CANONICAL = "canonical"
    TENANT = "tenant"


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    id: str
    kind: MemoryKind
    content: str
    tenant_id: str | None
    source: str
    confidence: float
    valid_from: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: datetime | None = None
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.kind is MemoryKind.TENANT and not self.tenant_id:
            raise ValueError("tenant memory requires tenant_id")
        if self.kind is MemoryKind.CANONICAL and self.tenant_id is not None:
            raise ValueError("canonical memory cannot be tenant-scoped")


class InMemoryMemoryStore:
    """Minimal executable store used by tests and early adapters."""

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def put(self, record: MemoryRecord) -> None:
        self._records[record.id] = record

    def get(self, record_id: str) -> MemoryRecord | None:
        return self._records.get(record_id)

    def query(
        self,
        *,
        kind: MemoryKind | None = None,
        tenant_id: str | None = None,
    ) -> list[MemoryRecord]:
        records = list(self._records.values())
        if kind is not None:
            records = [r for r in records if r.kind is kind]
        if tenant_id is not None:
            records = [r for r in records if r.tenant_id == tenant_id]
        return records
