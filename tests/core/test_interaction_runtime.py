from elo.cognitive import CognitiveCore
from elo.interface.contracts import CognitiveRequest
from elo.core.interaction_runtime import build_interaction


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
