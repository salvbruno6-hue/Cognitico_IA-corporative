import pytest

from elo.agentic.contracts import IntentSpec, KnowledgeContext
from elo.agentic.graph import GraphRuntimePolicy, build_agentic_graph


class StubOrchestrator:
    def run(self, intent):
        return KnowledgeContext(intent=intent)


def test_graph_requires_intent_interpreter_when_question_only():
    graph = build_agentic_graph(
        StubOrchestrator(),
        intent_interpreter=lambda q: IntentSpec(q, "consult"),
    )
    result = graph.invoke({"question": "preciso fechar a elétrica externa"})
    assert result["intent"].question == "preciso fechar a elétrica externa"
    assert result["trace"] == ("interpret", "retrieve", "ground")
    assert result["grounded"] is False


def test_graph_accepts_prebuilt_intent():
    intent = IntentSpec("x", "consult")
    graph = build_agentic_graph(StubOrchestrator())
    result = graph.invoke({"intent": intent})
    assert result["intent"] == intent
    assert result["trace"] == ("interpret", "retrieve", "ground")


def test_graph_rejects_write_capability():
    with pytest.raises(ValueError, match="read-only"):
        build_agentic_graph(
            StubOrchestrator(),
            policy=GraphRuntimePolicy(allow_writes=True),
        )


def test_graph_rejects_canonical_mutation():
    with pytest.raises(ValueError, match="read-only"):
        build_agentic_graph(
            StubOrchestrator(),
            policy=GraphRuntimePolicy(allow_canonical_mutation=True),
        )


def test_graph_rejects_invalid_step_limit():
    with pytest.raises(ValueError, match="max_steps"):
        build_agentic_graph(
            StubOrchestrator(),
            policy=GraphRuntimePolicy(max_steps=0),
        )


def test_graph_requires_question_when_intent_absent():
    graph = build_agentic_graph(
        StubOrchestrator(),
        intent_interpreter=lambda q: IntentSpec(q, "consult"),
    )
    with pytest.raises(ValueError, match="question or intent"):
        graph.invoke({})
