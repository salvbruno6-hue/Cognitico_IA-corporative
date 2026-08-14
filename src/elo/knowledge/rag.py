"""Provider-neutral retrieval and RAG context assembly for ELO-007."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.memory.persistent import MemoryRecord, PersistentMemoryStore


@dataclass(frozen=True)
class RetrievedEvidence:
    evidence_id: str
    source_id: str
    memory_id: str
    content: str
    relevance: float
    provenance: dict[str, Any]


@dataclass(frozen=True)
class RAGContext:
    query: str
    tenant_id: str
    domain: str
    evidence: tuple[RetrievedEvidence, ...]
    citations: tuple[str, ...]
    sufficient: bool


class GovernedRetriever:
    """Retrieves scoped evidence; it never generates canonical truth."""

    def __init__(self, memory: PersistentMemoryStore) -> None:
        self.memory = memory

    def retrieve(
        self,
        query: str,
        *,
        tenant_id: str,
        domain: str,
        limit: int = 5,
        kind: str | None = None,
    ) -> list[RetrievedEvidence]:
        return [
            RetrievedEvidence(
                evidence_id=record.memory_id,
                source_id=record.source_id,
                memory_id=record.memory_id,
                content=record.content,
                relevance=score,
                provenance=dict(record.provenance),
            )
            for record, score in self.memory.search(
                query, tenant_id=tenant_id, domain=domain, limit=limit, kind=kind
            )
        ]

    def build_context(
        self,
        query: str,
        *,
        tenant_id: str,
        domain: str,
        limit: int = 5,
        minimum_relevance: float = 0.0,
    ) -> RAGContext:
        evidence = tuple(
            item
            for item in self.retrieve(
                query, tenant_id=tenant_id, domain=domain, limit=limit
            )
            if item.relevance >= minimum_relevance
        )
        return RAGContext(
            query=query,
            tenant_id=tenant_id,
            domain=domain,
            evidence=evidence,
            citations=tuple(item.evidence_id for item in evidence),
            sufficient=bool(evidence),
        )

    @staticmethod
    def prompt_context(context: RAGContext) -> str:
        """Create bounded provider input with explicit evidence boundaries."""
        if not context.evidence:
            return "NO_VERIFIED_EVIDENCE_AVAILABLE"
        lines = [
            "Use only the following retrieved evidence. Do not treat it as canonical truth without provenance validation.",
        ]
        for item in context.evidence:
            lines.append(f"[{item.evidence_id}] source={item.source_id} relevance={item.relevance:.3f}: {item.content}")
        return "\n".join(lines)
