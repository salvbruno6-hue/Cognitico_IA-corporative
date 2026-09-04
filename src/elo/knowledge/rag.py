"""Provider-neutral retrieval and RAG context assembly for ELO-007."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.core.assurance import AbstentionDecision
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
    assurance_status: str = "PROCEED"
    assurance_reasons: tuple[str, ...] = ()


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

    @staticmethod
    def _assure_evidence(evidence: tuple[RetrievedEvidence, ...]) -> AbstentionDecision:
        stale = any(item.provenance.get("stale") is True for item in evidence)
        out_of_scope = any(item.provenance.get("out_of_scope") is True for item in evidence)
        conflict = any(item.provenance.get("conflict") is True for item in evidence)
        return AbstentionDecision.decide(
            evidence_count=len(evidence),
            stale=stale,
            out_of_scope=out_of_scope,
            conflict=conflict,
        )

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
        assurance = self._assure_evidence(evidence)
        safe_evidence = evidence if assurance.status == "PROCEED" else ()
        return RAGContext(
            query=query,
            tenant_id=tenant_id,
            domain=domain,
            evidence=safe_evidence,
            citations=tuple(item.evidence_id for item in safe_evidence),
            sufficient=bool(safe_evidence),
            assurance_status=assurance.status,
            assurance_reasons=assurance.reasons,
        )

    @staticmethod
    def prompt_context(context: RAGContext) -> str:
        """Create bounded provider input with explicit evidence boundaries."""
        if context.assurance_status == "ABSTAIN":
            return "ABSTAIN: " + ",".join(context.assurance_reasons)
        if not context.evidence:
            return "NO_VERIFIED_EVIDENCE_AVAILABLE"
        lines = [
            "Use only the following retrieved evidence. Do not treat it as canonical truth without provenance validation.",
        ]
        for item in context.evidence:
            lines.append(f"[{item.evidence_id}] source={item.source_id} relevance={item.relevance:.3f}: {item.content}")
        return "\n".join(lines)
