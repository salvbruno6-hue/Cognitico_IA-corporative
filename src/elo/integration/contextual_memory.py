"""Application service connecting context, knowledge, evidence and memory."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.context import ContextResolver, CognitiveContext
from elo.evidence import Evidence, EvidenceRepository
from elo.knowledge import KnowledgeItem, KnowledgeRepository
from elo.memory import MemoryRecord, MemoryStore
from elo.interface.contracts import CognitiveRequest


@dataclass(slots=True)
class ContextualIntakeResult:
    context: CognitiveContext
    evidence: Evidence
    knowledge: KnowledgeItem
    memory: MemoryRecord


class ContextualMemoryService:
    """Coordinates ELO-002 persistence boundaries without owning the Cognitive Core."""

    def __init__(self, *, context_resolver: ContextResolver, knowledge: KnowledgeRepository,
                 evidence: EvidenceRepository, memory: MemoryStore) -> None:
        self.context_resolver = context_resolver
        self.knowledge = knowledge
        self.evidence = evidence
        self.memory = memory

    @staticmethod
    def _to_request(payload: dict[str, Any]) -> CognitiveRequest:
        """Normalize application payloads at the canonical context boundary."""
        return CognitiveRequest(
            request_id=str(payload.get("request_id") or ""),
            correlation_id=str(payload.get("correlation_id") or "") or None,
            message=str(payload["observation"]),
            session_id=str(payload.get("session_id") or "") or None,
            user_id=str(payload.get("user_id") or "") or None,
            principal_id=str(payload.get("principal_id") or "") or None,
            tenant_id=str(payload["tenant_id"]),
            domain=str(payload.get("domain") or "") or None,
            context=dict(payload.get("context") or {}),
        )

    def ingest_observation(self, payload: dict[str, Any]) -> ContextualIntakeResult:
        request = self._to_request(payload)
        context = self.context_resolver.resolve(request)
        provenance = dict(payload.get("provenance") or {})
        provenance.setdefault("request_id", context.request_id)
        provenance.setdefault("correlation_id", context.correlation_id)
        provenance.setdefault("source_type", "agent")
        evidence = Evidence.create(
            tenant_id=context.tenant_id,
            domain=context.domain,
            source_type=str(payload.get("source_type", "agent")),
            source_id=str(payload.get("source_id") or payload.get("agent_id") or "unknown"),
            claim=str(payload["observation"]),
            content_ref=str(payload.get("content_ref", payload["observation"])),
            quality=str(payload.get("quality", "UNVERIFIED")),
            relevance=float(payload.get("relevance", 0.0)),
            provenance=provenance,
        )
        self.evidence.save(evidence)
        knowledge = KnowledgeItem.create(
            tenant_id=context.tenant_id,
            domain=context.domain,
            title=str(payload.get("title", "Agent observation")),
            content=str(payload["observation"]),
            knowledge_type="OBSERVATION",
            source_refs=(evidence.evidence_id,),
            evidence_refs=(evidence.evidence_id,),
            confidence=float(payload.get("confidence", 0.0)),
            provenance=provenance,
        )
        self.knowledge.save(knowledge)
        memory = MemoryRecord.create(
            tenant_id=context.tenant_id,
            domain=context.domain,
            session_id=context.session_id,
            principal_id=context.principal_id,
            memory_type="OBSERVATION",
            content=knowledge.content,
            source_refs=(knowledge.knowledge_id,),
            evidence_refs=(evidence.evidence_id,),
            provenance=provenance,
        )
        self.memory.save(memory)
        return ContextualIntakeResult(context, evidence, knowledge, memory)
