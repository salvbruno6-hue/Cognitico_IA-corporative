from datetime import datetime, timezone

import pytest

from elo.agent_intake import AgentIntakeError, AgentIntakeService, AgentObservation
from elo.evidence import Evidence, EvidenceAccessError, EvidenceRepository
from elo.knowledge import KnowledgeRepository
from elo.memory import InMemoryMemoryStore, MemoryAccessError, MemoryRecord


def build_service():
    return AgentIntakeService(
        knowledge=KnowledgeRepository(),
        evidence=EvidenceRepository(),
        memory=InMemoryMemoryStore(),
    )


def test_memory_is_persistable_by_contract_and_tenant_scoped():
    store = InMemoryMemoryStore()
    record = MemoryRecord.create(
        tenant_id="tenant-a",
        domain="finance",
        memory_type="EXPERIENCE",
        content="A validated operational lesson.",
        provenance={"source": "agent-finance"},
    )
    store.save(record)
    assert store.get(record.memory_id, tenant_id="tenant-a") == record
    with pytest.raises(MemoryAccessError):
        store.get(record.memory_id, tenant_id="tenant-b")


def test_agent_observation_creates_traceable_knowledge_memory_and_evidence():
    service = build_service()
    evidence = Evidence.create(
        tenant_id="tenant-a",
        domain="operations",
        source_type="system",
        source_id="maintenance-42",
        claim="Maintenance cost increased.",
        content_ref="maintenance-42",
        observed_at=datetime.now(timezone.utc),
        relevance=0.9,
        provenance={"request_id": "req-1"},
    )
    observation = AgentObservation(
        observation_id="obs-1",
        tenant_id="tenant-a",
        domain="operations",
        agent_id="maintenance-agent",
        subject="forklift maintenance",
        observation="Maintenance cost increased after repeated operation on uneven flooring.",
        confidence=0.7,
        evidence_refs=(evidence.evidence_id,),
        provenance={"request_id": "req-1"},
    )

    result = service.ingest(observation, source_evidence=(evidence,))

    assert result.knowledge.status == "UNVERIFIED"
    assert result.knowledge.evidence_refs == (evidence.evidence_id,)
    assert result.memory.evidence_refs == (evidence.evidence_id,)
    assert result.knowledge.provenance["agent_id"] == "maintenance-agent"
    assert result.memory.provenance["knowledge_id"] == result.knowledge.knowledge_id


def test_agent_cannot_intake_cross_tenant_evidence():
    service = build_service()
    evidence = Evidence.create(
        tenant_id="tenant-b",
        domain="operations",
        source_type="system",
        source_id="system-b",
        claim="Private tenant B observation.",
        content_ref="private-b",
    )
    observation = AgentObservation(
        observation_id="obs-a",
        tenant_id="tenant-a",
        domain="operations",
        agent_id="agent-a",
        subject="restricted",
        observation="Attempted cross-tenant intake.",
    )

    with pytest.raises(AgentIntakeError):
        service.ingest(observation, source_evidence=(evidence,))


def test_evidence_repository_rejects_cross_tenant_read():
    repository = EvidenceRepository()
    evidence = Evidence.create(
        tenant_id="tenant-a",
        domain="finance",
        source_type="erp",
        source_id="erp-1",
        claim="Invoice discrepancy exists.",
        content_ref="invoice-1",
    )
    repository.save(evidence)
    with pytest.raises(EvidenceAccessError):
        repository.get(evidence.evidence_id, tenant_id="tenant-b")
