from elo.context import ContextResolver
from elo.evidence import EvidenceRepository
from elo.knowledge import KnowledgeRepository
from elo.memory import InMemoryMemoryStore
from elo.integration.contextual_memory import ContextualMemoryService


def test_agent_observation_becomes_traceable_knowledge_and_memory() -> None:
    service = ContextualMemoryService(
        context_resolver=ContextResolver(),
        knowledge=KnowledgeRepository(),
        evidence=EvidenceRepository(),
        memory=InMemoryMemoryStore(),
    )
    result = service.ingest_observation({
        "tenant_id": "tenant-a",
        "domain": "production",
        "session_id": "session-1",
        "principal_id": "agent-production",
        "request_id": "req-1",
        "correlation_id": "corr-1",
        "agent_id": "agent-production",
        "observation": "forklift maintenance events increased after route changes",
        "confidence": 0.7,
    })

    assert result.context.tenant_id == "tenant-a"
    assert result.evidence.tenant_id == "tenant-a"
    assert result.knowledge.status == "UNVERIFIED"
    assert result.evidence.evidence_id in result.knowledge.evidence_refs
    assert result.knowledge.knowledge_id in result.memory.source_refs
    assert result.evidence.evidence_id in result.memory.evidence_refs
