from elo.core.temporal_memory import TemporalConversationMemory


def test_temporal_memory_keeps_provider_response_session_scoped():
    memory = TemporalConversationMemory()
    memory.append(
        conversation_id="c1",
        record_id="r1",
        source_type="CHATGPT",
        content="Multiteiner information from provider",
        provenance={"provider": "gpt", "source": "conversation"},
    )

    records = memory.snapshot("c1")
    assert len(records) == 1
    assert records[0].source_type == "CHATGPT"
    assert records[0].content.startswith("Multiteiner")


def test_temporal_memory_expires_without_promotion():
    memory = TemporalConversationMemory()
    memory.append(
        conversation_id="c2",
        record_id="r2",
        source_type="CHATGPT",
        content="temporary analysis",
        provenance={"provider": "gpt"},
    )

    removed = memory.clear("c2")
    assert len(removed) == 1
    assert memory.snapshot("c2") == ()


def test_temporal_memory_requires_provenance():
    memory = TemporalConversationMemory()
    try:
        memory.append(
            conversation_id="c3",
            record_id="r3",
            source_type="CHATGPT",
            content="x",
            provenance={},
        )
    except ValueError as exc:
        assert "provenance" in str(exc)
    else:
        raise AssertionError("missing provenance must be rejected")
