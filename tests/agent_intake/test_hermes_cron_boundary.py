from src.elo.agent_intake.hermes_cron_boundary import (
    ScheduleSignal, ScheduleDisposition, assess_schedule,
)

def _signal(**kw):
    base = dict(schedule_id="cron-001", tenant_scope="multiteiner",
                task_digest="task-a", source_refs=("hermes:cron:1",),
                schedule_expression="0 * * * *", owner_principal="elo",
                provenance_verified=True, explicit_authorization=True,
                idempotent=True)
    base.update(kw)
    return ScheduleSignal(**base)

def test_authorized_idempotent_schedule_is_candidate_only():
    a = assess_schedule(_signal())
    assert a.disposition is ScheduleDisposition.CANDIDATE
    assert a.canonical_authority is False
    assert a.execution_permitted is False

def test_missing_authorization_remains_observation():
    a = assess_schedule(_signal(explicit_authorization=False))
    assert a.disposition is ScheduleDisposition.OBSERVATION

def test_non_idempotent_schedule_remains_observation():
    a = assess_schedule(_signal(idempotent=False))
    assert a.disposition is ScheduleDisposition.OBSERVATION

def test_governance_bypass_is_rejected():
    a = assess_schedule(_signal(governance_bypass=True))
    assert a.disposition is ScheduleDisposition.REJECTED

def test_missing_provenance_is_rejected():
    a = assess_schedule(_signal(provenance_verified=False))
    assert a.disposition is ScheduleDisposition.REJECTED
