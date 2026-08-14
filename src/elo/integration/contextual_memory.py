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

    def ingest_observation(self, payload: dict[str, Any]) -> ContextualIntakeResult:
        observation = str(payload["observation"])
        request = CognitiveRequest(
            request_id=str(payload.get("request_id") or ""),
            correlation_id=payload.get("correlation_id"),
            message=observation,
            session_id=payload.get("session_id"),
            user_id=payload.get("user_id"),
            principal_id=payload.get("principal_id") or payload.get("agent_id"),
            tenant_id=str(payload["tenant_id"]),
            domain=payload.get("domain"),
            context=dict(payload.get("context") or {}),
        )
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
            claim=observation,
            content_ref=str(payload.get("content_ref", observation)),
            quality=str(payload.get("quality", "UNVERIFIED")),
            relevance=float(payload.get("relevance", 0.0)),
            provenance=provenance,
        )
        self.evidence.save(evidence)
        knowledge = KnowledgeItem.create(
            tenant_id=context.tenant_id,
            domain=context.domain,
            title=str(payload.get("title", "Agent observation")),
            content=observation,
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
