from elo.agent_intake.hermes_profile_boundary import ProfileSignal
from elo.agent_intake.hermes_profile_runtime_adapter import execute_profile_with_runtime_evidence
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
            domain="profile",
            capabilities=("execute_profile",),
            autonomy=AutonomyLevel.POLICY_BOUNDED,
        )
    )
    return AgentOrchestrator(agents, ToolRegistry())


def _signal(run: int) -> ProfileSignal:
    return ProfileSignal(
        profile_id=f"profile-{run}",
        tenant_scope="tenant-a",
        source_refs=(f"profile-context:{run}",),
        identity_digest=f"digest-{run}",
        isolated_state=True,
        explicit_activation=True,
        shared_canonical_memory=False,
        authority_transfer=False,
    )


def _executor(task: AgentTask) -> AgentObservation:
    return AgentObservation(
        observation_id=f"observation-{task.task_id}",
        agent_id=task.agent_id,
        tenant_id=task.tenant_id,
        domain=task.domain,
        subject=task.objective,
        observation="profile task completed in bounded context",
        evidence_refs=task.evidence_refs,
        confidence=1.0,
        provenance={
            "profile_id": task.objective.rsplit(":", 1)[-1],
            "identity_digest": f"digest-{task.task_id.split(':')[0].split('-')[-1]}",
            "context_refs": task.context_refs,
        },
    )


def test_real_orchestrator_dispatch_records_one_profile_runtime_observation() -> None:
    result = execute_profile_with_runtime_evidence(
        _signal(1),
        orchestrator=_runtime(),
        agent_id="profile-agent",
        required_capability="execute_profile",
        domain="profile",
        executor=_executor,
        source_commit="abc123",
        runtime_trace="profile-trace-1",
        execution_id="profile-exec-1",
    )

    assert result is not None
    assert result.task.context_refs == ("profile-context:1",)
    assert result.observation.agent_id == "profile-agent"
    assert result.evidence.runtime_entrypoint == "AgentOrchestrator.dispatch"
    assert result.evidence.operational_outcome_proven is False


def test_two_real_profile_dispatches_become_operational_outcome() -> None:
    collector = RuntimeOperationalEvidenceCollector()
    orchestrator = _runtime()

    for run in (1, 2):
        result = execute_profile_with_runtime_evidence(
            _signal(run),
            orchestrator=orchestrator,
            agent_id="profile-agent",
            required_capability="execute_profile",
            domain="profile",
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
    assert group.repeatable is True

    outcome = group.to_operational_outcome()
    assert outcome is not None
    assert outcome.candidate_id == "EXT-PROFILE-HERMES"
    assert outcome.production_proven is False
    assert outcome.repeatable is True
