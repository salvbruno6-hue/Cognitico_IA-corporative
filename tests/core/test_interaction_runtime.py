from elo.cognitive import CognitiveCore
from elo.interface.contracts import CognitiveRequest
from elo.core.interaction_runtime import build_interaction
from elo.core.temporal_memory import TemporalConversationMemory


def test_runtime_connects_mature_posture_to_response() -> None:
    result = build_interaction(
        "Preciso decidir qual caminho seguir.",
        context={"decision_relevance": 0.8},
    )

    assert result.posture.value == "ANALYZE"
    assert result.next_step
    assert result.metadata["interaction_mode"] == "mature_contextual"


def test_runtime_investigates_when_evidence_is_missing() -> None:
    result = build_interaction(
        "Investigue porque ainda não tenho dados.",
        context={"evidence_gap": 0.8},
    )

    assert result.posture.value == "INVESTIGATE"
    assert "verificado" in result.next_step.lower()


def test_cognitive_core_exposes_interaction_behavior() -> None:
    request = CognitiveRequest(
        message="O que devo verificar antes de decidir?",
        tenant_id="tenant-test",
        context={"decision_relevance": 0.8},
    )

    result = CognitiveCore().process(request)

    assert result["response"]["posture"] == "ANALYZE"
    assert result["response"]["next_step"]
    assert result["interaction"]["interaction_mode"] == "mature_contextual"
    assert "Entendi" in result["response"]["content"]


def test_authorized_session_reuses_temporal_context() -> None:
    memory = TemporalConversationMemory()
    core = CognitiveCore(temporal_memory=memory)

    first = CognitiveRequest(
        message="Estamos avaliando o contrato de fornecimento.",
        tenant_id="tenant-test",
        session_id="session-1",
        context={"conversation_authorized": True},
    )
    second = CognitiveRequest(
        message="E agora, o que devo verificar?",
        tenant_id="tenant-test",
        session_id="session-1",
        context={"conversation_authorized": True},
    )

    core.process(first)
    result = core.process(second)

    assert result["interaction"]["continuity"] is True
    assert result["interaction"]["prior_context_records"] == 1
    assert len(memory.snapshot("session-1")) == 2


def test_unauthorized_session_does_not_enter_temporal_context() -> None:
    memory = TemporalConversationMemory()
    core = CognitiveCore(temporal_memory=memory)

    request = CognitiveRequest(
        message="Não deve ser retido como contexto.",
        tenant_id="tenant-test",
        session_id="session-unauthorized",
        context={"conversation_authorized": False},
    )

    result = core.process(request)

    assert result["interaction"]["continuity"] is False
    assert memory.snapshot("session-unauthorized") == ()
