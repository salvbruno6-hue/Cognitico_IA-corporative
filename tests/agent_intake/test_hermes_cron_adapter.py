from elo.agent_intake.hermes_cron_adapter import adapt_schedule
from elo.agent_intake.hermes_cron_boundary import ScheduleDisposition, ScheduleSignal


def signal(**overrides):
    values = dict(
        schedule_id="cron-test-1",
        tenant_scope="multiteiner",
        task_digest="task-1",
        source_refs=("controlled-eval:cron/1",),
        schedule_expression="0 8 * * *",
        owner_principal="elo",
        provenance_verified=True,
        explicit_authorization=True,
        idempotent=True,
        governance_bypass=False,
    )
    values.update(overrides)
    return ScheduleSignal(**values)


def test_adapts_authorized_idempotent_schedule_to_bounded_contract():
    contract = adapt_schedule(signal())
    assert contract is not None
    assert contract.disposition is ScheduleDisposition.CANDIDATE
    assert contract.idempotency_key == "multiteiner:cron-test-1:task-1"
    assert contract.execution_permitted is False
    assert contract.canonical_authority is False


def test_rejects_non_idempotent_schedule():
    assert adapt_schedule(signal(idempotent=False)) is None


def test_rejects_governance_bypass():
    assert adapt_schedule(signal(governance_bypass=True)) is None
