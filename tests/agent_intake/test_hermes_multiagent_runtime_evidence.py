from elo.agent_intake.hermes_multiagent_adapter import dispatch_delegation_with_runtime_evidence
from elo.agent_intake.hermes_multiagent_boundary import DelegationSignal
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.agents.governance import AgentContract, AgentObservation, AgentRegistry, AgentTask, AutonomyLevel
from elo.agents.orchestrator import AgentOrchestrator, ToolRegistry


def _runtime() -> AgentOrchestrator:
    agents = AgentRegistry()
    agents.register(
        AgentContract(
            agent_id="parent-agent",
            version="1.0",
            tenant_id="tenant-a",
            domain="production",
            capabilities=("delegate",),
            autonomy=AutonomyLevel.POLICY_BOUNDED,
        )
    )
    agents.register(
        AgentContract(
            agent_id="child-agent",
            version="1.0",
            tenant_id="tenant-a",
            domain="production",
            capabilities=("execute_child",),
            autonomy=AutonomyLevel.POLICY_BOUNDED,
        )
    )
    return AgentOrchestrator(agents, ToolRegistry())


def _parent_task() -> AgentTask:
    return AgentTask(
        task_id="parent-task",
        agent_id="parent-agent",
        tenant_id="tenant-a",
        domain="production",
        objective="delegate bounded work",
        required_capability="delegate",
        policy="default",
    )


def _signal(run: int) -> DelegationSignal:
    return DelegationSignal(
        delegation_id=f"delegation-{run}",
        tenant_scope="tenant-a",
        parent_agent_id="parent-agent",
        child_agent_id="child-agent",
        goal_digest="goal-digest",
        source_refs=("source-1",),
        resource_scope=("context:child", "resource:bounded"),
        provenance_verified=True,
        isolated_context=True,
        delegation_depth=1,
        max_child_concurrency=2,
        heartbeat_ref=f"heartbeat-{run}",
    )


def _executor(task: AgentTask) -> AgentObservation:
    return AgentObservation(
        observation_id=f"observation-{task.task_id}",
        agent_id=task.agent_id,
        tenant_id=task.tenant_id,
        domain=task.domain,
        subject="delegated-task",
        observation="completed within delegated context",
        evidence_refs=task.evidence_refs,
        confidence=1.0,
        provenance={"context_refs": task.context_refs},
    )


def test_real_orchestrator_dispatch_records_one_multiagent_runtime_observation() -> None:
    result = dispatch_delegation_with_runtime_evidence(
        _signal(1),
        orchestrator=_runtime(),
        parent_task=_parent_task(),
        child_required_capability="execute_child",
        executor=_executor,
        source_commit="abc123",
        runtime_trace="multiagent-trace-1",
        execution_id="multiagent-exec-1",
    )

    assert result is not None
    assert result.child_task.agent_id == "child-agent"
    assert result.child_task.context_refs == ("context:child", "resource:bounded")
    assert result.observation.agent_id == "child-agent"
    assert result.evidence.runtime_entrypoint == "AgentOrchestrator.dispatch"
    assert result.evidence.operational_outcome_proven is False


def test_two_real_multiagent_dispatches_become_operational_outcome() -> None:
    collector = RuntimeOperationalEvidenceCollector()
    orchestrator = _runtime()

    for run in (1, 2):
        result = dispatch_delegation_with_runtime_evidence(
            _signal(run),
            orchestrator=orchestrator,
            parent_task=_parent_task(),
            child_required_capability="execute_child",
            executor=_executor,
            source_commit="abc123",
            runtime_trace=f"multiagent-trace-{run}",
            execution_id=f"multiagent-exec-{run}",
        )
        assert result is not None
        collector.append(result.evidence)

    groups = collector.ready_groups()
    assert len(groups) == 1
    group = groups[0]
    assert group.candidate_id == "EXT-MULTIAGENT-HERMES"
    assert group.repeatable is True

    outcome = group.to_operational_outcome()
    assert outcome is not None
    assert outcome.candidate_id == "EXT-MULTIAGENT-HERMES"
    assert outcome.production_proven is False
    assert outcome.repeatable is True


def test_delegation_controls_are_carried_into_runtime_contract() -> None:
    result = dispatch_delegation_with_runtime_evidence(
        _signal(3),
        orchestrator=_runtime(),
        parent_task=_parent_task(),
        child_required_capability="execute_child",
        executor=_executor,
        source_commit="abc123",
        runtime_trace="multiagent-trace-3",
        execution_id="multiagent-exec-3",
    )

    assert result is not None
    assert result.work_item.delegation_depth == 1
    assert result.work_item.max_child_concurrency == 2
    assert result.work_item.heartbeat_ref == "heartbeat-3"


def test_delegation_without_heartbeat_is_fail_closed() -> None:
    signal = DelegationSignal(
        delegation_id="delegation-no-heartbeat",
        tenant_scope="tenant-a",
        parent_agent_id="parent-agent",
        child_agent_id="child-agent",
        goal_digest="goal-digest",
        source_refs=("source-1",),
        resource_scope=("context:child",),
        provenance_verified=True,
        isolated_context=True,
        delegation_depth=1,
        max_child_concurrency=1,
        heartbeat_ref=None,
    )
    result = dispatch_delegation_with_runtime_evidence(
        signal,
        orchestrator=_runtime(),
        parent_task=_parent_task(),
        child_required_capability="execute_child",
        executor=_executor,
        source_commit="abc123",
        runtime_trace="multiagent-trace-no-heartbeat",
        execution_id="multiagent-exec-no-heartbeat",
    )
    assert result is None


def test_delegation_depth_and_concurrency_limits_are_fail_closed() -> None:
    for depth, concurrency in ((3, 1), (1, 5)):
        signal = DelegationSignal(
            delegation_id=f"delegation-invalid-{depth}-{concurrency}",
            tenant_scope="tenant-a",
            parent_agent_id="parent-agent",
            child_agent_id="child-agent",
            goal_digest="goal-digest",
            source_refs=("source-1",),
            resource_scope=("context:child",),
            provenance_verified=True,
            isolated_context=True,
            delegation_depth=depth,
            max_child_concurrency=concurrency,
            heartbeat_ref="heartbeat-invalid",
        )
        assert dispatch_delegation_with_runtime_evidence(
            signal,
            orchestrator=_runtime(),
            parent_task=_parent_task(),
            child_required_capability="execute_child",
            executor=_executor,
            source_commit="abc123",
            runtime_trace="multiagent-trace-invalid",
            execution_id=f"multiagent-exec-invalid-{depth}-{concurrency}",
        ) is None
