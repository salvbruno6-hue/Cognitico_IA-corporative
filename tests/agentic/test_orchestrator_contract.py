from elo.agentic.contracts import IntentSpec
from elo.agentic.orchestrator import KnowledgeOrchestrator, OrchestrationLimits


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
