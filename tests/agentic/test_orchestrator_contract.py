import pytest

from elo.agentic.contracts import IntentSpec
from elo.agentic.orchestrator import KnowledgeOrchestrator, OrchestrationLimits
from elo.observability.cognitive_timing import InMemoryCognitiveTimingSink


class Provider:
    def retrieve(self, intent, requirement):
        from elo.agentic.contracts import KnowledgeCandidate

        return (
            KnowledgeCandidate(
                source_id=f"{requirement.key}-source",
                content=f"evidence for {requirement.key}",
                source_type="TEST",
                status="APPLICABLE",
                relevance=0.9,
                confidence=0.9,
                context_match=1.0,
                provenance={"context": intent.active_context or "none"},
            ),
        )


def test_budget_intent_expands_without_internal_elo_identifiers() -> None:
    orchestrator = KnowledgeOrchestrator(Provider(), OrchestrationLimits(max_requirements=20))
    intent = IntentSpec(
        question="preciso fechar a elétrica externa",
        intent="close_budget",
        domain="orçamento",
        task="fechamento",
        entity="SO 157.26",
        active_context="SO 157.26",
    )

    context = orchestrator.run(intent)

    keys = {candidate.source_id.removesuffix("-source") for candidate in context.candidates}
    assert {"current_requirements", "applicable_composition", "materials", "labor", "calculation_memory", "excesses"} <= keys
    assert all("elo_" not in candidate.source_id for candidate in context.candidates)
    assert all(candidate.provenance["context"] == "SO 157.26" for candidate in context.candidates)


def test_required_missing_knowledge_becomes_blocking_gap() -> None:
    class EmptyProvider:
        def retrieve(self, intent, requirement):
            return ()

    orchestrator = KnowledgeOrchestrator(EmptyProvider())
    intent = IntentSpec(question="x", intent="x", domain="orçamento")

    context = orchestrator.run(intent)

    assert context.gaps
    assert context.requires_human_decision



class _Clock:
    def __init__(self, values):
        self._values = iter(values)

    def __call__(self):
        return next(self._values)


def test_orchestrator_emits_stage_timing_without_changing_context():
    sink = InMemoryCognitiveTimingSink()
    intent = IntentSpec(
        question="qual requisito falta?",
        intent="diagnose",
        domain="planning",
        required_knowledge=("scope",),
        metadata={"correlation_id": "corr-1179"},
    )
    orchestrator = KnowledgeOrchestrator(
        Provider(),
        timing_sink=sink,
        clock=_Clock((0.0, 0.10, 0.15, 0.20, 0.23, 0.30)),
    )

    context = orchestrator.run(intent)

    assert [item.stage for item in sink.observations] == [
        "knowledge.retrieve",
        "knowledge.curate",
        "knowledge.total",
    ]
    retrieval, curation, total = sink.observations
    assert retrieval.requirement_key == "scope"
    assert retrieval.duration_ms == pytest.approx(50.0)
    assert retrieval.candidate_count == 1
    assert curation.duration_ms == pytest.approx(30.0)
    assert total.duration_ms == pytest.approx(300.0)
    assert total.correlation_id == "corr-1179"
    assert total.metadata["requirements"] == "1"
    assert total.metadata["retrieval_calls"] == "1"
    assert len(context.candidates) == 1


def test_observability_failure_never_changes_cognitive_output():
    class BrokenSink:
        def record(self, observation):
            raise RuntimeError("telemetry unavailable")

    intent = IntentSpec(
        question="x",
        intent="x",
        domain="planning",
        required_knowledge=("scope",),
    )
    context = KnowledgeOrchestrator(Provider(), timing_sink=BrokenSink()).run(intent)

    assert len(context.candidates) == 1
    assert context.gaps == ()
