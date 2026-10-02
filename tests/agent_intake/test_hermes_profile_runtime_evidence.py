from elo.agent_intake.hermes_profile_boundary import ProfileSignal
from elo.agent_intake.hermes_profile_runtime_adapter import dispatch_profile_with_runtime_evidence
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.agents.governance import AgentContract, AgentObservation, AgentRegistry, AgentTask, AutonomyLevel
from elo.agents.orchestrator import AgentOrchestrator, ToolRegistry


def _runtime() -> AgentOrchestrator:
    agents = AgentRegistry()
    agents.register(
        AgentContract(
            agent_id="profile-agent",
            version="1.0",
            tenant_id="tenant-a",
            domain="production",
            capabilities=("profile_execute",),
            autonomy=AutonomyLevel.POLICY_BOUNDED,
        )
    )
    return AgentOrchestrator(agents, ToolRegistry())


def _signal(run: int) -> ProfileSignal:
    return ProfileSignal(
        profile_id=f"profile-{run}",
        tenant_scope="tenant-a",
        source_refs=(f"profile-source-{run}",),
        identity_digest=f"digest-{run}",
        isolated_state=True,
        explicit_activation=True,
        shared_canonical_memory=False,
        authority_transfer=False,
    )


def _task(run: int) -> AgentTask:
    return AgentTask(
        task_id=f"profile-task-{run}",
        agent_id="profile-agent",
        tenant_id="tenant-a",
        domain="production",
        objective="execute within bounded profile context",
        required_capability="profile_execute",
        requires_execution=True,
    )


def _executor(task: AgentTask) -> AgentObservation:
    return AgentObservation(
        observation_id=f"observation-{task.task_id}",
        agent_id=task.agent_id,
        tenant_id=task.tenant_id,
        domain=task.domain,
        subject="profile-task",
        observation="completed within profile context",
        evidence_refs=task.evidence_refs,
        confidence=1.0,
        provenance={"context_refs": task.context_refs},
    )


def test_profile_dispatch_uses_existing_orchestrator_and_binds_profile_context() -> None:
    result = dispatch_profile_with_runtime_evidence(
        _signal(1),
        orchestrator=_runtime(),
        task=_task(1),
        executor=_executor,
        source_commit="abc123",
        runtime_trace="profile-trace-1",
        execution_id="profile-exec-1",
    )

    assert result is not None
    assert result.task.context_refs == ("profile:profile-1", "profile-source-1")
    assert result.observation.tenant_id == "tenant-a"
    assert result.evidence.candidate_id == "EXT-PROFILE-HERMES"
    assert result.evidence.runtime_entrypoint == "AgentOrchestrator.dispatch"
    assert result.evidence.operational_outcome_proven is False


def test_two_profile_dispatches_produce_repeatable_operational_evidence() -> None:
    collector = RuntimeOperationalEvidenceCollector()
    orchestrator = _runtime()

    for run in (1, 2):
        result = dispatch_profile_with_runtime_evidence(
            _signal(run),
            orchestrator=orchestrator,
            task=_task(run),
            executor=_executor,
            source_commit="abc123",
            runtime_trace=f"profile-trace-{run}",
            execution_id=f"profile-exec-{run}",
        )
        assert result is not None
        collector.append(result.evidence)

    groups = collector.ready_groups()
    assert len(groups) == 1
    group = groups[0]
    assert group.candidate_id == "EXT-PROFILE-HERMES"
    assert group.owner == "ELO Agent Context & Delegation"
    assert group.runtime_entrypoint == "AgentOrchestrator.dispatch"
    assert group.repeatable is True

    outcome = group.to_operational_outcome()
    assert outcome.candidate_id == "EXT-PROFILE-HERMES"
    assert outcome.repeatable is True
    assert outcome.production_proven is False
