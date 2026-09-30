from automation.workflow_contract import GovernedWorkflowRuntime
from elo.agent_intake.hermes_cron_boundary import ScheduleSignal
from elo.agent_intake.hermes_cron_runtime_adapter import execute_schedule_with_runtime_evidence
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector


def _signal(run: int) -> ScheduleSignal:
    return ScheduleSignal(
        schedule_id=f"schedule-{run}",
        tenant_scope="tenant-a",
        task_digest="task-digest",
        source_refs=(f"controlled-runtime:cron/{run}",),
        schedule_expression="0 8 * * *",
        owner_principal="elo",
        provenance_verified=True,
        explicit_authorization=True,
        idempotent=True,
        governance_bypass=False,
    )


def _executor(contract) -> object:
    return {
        "schedule_id": contract.schedule_id,
        "idempotency_key": contract.idempotency_key,
        "idempotency_collision_free": True,
    }


def test_cron_schedule_executes_through_governed_runtime_and_records_evidence():
    result = execute_schedule_with_runtime_evidence(
        _signal(1),
        runtime=GovernedWorkflowRuntime(),
        executor=_executor,
        source_commit="cron-test-commit",
        runtime_trace="cron-runtime-trace-1",
        execution_id="cron-exec-1",
    )

    assert result is not None
    assert result.run.outcome_status == "COMPLETED"
    assert result.run.authorization_status == "ALLOW"
    assert result.evidence.candidate_id == "EXT-CRON-HERMES"
    assert result.evidence.runtime_entrypoint == "GovernedWorkflowRuntime.execute"
    assert result.evidence.action_observed is True
    assert result.evidence.operational_outcome_proven is False


def test_two_cron_runtime_executions_become_operational_outcome():
    collector = RuntimeOperationalEvidenceCollector()
    runtime = GovernedWorkflowRuntime()

    for run in (1, 2):
        result = execute_schedule_with_runtime_evidence(
            _signal(run),
            runtime=runtime,
            executor=_executor,
            source_commit="cron-test-commit",
            runtime_trace=f"cron-runtime-trace-{run}",
            execution_id=f"cron-exec-{run}",
        )
        assert result is not None
        collector.append(result.evidence)

    groups = collector.ready_groups()
    assert len(groups) == 1
    group = groups[0]
    assert group.candidate_id == "EXT-CRON-HERMES"
    assert group.owner == "ELO Workflow/Automation"
    assert group.runtime_entrypoint == "GovernedWorkflowRuntime.execute"
    assert group.repeatable is True

    outcome = group.to_operational_outcome()
    assert outcome.candidate_id == "EXT-CRON-HERMES"
    assert outcome.repeatable is True
    assert outcome.production_proven is False


def test_cron_without_explicit_authorization_is_blocked():
    signal = ScheduleSignal(
        schedule_id="schedule-blocked",
        tenant_scope="tenant-a",
        task_digest="task-digest",
        source_refs=("controlled-runtime:cron/blocked",),
        schedule_expression="0 8 * * *",
        owner_principal="elo",
        provenance_verified=True,
        explicit_authorization=False,
        idempotent=True,
        governance_bypass=False,
    )

    result = execute_schedule_with_runtime_evidence(
        signal,
        runtime=GovernedWorkflowRuntime(),
        executor=_executor,
        source_commit="cron-test-commit",
        runtime_trace="cron-runtime-trace-blocked",
        execution_id="cron-exec-blocked",
    )

    assert result is not None
    assert result.run.authorization_status == "DENY"
    assert result.run.outcome_status == "BLOCKED"
