"""Controlled evaluation of Hermes cron scheduling boundary."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_cron_boundary import ScheduleDisposition, ScheduleSignal, assess_schedule

CAPABILITY_ID = "EXT-CRON-HERMES"

@dataclass(frozen=True)
class CronEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

def _signals(prefix: str):
    return tuple(ScheduleSignal(
        schedule_id=f"{prefix}-{i}", tenant_scope="multiteiner",
        task_digest=f"task-{i}", source_refs=(f"hermes:cron:{prefix.lower()}/{i}",),
        schedule_expression="0 8 * * *", owner_principal="elo",
        provenance_verified=True, explicit_authorization=True, idempotent=True,
    ) for i in range(1,6))

def _rate(signals):
    return sum(assess_schedule(s).disposition is ScheduleDisposition.CANDIDATE for s in signals)/len(signals)

def _integrity(signals):
    return sum((a:=assess_schedule(s)).canonical_authority is False and a.execution_permitted is False for s in signals)/len(signals)

def evaluate() -> CronEvaluation:
    baseline=_signals("BASE"); adapted=_signals("HERMES")
    b=_rate(baseline); a=_rate(adapted); i=_integrity(adapted)
    repeatable=_rate(_signals("REPEAT"))==a and i==1.0
    result="EVOLUTION_GATE_REQUIRED" if a>b and repeatable else "RETEST"
    return CronEvaluation(b,a,i,repeatable,result)
