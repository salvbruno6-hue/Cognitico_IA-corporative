"""Bounded registration adapter for EXT-CRON-HERMES.

The adapter materializes an authorized, idempotent schedule contract in memory.
It does not register with a scheduler, execute a task, mutate permissions, or
grant canonical authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from .hermes_cron_boundary import ScheduleDisposition, ScheduleSignal, assess_schedule


@dataclass(frozen=True, slots=True)
class ScheduledInvocationContract:
    schedule_id: str
    tenant_scope: str
    task_digest: str
    schedule_expression: str
    owner_principal: str
    source_refs: tuple[str, ...]
    idempotency_key: str
    disposition: ScheduleDisposition
    execution_permitted: bool = False
    canonical_authority: bool = False


class CronAdapter:
    """Turn an already-authorized schedule signal into a bounded contract."""

    def adapt(self, signal: ScheduleSignal) -> ScheduledInvocationContract | None:
        assessment = assess_schedule(signal)
        if assessment.disposition is not ScheduleDisposition.CANDIDATE:
            return None
        return ScheduledInvocationContract(
            schedule_id=signal.schedule_id,
            tenant_scope=signal.tenant_scope,
            task_digest=signal.task_digest,
            schedule_expression=signal.schedule_expression,
            owner_principal=signal.owner_principal,
            source_refs=assessment.evidence_refs,
            idempotency_key=f"{signal.tenant_scope}:{signal.schedule_id}:{signal.task_digest}",
            disposition=assessment.disposition,
        )


def adapt_schedule(signal: ScheduleSignal) -> ScheduledInvocationContract | None:
    return CronAdapter().adapt(signal)


__all__ = ["CronAdapter", "ScheduledInvocationContract", "adapt_schedule"]
