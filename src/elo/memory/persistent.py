"""Governed persistent memory adapter for ELO-007.

SQLite is deliberately used as a deterministic reference adapter. It is not
presented as the canonical vector database or as a second memory authority.
Production deployments may replace the adapter while preserving the contract.
"""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    tenant_id: str
    domain: str
    principal_id: str
    content: str
    source_id: str
    provenance: dict[str, Any]
    created_at: float
    expires_at: float | None = None
    kind: str = "temporal"
    tags: tuple[str, ...] = ()


class MemoryAdmissionError(ValueError):
    """Raised when a memory record fails the governed admission boundary."""


class PersistentMemoryStore:
    """Tenant-isolated persistent memory with deterministic lexical retrieval."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        self._connection = sqlite3.connect(self.path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                domain TEXT NOT NULL,
                principal_id TEXT NOT NULL,
                content TEXT NOT NULL,
                source_id TEXT NOT NULL,
                provenance_json TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL,
                kind TEXT NOT NULL,
                tags_json TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_memories_scope ON memories(tenant_id, domain, created_at)"
        )
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def admit(self, record: MemoryRecord) -> MemoryRecord:
        if not record.tenant_id or not record.domain or not record.principal_id:
            raise MemoryAdmissionError("tenant_id, domain and principal_id are required")
        if not record.source_id or not record.provenance:
            raise MemoryAdmissionError("source_id and provenance are required")
        self._connection.execute(
            """
            INSERT INTO memories
            (memory_id, tenant_id, domain, principal_id, content, source_id,
             provenance_json, created_at, expires_at, kind, tags_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.memory_id,
                record.tenant_id,
                record.domain,
                record.principal_id,
                record.content,
                record.source_id,
                json.dumps(record.provenance, sort_keys=True),
                record.created_at,
                record.expires_at,
                record.kind,
                json.dumps(record.tags),
            ),
        )
        self._connection.commit()
        return record

    def remember(
        self,
        *,
        tenant_id: str,
        domain: str,
        principal_id: str,
        content: str,
        source_id: str,
        provenance: dict[str, Any],
        expires_at: float | None = None,
        kind: str = "temporal",
        tags: Iterable[str] = (),
    ) -> MemoryRecord:
        return self.admit(
            MemoryRecord(
                memory_id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                domain=domain,
                principal_id=principal_id,
                content=content,
                source_id=source_id,
                provenance=dict(provenance),
                created_at=time.time(),
                expires_at=expires_at,
                kind=kind,
                tags=tuple(tags),
            )
        )

    def get(self, memory_id: str, *, tenant_id: str, domain: str) -> MemoryRecord | None:
        row = self._connection.execute(
            "SELECT * FROM memories WHERE memory_id=? AND tenant_id=? AND domain=?",
            (memory_id, tenant_id, domain),
        ).fetchone()
        return self._row_to_record(row) if row else None

    def search(
        self,
        query: str,
        *,
        tenant_id: str,
        domain: str,
        limit: int = 5,
        kind: str | None = None,
    ) -> list[tuple[MemoryRecord, float]]:
        """Return deterministic lexical relevance scores within the caller scope."""
        now = time.time()
        rows = self._connection.execute(
            """
            SELECT * FROM memories
            WHERE tenant_id=? AND domain=?
              AND (expires_at IS NULL OR expires_at > ?)
              AND (? IS NULL OR kind=?)
            ORDER BY created_at DESC
            """,
            (tenant_id, domain, now, kind, kind),
        ).fetchall()
        tokens = {token for token in query.lower().split() if token}
        scored: list[tuple[MemoryRecord, float]] = []
        for row in rows:
            record = self._row_to_record(row)
            corpus = set(record.content.lower().split())
            score = len(tokens & corpus) / max(len(tokens), 1)
            if score > 0:
                scored.append((record, score))
        scored.sort(key=lambda item: (-item[1], -item[0].created_at, item[0].memory_id))
        return scored[: max(0, limit)]

    def purge_expired(self, *, tenant_id: str | None = None) -> int:
        now = time.time()
        if tenant_id is None:
            cursor = self._connection.execute(
                "DELETE FROM memories WHERE expires_at IS NOT NULL AND expires_at <= ?", (now,)
            )
        else:
            cursor = self._connection.execute(
                "DELETE FROM memories WHERE tenant_id=? AND expires_at IS NOT NULL AND expires_at <= ?",
                (tenant_id, now),
            )
        self._connection.commit()
        return cursor.rowcount

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> MemoryRecord:
        return MemoryRecord(
            memory_id=row["memory_id"],
            tenant_id=row["tenant_id"],
            domain=row["domain"],
            principal_id=row["principal_id"],
            content=row["content"],
            source_id=row["source_id"],
            provenance=json.loads(row["provenance_json"]),
            created_at=row["created_at"],
            expires_at=row["expires_at"],
            kind=row["kind"],
            tags=tuple(json.loads(row["tags_json"])),
        )

    def export_record(self, record: MemoryRecord) -> dict[str, Any]:
        """Expose an audit-friendly representation without database internals."""
        return asdict(record)
