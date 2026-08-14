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


def agent(level=AutonomyLevel.OBSERVE):
    return AgentContract("finance", "1.0", "t1", "finance", ("observe",), ("ledger",), level)


def task(**kw):
    base = dict(
        task_id="x",
        agent_id="finance",
        tenant_id="t1",
        domain="finance",
        objective="inspect",
        required_capability="observe",
    )
    base.update(kw)
    return AgentTask(**base)


def observation(**kw):
    base = dict(
        observation_id="obs-1",
        agent_id="finance",
        tenant_id="t1",
        domain="finance",
        subject="ledger",
        observation="ledger is available",
        confidence=0.9,
    )
    base.update(kw)
    return AgentObservation(**base)


def test_tenant_and_capability_are_required():
    r = AgentRegistry()
    r.register(agent())
    assert r.authorize(task()).agent_id == "finance"
    with pytest.raises(AgentAuthorizationError):
        r.authorize(task(tenant_id="t2"))


def test_domain_and_tool_are_governed():
    r = AgentRegistry()
    r.register(agent())
    tools = ToolRegistry()
    tools.register(ToolContract("ledger", "t1", "finance", "observe"))

    result = AgentOrchestrator(r, tools).dispatch(
        task(allowed_tools=("ledger",)), lambda t: observation()
    )
    assert result.observation_id == "obs-1"

    with pytest.raises(AgentAuthorizationError):
        AgentOrchestrator(r, tools).dispatch(
            task(domain="hr"), lambda t: observation(domain="hr")
        )


def test_executor_observation_identity_is_governed():
    r = AgentRegistry()
    r.register(agent())
    tools = ToolRegistry()

    with pytest.raises(AgentAuthorizationError, match="identity mismatch"):
        AgentOrchestrator(r, tools).dispatch(
            task(), lambda t: observation(agent_id="other-agent")
        )


def test_low_autonomy_cannot_execute():
    r = AgentRegistry()
    r.register(agent(AutonomyLevel.RECOMMEND))
    with pytest.raises(AgentAuthorizationError):
        r.authorize(task(requires_execution=True))
