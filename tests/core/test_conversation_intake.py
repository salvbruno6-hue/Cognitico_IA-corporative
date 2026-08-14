from elo.core import ConversationEvent, ConversationIntake, EvolutionMemory, KnowledgeAdmission


def make_event(authorized=True):
    return ConversationEvent(
        conversation_id="conv-001", tenant_id="tenant-a", domain="contracts",
        principal="user-a", session_id="session-a", request_id="request-a",
        correlation_id="corr-a", source_type="CHATGPT", source_id="chatgpt:conversation:001",
        content="authorized conversation", authorized=authorized,
        provenance={"provider": "chatgpt"},
    )


def test_rejected_event_does_not_persist():
    memory = EvolutionMemory()
    intake = ConversationIntake(KnowledgeAdmission(), memory)
    result = intake.ingest(make_event(False))
    assert result.admission.outcome == "REJECT"
    assert result.evolution_id is None
    assert memory.list("tenant-a", "contracts") == []


def test_authorized_event_stays_temporal():
    memory = EvolutionMemory()
    intake = ConversationIntake(KnowledgeAdmission(), memory)
    result = intake.ingest(make_event())
    assert result.admission.outcome == "OBSERVATION"
    assert result.evolution_id is None
    assert result.temporal_record_id == "temporal:conv-001:request-a"
    assert memory.list("tenant-a", "contracts") == []
    assert len(intake.temporal_context("conv-001")) == 1


def test_explicit_promotion_persists_with_scope():
    memory = EvolutionMemory()
    intake = ConversationIntake(KnowledgeAdmission(), memory)
    intake.ingest(make_event())
    record = intake.promote_temporal(
        conversation_id="conv-001", evolution_id="conv:conv-001", tenant_id="tenant-a",
        domain="contracts", source_id="chatgpt:conversation:001",
    )
    assert record.evolution_id == "conv:conv-001"
    assert memory.get("conv:conv-001") is not None
    assert len(memory.list("tenant-a", "contracts")) == 1
    assert memory.list("tenant-b", "contracts") == []
