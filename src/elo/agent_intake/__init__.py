"""Governed intake boundary for observations reported by ELO agents/sectors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from elo.evidence import Evidence, EvidenceRepository
from elo.knowledge import KnowledgeItem, KnowledgeRepository
from elo.memory import MemoryRecord, MemoryStore


class AgentIntakeError(ValueError):
    """Raised when a specialist-agent observation is invalid or unauthorized."""


@dataclass(frozen=True, slots=True)
class AgentObservation:
    observation_id: str
    tenant_id: str
    domain: str
    agent_id: str
    subject: str
    observation: str
    confidence: float = 0.0
    evidence_refs: tuple[str, ...] = ()
    questions: tuple[str, ...] = ()
    provenance: dict[str, object] | None = None


@dataclass(frozen=True, slots=True)
class IntakeResult:
    observation: AgentObservation
    knowledge: KnowledgeItem
    memory: MemoryRecord
    evidence: tuple[Evidence, ...]


class AgentIntakeService:
    """Converts specialist reports into traceable candidates, never automatic truth."""

    def __init__(
        self,
        *,
        knowledge: KnowledgeRepository,
        evidence: EvidenceRepository,
        memory: MemoryStore,
    ) -> None:
        self.knowledge = knowledge
        self.evidence = evidence
        self.memory = memory

    def ingest(self, observation: AgentObservation, *, source_evidence: Iterable[Evidence] = ()) -> IntakeResult:
        if not observation.tenant_id.strip():
            raise AgentIntakeError("tenant_id is required")
        if not observation.domain.strip():
            raise AgentIntakeError("domain is required")
        if not observation.agent_id.strip():
            raise AgentIntakeError("agent_id is required")
        if not observation.observation.strip():
            raise AgentIntakeError("observation is required")

        evidence_items = tuple(source_evidence)
        for item in evidence_items:
            if item.tenant_id != observation.tenant_id or item.domain != observation.domain:
                raise AgentIntakeError("evidence does not belong to observation context")
            self.evidence.save(item)

        knowledge = KnowledgeItem.create(
            tenant_id=observation.tenant_id,
            domain=observation.domain,
            title=f"Agent observation: {observation.subject}",
            content=observation.observation,
            knowledge_type="OBSERVATION",
            evidence_refs=observation.evidence_refs,
            confidence=observation.confidence,
            provenance={**(observation.provenance or {}), "agent_id": observation.agent_id, "observation_id": observation.observation_id},
        )
        self.knowledge.save(knowledge)

        memory = MemoryRecord.create(
            tenant_id=observation.tenant_id,
            domain=observation.domain,
            memory_type="OBSERVATION",
            content=observation.observation,
            source_refs=(observation.observation_id, observation.agent_id),
            evidence_refs=observation.evidence_refs,
            provenance={**(observation.provenance or {}), "agent_id": observation.agent_id, "knowledge_id": knowledge.knowledge_id},
        )
        self.memory.save(memory)
        return IntakeResult(observation, knowledge, memory, evidence_items)


__all__ = ["AgentIntakeError", "AgentObservation", "IntakeResult", "AgentIntakeService"]
