from decimal import Decimal

import pytest

from elo.agents.governance import AgentAuthorizationError, AgentContract, AgentObservation, AgentRegistry, AgentTask, AutonomyLevel
from elo.agents.orchestrator import AgentOrchestrator, ToolContract, ToolRegistry
from elo.core.budgeting import BudgetInputClass
from elo.core.budgeting_retrieval import retrieved_to_budget_input
from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry
from elo.core.hybrid_bridge import HybridCapabilityBridge
from elo.core.source_resolver import RetrievedSource
from elo.core.diagnostic_scenarios import DiagnosticObservation, DiagnosticScenario, DiagnosticStatus
from elo.core.scenario_gates import MultiScenarioGate


def test_budgeting_retrieval_bridge_preserves_source_and_request_provenance():
    retrieved = RetrievedSource(source_id="source-203", source_type="GITHUB", content="unit cost 25", provenance={"uri": "github://budget/203", "tenant_id": "tenant-a"})
    budget_input = retrieved_to_budget_input(retrieved=retrieved, tenant_id="tenant-a", domain="budgeting", name="unit_cost", classification=BudgetInputClass.FACT, value=Decimal("25"), unit="BRL", request_id="request-203", correlation_id="correlation-203")
    assert budget_input.source_id == "source-203"
    assert budget_input.provenance["uri"] == "github://budget/203"
    assert budget_input.provenance["request_id"] == "request-203"
    assert budget_input.provenance["correlation_id"] == "correlation-203"


def test_unauthorized_execution_is_blocked_before_executor_is_called():
    agents = AgentRegistry()
    tools = ToolRegistry()
    agents.register(AgentContract("agent-1", "1", "tenant-a", "budgeting", ("analyze",), ("tool-1",), AutonomyLevel.RECOMMEND))
    tools.register(ToolContract("tool-1", "tenant-a", "budgeting", "analyze"))
    orchestrator = AgentOrchestrator(agents, tools)
    task = AgentTask("task-1", "agent-1", "tenant-a", "budgeting", "execute commitment", "analyze", ("tool-1",), requires_execution=True)
    called = False

    def executor(_task):
        nonlocal called
        called = True
        return AgentObservation("obs-1", "agent-1", "tenant-a", "budgeting", "x", "should not execute")

    with pytest.raises(AgentAuthorizationError):
        orchestrator.dispatch(task, executor)
    assert called is False


def test_hybrid_provider_failure_degrades_without_claiming_local_capability():
    registry = CapabilityRegistry((CapabilityProbe("LOCAL_AI", "ollama", health_check=lambda: False),))
    selection = HybridCapabilityBridge(registry).select(preferred_kinds=("LOCAL_AI",))
    assert selection.status == "DEGRADED"
    assert selection.capability_name is None


def test_scenario_gate_remains_single_readiness_authority_and_blocks_incomplete_sets():
    observation = DiagnosticObservation("e-210", "capacity", 1.0, "capacity evidence", 0.9)
    scenarios = (DiagnosticScenario("baseline", "compare", observations=(observation,), metadata={"scenario_type": "BASELINE", "metrics": "cost", "metric:cost": "100"}),)
    result = MultiScenarioGate().evaluate(scenarios)
    assert result.status == "BLOCKED"
    assert result.ready_for_reasoning is False
    assert any("missing scenario types" in gap for gap in result.gaps)


def test_conflicting_evidence_cannot_be_promoted_to_scenario_readiness():
    observation = DiagnosticObservation("e-211", "capacity", 1.0, "conflict", 0.9, status=DiagnosticStatus.CONFLICTING)
    scenario = DiagnosticScenario("failure", "compare", observations=(observation,), metadata={"scenario_type": "FAILURE", "metrics": "cost", "metric:cost": "100"})
    result = MultiScenarioGate().evaluate((scenario,))
    assert result.status == "BLOCKED"
    assert any("conflicting evidence" in gap for gap in result.gaps)
