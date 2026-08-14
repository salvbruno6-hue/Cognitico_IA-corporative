from elo.core import (
    ConversationEvent,
    ConversationIntake,
    EvolutionMemory,
    KnowledgeAdmission,
)


def event(*, authorized: bool) -> ConversationEvent:
    return ConversationEvent(
        conversation_id="conv-001",
        tenant_id="tenant-a",
        domain="contracts",
        principal="user-a",
        session_id="session-a",
        request_id="request-a",
        correlation_id="corr-a",
        source_type="CHATGPT",
        source_id="chatgpt:conversation:001",
        content="Análise autorizada para retenção evolutiva.",
        authorized=authorized,
        provenance={"provider": "chatgpt", "origin": "authorized-session"},
    )


def test_unauthorized_conversation_is_rejected():
    memory = EvolutionMemory()
    intake = ConversationIntake(KnowledgeAdmission(), memory)

    result = intake.ingest(event(authorized=False))

    assert result.admission.outcome == "REJECT"
    assert result.evolution_id is None
    assert result.temporal_record_id is None
    assert memory.list("tenant-a", "contracts") == []


def test_authorized_conversation_enters_temporal_memory_before_explicit_promotion():
    memory = EvolutionMemory()
    intake = ConversationIntake(KnowledgeAdmission(), memory)

    result = intake.ingest(event(authorized=True))

    assert result.admission.outcome == "OBSERVATION"
    assert result.evolution_id is None
    assert result.temporal_record_id == "temporal:conv-001:request-a"
    assert memory.list("tenant-a", "contracts") == []

    promoted = intake.promote_temporal(
        conversation_id="conv-001",
        evolution_id="conv:conv-001",
        tenant_id="tenant-a",
        domain="contracts",
        source_id="chatgpt:conversation:001",
    )
    assert promoted.evolution_id == "conv:conv-001"
    assert promoted.status == "OBSERVATION"
    assert promoted.provenance["provider"] == "chatgpt"
    assert promoted.provenance["conversation_id"] == "conv-001"


def test_tenant_and_domain_isolation_are_preserved():
    memory = EvolutionMemory()
    intake = ConversationIntake(KnowledgeAdmission(), memory)

    intake.ingest(event(authorized=True))
    intake.promote_temporal(
        conversation_id="conv-001",
        evolution_id="conv:conv-001",
        tenant_id="tenant-a",
        domain="contracts",
        source_id="chatgpt:conversation:001",
    )

    assert len(memory.list("tenant-a", "contracts")) == 1
    assert memory.list("tenant-b", "contracts") == []
    assert memory.list("tenant-a", "finance") == []
