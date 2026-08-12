from elo.agents import AgentContract, AgentObservation, AgentTask, AutonomyLevel
from elo.agents.orchestrator import AgentExecutionDenied, AgentOrchestrator, ToolContract, ToolRegistry
from elo.agents.registry import AgentRegistry


def make_agent(level=AutonomyLevel.OBSERVE):
    return AgentContract(
        agent_id="finance-agent",
        agent_name="Finance Specialist",
        agent_version="1.0.0",
        tenant_scope="tenant-a",
        domain="finance",
        capabilities=("observation", "analysis"),
        tools=("ledger-read",),
        autonomy_level=level,
    )


def test_registry_is_tenant_scoped():
    registry = AgentRegistry()
    registry.register(make_agent())
    assert registry.get("tenant-a", "finance-agent").domain == "finance"
    try:
        registry.get("tenant-b", "finance-agent")
        assert False
    except KeyError:
        pass


def test_orchestrator_allows_authorized_observation():
    agents = AgentRegistry(); agents.register(make_agent())
    tools = ToolRegistry(); tools.register(ToolContract("ledger-read", "observation", "finance", "tenant-a"))
    orchestrator = AgentOrchestrator(agents, tools)
    task = AgentTask("t1", "finance-agent", "tenant-a", "finance", "inspect", allowed_tools=("ledger-read",), required_output="observation")
    result = orchestrator.dispatch(task, lambda t: AgentObservation("o1", t.agent_id, t.tenant_id, t.domain, "ledger", "ok"))
    assert result.observation == "ok"


def test_orchestrator_blocks_wrong_domain():
    agents = AgentRegistry(); agents.register(make_agent())
    tools = ToolRegistry()
    task = AgentTask("t1", "finance-agent", "tenant-a", "hr", "inspect", required_output="observation")
    try:
        AgentOrchestrator(agents, tools).dispatch(task, lambda t: None)
        assert False
    except AgentExecutionDenied:
        pass


def test_low_autonomy_cannot_execute():
    agents = AgentRegistry(); agents.register(make_agent(AutonomyLevel.RECOMMEND))
    tools = ToolRegistry(); tools.register(ToolContract("ledger-read", "observation", "finance", "tenant-a"))
    task = AgentTask("t1", "finance-agent", "tenant-a", "finance", "act", allowed_tools=("ledger-read",), required_output="observation", constraints={"requires_execution": True})
    try:
        AgentOrchestrator(agents, tools).dispatch(task, lambda t: None)
        assert False
    except AgentExecutionDenied:
        pass


def test_observation_identity_is_verified():
    agents = AgentRegistry(); agents.register(make_agent())
    orchestrator = AgentOrchestrator(agents, ToolRegistry())
    task = AgentTask("t1", "finance-agent", "tenant-a", "finance", "inspect", required_output="observation")
    try:
        orchestrator.dispatch(task, lambda t: AgentObservation("o1", "other-agent", t.tenant_id, t.domain, "x", "bad"))
        assert False
    except AgentExecutionDenied:
        pass
