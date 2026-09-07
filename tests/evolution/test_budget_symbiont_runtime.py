from decimal import Decimal

import pytest

from elo.core.budgeting import BudgetInput, BudgetInputClass, BudgetLine, BudgetLineType, BudgetRequest, GovernedBudgetingService
from elo.core.learning_governance import ExperienceRecord, LearningCandidate
from elo.cognitive.budget_symbiont_runtime import BudgetSymbiontRuntime, EvolutionImpact, IntelligenceRouter, ProviderResult
from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.model_selection import ModelCandidate, ModelSelector
from elo.cognitive.routing.tool_selection import ToolCandidate, ToolSelector
from elo.cognitive.symbionte_lab import SymbiontLabAdapter


class FakeLearning:
    def __init__(self):
        self.captured = 0

    def capture_outcome(self, **kwargs):
        self.captured += 1
        return ExperienceRecord("exp-1", kwargs["tenant_id"], kwargs["domain"], kwargs["decision_id"], kwargs["expected_outcome"], kwargs["observed_outcome"], kwargs["evidence_ids"], 0.0)

    def propose_candidate(self, experience, *, dataset_version, hypothesis):
        return LearningCandidate("cand-1", experience.experience_id, experience.tenant_id, experience.domain, hypothesis, dataset_version, {"experience_id": experience.experience_id})


class Provider:
    def execute(self, *, request, route, context):
        assert route.model_id == "model-budget"
        assert route.tool_id == "tool-budget"
        assert request.tenant_id == "tenant-a"
        assert context == "budget context"
        return ProviderResult("provider-test", route.model_id, "budget result", ("provider-evidence",), {"source_commit": "test-commit", "origin": "test"})


def _runtime():
    learning = FakeLearning()
    return BudgetSymbiontRuntime(
        budgeting=GovernedBudgetingService(),
        execution_router=ExecutionRouter(ModelSelector(), ToolSelector()),
        intelligence_router=IntelligenceRouter(),
        laboratory=SymbiontLabAdapter(learning),
    ), learning


def _request_and_inputs():
    request = BudgetRequest("req-1", "tenant-a", "principal-a", "ORCAMENTO", "2026", "test", "test scope")
    quantity = BudgetInput.create(tenant_id="tenant-a", domain="ORCAMENTO", name="qtd", classification=BudgetInputClass.FACT, value=2, unit="unit", source_id="budget-source", provenance={"source": "fixture"})
    unit_cost = BudgetInput.create(tenant_id="tenant-a", domain="ORCAMENTO", name="unit", classification=BudgetInputClass.FACT, value=Decimal("100"), unit="BRL", source_id="price-source", provenance={"source": "fixture"})
    return request, [quantity, unit_cost], [BudgetLine("line-1", "test", BudgetLineType.COST, quantity.input_id, unit_cost.input_id)]


def _run(runtime):
    request, inputs, lines = _request_and_inputs()
    return runtime.run(
        request=request,
        inputs=inputs,
        lines=lines,
        capability="budget-intelligence",
        models=[ModelCandidate("model-budget", frozenset({"budget-intelligence"}), quality=1, evidence=1)],
        tools=[ToolCandidate("tool-budget", frozenset({"budget-intelligence"}), reliability=1, evidence=1)],
        provider=Provider(),
        context="budget context",
        principal_id="principal-a",
        dataset_version="fixture-v1",
        hypothesis="validated budget execution pattern",
        expected_outcome="useful budget result",
        evolution_impact=EvolutionImpact(baseline_score=0.60, observed_score=0.75, evidence_confidence=0.90, comparative_runs=3),
    )


def test_budget_runtime_requires_material_evolution_and_routes_through_canonical_components():
    runtime, learning = _runtime()
    result = _run(runtime)
    assert result.budget.total_cost == Decimal("200")
    assert result.intelligence.route.model_id == "model-budget"
    assert result.intelligence.route.tool_id == "tool-budget"
    assert result.evolution_impact.delta == pytest.approx(0.15)
    assert result.evolution_impact.material is True
    assert result.laboratory.state == "LAB_ONLY"
    assert result.laboratory.experience is not None
    assert result.laboratory.candidate is not None
    assert learning.captured == 1


def test_budget_runtime_rejects_non_material_evolution_before_execution():
    runtime, learning = _runtime()
    request, inputs, lines = _request_and_inputs()
    with pytest.raises(ValueError, match="material evolution"):
        runtime.run(
            request=request,
            inputs=inputs,
            lines=lines,
            capability="budget-intelligence",
            models=[ModelCandidate("model-budget", frozenset({"budget-intelligence"}), quality=1, evidence=1)],
            tools=[ToolCandidate("tool-budget", frozenset({"budget-intelligence"}), reliability=1, evidence=1)],
            provider=Provider(),
            context="budget context",
            principal_id="principal-a",
            dataset_version="fixture-v1",
            hypothesis="weak change",
            expected_outcome="useful budget result",
            evolution_impact=EvolutionImpact(baseline_score=0.60, observed_score=0.64, evidence_confidence=0.90, comparative_runs=3),
        )
    assert learning.captured == 0


def test_intelligence_router_does_not_select_or_mutate_route():
    route = ExecutionRouter(ModelSelector(), ToolSelector()).route(
        "budget-intelligence",
        models=[ModelCandidate("canonical-model", frozenset({"budget-intelligence"}), quality=1, evidence=1)],
        tools=[ToolCandidate("canonical-tool", frozenset({"budget-intelligence"}), reliability=1, evidence=1)],
    )
    class CanonicalProvider:
        def execute(self, *, request, route, context):
            return ProviderResult("provider-test", route.model_id, "result", ("evidence",), {"source_commit": "test"})

    execution = IntelligenceRouter().execute(
        route=route,
        provider=CanonicalProvider(),
        request=BudgetRequest("req-2", "tenant-a", "principal-a", "ORCAMENTO", "2026", "test", "scope"),
        context="budget context",
    )
    assert execution.route is route
