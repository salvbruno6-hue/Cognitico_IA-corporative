from elo.agents.runtime import AgentRun, GovernedAgentRuntime, BLOCKED


def make_run():
    return AgentRun(
        run_id="run-1",
        tenant_id="tenant-1",
        principal_id="principal-1",
        request_id="request-1",
        agent_id="agent-1",
    )


def test_allowed_path_executes_and_records_outcome():
    runtime = GovernedAgentRuntime()
    calls = []

    def action(run, reasoning):
        calls.append("action")
        return {"decision": reasoning}

    def record(run, result):
        calls.append("record")
        return run

    result = runtime.execute(
        make_run(),
        select_capabilities=lambda run: ("capability-1",),
        collect_evidence=lambda run: ("evidence-1",),
        reason=lambda run: "reasoned",
        authorize=lambda run, reasoning: True,
        execute_action=action,
        record_outcome=record,
    )

    assert result.capability_ids == ("capability-1",)
    assert result.evidence_ids == ("evidence-1",)
    assert result.authorization_status == "ALLOW"
    assert result.outcome_status == "COMPLETED"
    assert result.response == {"decision": "reasoned"}
    assert calls == ["action", "record"]


def test_missing_evidence_blocks_before_reasoning_or_execution():
    runtime = GovernedAgentRuntime()
    calls = []

    result = runtime.execute(
        make_run(),
        select_capabilities=lambda run: ("capability-1",),
        collect_evidence=lambda run: (),
        reason=lambda run: calls.append("reason"),
        authorize=lambda run, reasoning: calls.append("authorize") or True,
        execute_action=lambda run, reasoning: calls.append("action"),
        record_outcome=lambda run, result: run,
    )

    assert result.outcome_status == BLOCKED
    assert result.authorization_status == "NOT_EVALUATED"
    assert calls == []


def test_denied_authorization_blocks_execution():
    runtime = GovernedAgentRuntime()
    calls = []

    result = runtime.execute(
        make_run(),
        select_capabilities=lambda run: ("capability-1",),
        collect_evidence=lambda run: ("evidence-1",),
        reason=lambda run: "reasoned",
        authorize=lambda run, reasoning: False,
        execute_action=lambda run, reasoning: calls.append("action"),
        record_outcome=lambda run, result: run,
    )

    assert result.authorization_status == "DENY"
    assert result.outcome_status == BLOCKED
    assert calls == []


def test_required_identity_is_enforced():
    runtime = GovernedAgentRuntime()
    invalid = AgentRun(
        run_id="run-1",
        tenant_id="",
        principal_id="principal-1",
        request_id="request-1",
        agent_id="agent-1",
    )

    try:
        runtime.start(invalid)
    except ValueError as exc:
        assert "tenant_id" in str(exc)
    else:
        raise AssertionError("missing tenant_id must be rejected")
