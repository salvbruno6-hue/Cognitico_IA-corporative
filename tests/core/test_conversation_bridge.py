import json

import pytest

from elo.core import EvolutionMemory, KnowledgeAdmission
from elo.core.conversation_bridge import ChatBridge, ChatBridgeEvent
from elo.core.conversation_intake import ConversationIntake


def _event(**overrides):
    data = {
        "conversation_id": "conv-001",
        "tenant_id": "tenant-001",
        "domain": "elo",
        "principal": "user-001",
        "session_id": "session-001",
        "request_id": "request-001",
        "correlation_id": "corr-001",
        "source_id": "chat-001",
        "content": "Discussed a candidate architecture.",
        "authorized": True,
        "provenance": {"source": "chatgpt", "channel": "conversation"},
    }
    data.update(overrides)
    return ChatBridgeEvent(**data)


def test_bridge_serializes_and_ingests_authorized_event_without_implicit_promotion():
    memory = EvolutionMemory()
    bridge = ChatBridge(ConversationIntake(KnowledgeAdmission(), memory))

    event = _event()
    restored = ChatBridgeEvent.from_json(event.to_json())
    result = bridge.ingest(restored)

    assert result.evolution_id is None
    assert result.temporal_record_id == "temporal:conv-001:request-001"
    assert memory.get("conv:conv-001") is None


def test_bridge_rejects_unauthorized_event():
    with pytest.raises(PermissionError):
        _event(authorized=False).validate()


def test_bridge_requires_provenance():
    with pytest.raises(ValueError, match="provenance"):
        _event(provenance={}).validate()


def test_bridge_json_is_deterministic_and_parseable():
    payload = json.loads(_event().to_json())
    assert payload["schema_version"] == "1.1"
    assert payload["source_type"] == "CHATGPT"
    assert payload["event_role"] == "CONVERSATION"
