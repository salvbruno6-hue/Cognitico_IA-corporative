from pathlib import Path


def test_improvement_contracts_exist():
    root = Path(__file__).resolve().parents[1]
    required = (
        root / "src/elo/agents/runtime.py",
        root / "automation/workflow_contract.py",
        root / "12-system-engineering/ELO_INTEGRATION_EVALUATION_MATRIX.md",
        root / "frontend/ELO_CORPORATE_WORKSPACE_CONTRACT.md",
        root / "docs/governance/ELO_EVOLUTION_DASHBOARD_CONTRACT.md",
        root / "docs/governance/ELO_IMPROVEMENT_BLOCK_REGISTRY.yaml",
    )
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"missing ELO improvement artifacts: {missing}"


def test_agent_runtime_requires_tenant_principal_and_request():
    from elo.agents.runtime import AgentRun, GovernedAgentRuntime

    runtime = GovernedAgentRuntime()
    try:
        runtime.start(AgentRun("r", "", "p", "q", "agent"))
    except ValueError:
        pass
    else:
        raise AssertionError("agent runtime accepted an incomplete trust envelope")


def test_workflow_contract_rejects_unknown_terminal_state():
    from automation.workflow_contract import WorkflowRun

    run = WorkflowRun("w", "r", "tenant", "request", "manual")
    try:
        run.finish("UNKNOWN")
    except ValueError:
        pass
    else:
        raise AssertionError("workflow contract accepted an unknown terminal state")
