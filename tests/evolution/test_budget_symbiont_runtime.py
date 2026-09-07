from decimal import Decimal

from elo.core.budgeting import BudgetInput, BudgetInputClass, BudgetLine, BudgetLineType, BudgetRequest, GovernedBudgetingService
from elo.core.learning_governance import ExperienceRecord, LearningCandidate
from elo.cognitive.budget_symbiont_runtime import BudgetSymbiontRuntime, IntelligenceRouter, ProviderResult
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


def test_budget_runtime_routes_through_execution_router_and_learning_lab():
    learning = FakeLearning()
    runtime = BudgetSymbiontRuntime(
        budgeting=GovernedBudgetingService(),
        execution_router=ExecutionRouter(ModelSelector(), ToolSelector()),
        intelligence_router=IntelligenceRouter(),
        laboratory=SymbiontLabAdapter(learning),
    )
    request = BudgetRequest("req-1", "tenant-a", "principal-a", "ORCAMENTO", "2026", "test", "test scope")
    quantity = BudgetInput.create(tenant_id="tenant-a", domain="ORCAMENTO", name="qtd", classification=BudgetInputClass.FACT, value=2, unit="unit", source_id="budget-source", provenance={"source": "fixture"})
    unit_cost = BudgetInput.create(tenant_id="tenant-a", domain="ORCAMENTO", name="unit", classification=BudgetInputClass.FACT, value=Decimal("100"), unit="BRL", source_id="price-source", provenance={"source": "fixture"})
    line = BudgetLine("line-1", "test", BudgetLineType.COST, quantity.input_id, unit_cost.input_id)
    result = runtime.run(
        request=request,
        inputs=[quantity, unit_cost],
        lines=[line],
        capability="budget-intelligence",
        models=[ModelCandidate("model-budget", frozenset({"budget-intelligence"}), quality=1, evidence=1)],
        tools=[ToolCandidate("tool-budget", frozenset({"budget-intelligence"}), reliability=1, evidence=1)],
        provider=Provider(),
        context="budget context",
        principal_id="principal-a",
        dataset_version="fixture-v1",
        hypothesis="validated budget execution pattern",
        expected_outcome="useful budget result",
    )
    assert result.budget.total_cost == Decimal("200")
    assert result.intelligence.route.model_id == "model-budget"
    assert result.intelligence.route.tool_id == "tool-budget"
    assert result.laboratory.state == "LAB_ONLY"
    assert result.laboratory.experience is not None
    assert result.laboratory.candidate is not None
    assert learning.captured == 1


def test_intelligence_router_does_not_select_or_mutate_route():
    route = ExecutionRouter(ModelSelector(), ToolSelector()).route(
        "budget-intelligence",
        models=[ModelCandidate("canonical-model", frozenset({"budget-intelligence"}), quality=1, evidence=1)],
        tools=[ToolCandidate("canonical-tool", frozenset({"budget-intelligence"}), reliability=1, evidence=1)],
    )
    execution = IntelligenceRouter().execute(
        route=route,
        provider=Provider(),
        request=BudgetRequest("req-2", "tenant-a", "principal-a", "ORCAMENTO", "2026", "test", "scope"),
        context="budget context",
    )
    assert execution.route is route
