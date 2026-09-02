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


def test_governed_workflow_runtime_runs_authorized_lifecycle():
    from automation.workflow_contract import GovernedWorkflowRuntime, WorkflowRun

    calls = []

    def build_context(run):
        calls.append("context")
        return {"tenant": run.tenant_id}

    def analyze(run, context):
        calls.append("analyze")
        return {"context": context}

    def decide(run, analysis):
        calls.append("decide")
        return {"approved": True, "analysis": analysis}

    def authorize(run, decision):
        calls.append("authorize")
        return True

    def execute_action(run, decision):
        calls.append("execute")
        return {"ok": True}

    def observe(run, response):
        calls.append("observe")
        return ("evidence-1",)

    def record_outcome(run, response):
        calls.append("record")
        return run.finish("COMPLETED")

    def learn(run, response):
        calls.append("learn")

    result = GovernedWorkflowRuntime().execute(
        WorkflowRun("w", "r", "tenant", "request", "manual"),
        build_context=build_context,
        analyze=analyze,
        decide=decide,
        authorize=authorize,
        execute_action=execute_action,
        observe=observe,
        record_outcome=record_outcome,
        learn=learn,
        capability_ids=("capability-1",),
        action_ids=("action-1",),
    )

    assert result.authorization_status == "ALLOW"
    assert result.outcome_status == "COMPLETED"
    assert result.evidence_ids == ("evidence-1",)
    assert result.capability_ids == ("capability-1",)
    assert calls == ["context", "analyze", "decide", "authorize", "execute", "observe", "record", "learn"]


def test_governed_workflow_runtime_blocks_before_execution_when_denied():
    from automation.workflow_contract import GovernedWorkflowRuntime, WorkflowRun

    executed = []
    result = GovernedWorkflowRuntime().execute(
        WorkflowRun("w", "r", "tenant", "request", "manual"),
        build_context=lambda run: {},
        analyze=lambda run, context: {},
        decide=lambda run, analysis: {},
        authorize=lambda run, decision: False,
        execute_action=lambda run, decision: executed.append(True),
        observe=lambda run, response: (),
        record_outcome=lambda run, response: run.finish("COMPLETED"),
        learn=lambda run, response: None,
    )

    assert result.authorization_status == "DENY"
    assert result.outcome_status == "BLOCKED"
    assert executed == []
