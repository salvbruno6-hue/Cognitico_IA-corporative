import pytest

from elo.agents.governance import (
    AgentAuthorizationError,
    AgentContract,
    AgentObservation,
    AgentRegistry,
    AgentTask,
    AutonomyLevel,
)
from elo.agents.orchestrator import AgentOrchestrator, ToolContract, ToolRegistry


def make_registry(autonomy=AutonomyLevel.RECOMMEND):
    registry = AgentRegistry()
    registry.register(
        AgentContract(
            agent_id="production-agent",
            version="1.0",
            tenant_id="tenant-a",
            domain="production",
            capabilities=("analyze_maintenance",),
            tools=("maintenance-read",),
            autonomy=autonomy,
        )
    )
    return registry


def make_task(**overrides):
    values = {
        "task_id": "task-1",
        "agent_id": "production-agent",
        "tenant_id": "tenant-a",
        "domain": "production",
        "objective": "analyze maintenance",
        "required_capability": "analyze_maintenance",
        "allowed_tools": ("maintenance-read",),
    }
    values.update(overrides)
    return AgentTask(**values)


def test_agent_authorization_enforces_tenant_domain_capability_and_tool():
    agents = make_registry()
    tools = ToolRegistry()
    tools.register(ToolContract("maintenance-read", "tenant-a", "production", "analyze_maintenance"))
    orchestrator = AgentOrchestrator(agents, tools)

    observation = orchestrator.dispatch(
        make_task(),
        lambda task: AgentObservation(
            observation_id="obs-1",
            agent_id=task.agent_id,
            tenant_id=task.tenant_id,
            domain=task.domain,
            subject="forklift",
            observation="maintenance events increased",
            confidence=0.7,
        ),
    )

    assert observation.observation_id == "obs-1"


def test_cross_tenant_task_is_rejected():
    with pytest.raises(AgentAuthorizationError):
        make_registry().authorize(make_task(tenant_id="tenant-b"))


def test_execution_requires_sufficient_autonomy():
    with pytest.raises(AgentAuthorizationError):
        make_registry(AutonomyLevel.RECOMMEND).authorize(make_task(requires_execution=True))


def test_policy_bounded_agent_can_execute():
    agent = make_registry(AutonomyLevel.POLICY_BOUNDED)
    task = make_task(requires_execution=True)
    assert agent.authorize(task).autonomy == AutonomyLevel.POLICY_BOUNDED


def test_executor_cannot_impersonate_agent_or_tenant():
    agents = make_registry()
    tools = ToolRegistry()
    tools.register(ToolContract("maintenance-read", "tenant-a", "production", "analyze_maintenance"))
    orchestrator = AgentOrchestrator(agents, tools)

    with pytest.raises(AgentAuthorizationError):
        orchestrator.dispatch(
            make_task(),
            lambda task: AgentObservation(
                observation_id="obs-1",
                agent_id="other-agent",
                tenant_id=task.tenant_id,
                domain=task.domain,
                subject="forklift",
                observation="invalid",
            ),
        )
