"""Canonical knowledge intake and repository contracts for ELO-002."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from threading import RLock
from typing import Iterable
from uuid import uuid4


class KnowledgeAccessError(PermissionError):
    """Raised when a knowledge record is outside the caller tenant/domain policy."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class KnowledgeItem:
    knowledge_id: str
    tenant_id: str
    domain: str
    title: str
    content: str
    knowledge_type: str
    source_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    status: str = "UNVERIFIED"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    provenance: dict[str, object] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        domain: str,
        title: str,
        content: str,
        knowledge_type: str = "OBSERVATION",
        source_refs: Iterable[str] = (),
        evidence_refs: Iterable[str] = (),
        confidence: float = 0.0,
        provenance: dict[str, object] | None = None,
    ) -> "KnowledgeItem":
        if not tenant_id.strip():
            raise ValueError("tenant_id is required")
        if not domain.strip():
            raise ValueError("domain is required")
        if not title.strip() or not content.strip():
            raise ValueError("knowledge title and content are required")
        return cls(
            knowledge_id=str(uuid4()),
            tenant_id=tenant_id.strip(),
            domain=domain.strip(),
            title=title.strip(),
            content=content.strip(),
            knowledge_type=knowledge_type,
            source_refs=tuple(source_refs),
            evidence_refs=tuple(evidence_refs),
            confidence=max(0.0, min(1.0, float(confidence))),
            provenance=dict(provenance or {}),
        )


class KnowledgeRepository:
    """In-memory adapter for development; persistence remains an infrastructure concern."""

    def __init__(self) -> None:
        self._items: dict[str, KnowledgeItem] = {}
        self._lock = RLock()

    def save(self, item: KnowledgeItem) -> KnowledgeItem:
        with self._lock:
            self._items[item.knowledge_id] = item
        return item

    def get(self, knowledge_id: str, *, tenant_id: str) -> KnowledgeItem | None:
        with self._lock:
            item = self._items.get(knowledge_id)
            if item is None:
                return None
            if item.tenant_id != tenant_id:
                raise KnowledgeAccessError("knowledge does not belong to tenant")
            return item

    def search(self, query: str, *, tenant_id: str, domain: str | None = None) -> list[KnowledgeItem]:
        terms = {term.lower() for term in query.split() if term.strip()}
        with self._lock:
            candidates = [item for item in self._items.values() if item.tenant_id == tenant_id and (domain is None or item.domain == domain)]
        if not terms:
            return candidates
        return [item for item in candidates if terms.intersection(set((item.title + " " + item.content).lower().split()))]

    def attach_evidence(self, knowledge_id: str, evidence_refs: Iterable[str], *, tenant_id: str) -> KnowledgeItem:
        current = self.get(knowledge_id, tenant_id=tenant_id)
        if current is None:
            raise KeyError(knowledge_id)
        merged = tuple(dict.fromkeys((*current.evidence_refs, *evidence_refs)))
        updated = replace(current, evidence_refs=merged, updated_at=utc_now())
        return self.save(updated)


__all__ = ["KnowledgeAccessError", "KnowledgeItem", "KnowledgeRepository"]
